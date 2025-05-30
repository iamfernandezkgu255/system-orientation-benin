import json
import requests
from typing import Dict, List, Any, Optional
import logging
from knowledge_base_manager import KnowledgeBaseManager, Metier
import time

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    Moteur de recommandation utilisant l'API DeepSeek via OpenRouter.
    """
    
    def __init__(self, api_key: str, knowledge_base_manager: KnowledgeBaseManager):
        self.api_key = api_key
        self.kb_manager = knowledge_base_manager
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-chat"
        self.max_retries = 3
        self.retry_delay = 2
    
    def generate_recommendation(self, student_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Génère une recommandation complète pour un étudiant.
        
        Args:
            student_data: Données de l'étudiant
            
        Returns:
            Dict[str, Any]: Recommandation structurée
        """
        try:
            # Analyser le profil de l'étudiant
            student_analysis = self._analyze_student_profile(student_data)
            
            # Générer le prompt pour DeepSeek
            prompt = self._build_deepseek_prompt(student_data, student_analysis)
            
            # Appeler l'API DeepSeek
            ai_response = self._call_deepseek_api(prompt)
            
            # Structurer la réponse
            recommendation = self._structure_recommendation(ai_response, student_analysis)
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de recommandation: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_student_profile(self, student_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyse le profil de l'étudiant avec la base de connaissances.
        
        Args:
            student_data: Données de l'étudiant
            
        Returns:
            Dict[str, Any]: Analyse du profil
        """
        analysis = {
            'filiere_actuelle': student_data.get('Filière Actuelle', ''),
            'carriere_envisagee': student_data.get('Carrière Envisagée', ''),
            'metier_trouve': None,
            'compatibility_analysis': None,
            'alternative_careers': [],
            'secteur_recommendations': []
        }
        
        # Analyser la carrière envisagée
        if analysis['carriere_envisagee']:
            metier = self.kb_manager.find_metier(analysis['carriere_envisagee'])
            if metier:
                analysis['metier_trouve'] = metier
                
                # Analyser la compatibilité filière-métier
                compatibility = self.kb_manager.analyze_filiere_metier_compatibility(
                    analysis['filiere_actuelle'],
                    analysis['carriere_envisagee']
                )
                analysis['compatibility_analysis'] = compatibility
                
                # Trouver des métiers similaires
                similar_metiers = self.kb_manager.find_similar_metiers(metier, max_results=3)
                analysis['alternative_careers'] = similar_metiers
        
        # Recommander des secteurs porteurs
        secteurs_porteurs = self.kb_manager.get_secteurs_porteurs()
        analysis['secteur_recommendations'] = secteurs_porteurs[:3]  # Top 3 secteurs
        
        return analysis
    
    def _build_deepseek_prompt(self, student_data: Dict[str, str], analysis: Dict[str, Any]) -> str:
        """
        Construit le prompt pour l'API DeepSeek.
        
        Args:
            student_data: Données de l'étudiant
            analysis: Analyse préliminaire
            
        Returns:
            str: Prompt structuré
        """
        prompt = f"""Tu es un conseiller en orientation professionnelle spécialisé dans le marché du travail béninois. 
Analyse le profil de cet étudiant et fournis des recommandations détaillées.

PROFIL ÉTUDIANT:
- Nom: {student_data.get('Nom', 'N/A')} {student_data.get('Prénom', 'N/A')}
- Filière actuelle: {student_data.get('Filière Actuelle', 'N/A')}
- Carrière envisagée: {student_data.get('Carrière Envisagée', 'N/A')}
- Lieu de naissance: {student_data.get('Lieu de Naissance', 'N/A')}

CONTEXTE MARCHÉ DU TRAVAIL BÉNINOIS:
"""
        
        # Ajouter les informations sur le métier envisagé
        if analysis['metier_trouve']:
            metier = analysis['metier_trouve']
            prompt += f"""
MÉTIER ENVISAGÉ - {metier.nom_metier}:
- Description: {metier.description}
- Secteur: {metier.secteur_activite}
- Niveau de demande: {metier.niveau_demande_marche}
- Perspectives de croissance: {'Excellentes' if metier.perspectives_croissance else 'Limitées'}
- Compétences techniques requises: {', '.join(metier.competences_requises_techniques)}
- Compétences transversales: {', '.join(metier.competences_requises_transversales)}
- Formations typiques: {', '.join(metier.formations_typiques)}
- Pertinence pour le Bénin: {metier.pertinence_realites_africaines_benin}
"""
        
        # Ajouter l'analyse de compatibilité
        if analysis['compatibility_analysis']:
            comp_analysis = analysis['compatibility_analysis']
            prompt += f"""
ANALYSE DE COMPATIBILITÉ:
- Score de compatibilité: {comp_analysis['compatibility_score']}/10
- Formations correspondantes: {', '.join(comp_analysis['formations_matching']) if comp_analysis['formations_matching'] else 'Aucune correspondance directe'}
- Lacunes de compétences identifiées: {', '.join(comp_analysis['competences_gaps']) if comp_analysis['competences_gaps'] else 'Aucune lacune majeure'}
"""
        
        # Ajouter les alternatives
        if analysis['alternative_careers']:
            prompt += "\nMÉTIERS ALTERNATIFS SIMILAIRES:\n"
            for alt_metier in analysis['alternative_careers']:
                prompt += f"- {alt_metier.nom_metier}: {alt_metier.description[:100]}... (Demande: {alt_metier.niveau_demande_marche})\n"
        
        # Ajouter les secteurs porteurs
        if analysis['secteur_recommendations']:
            prompt += "\nSECTEURS PORTEURS AU BÉNIN:\n"
            for secteur in analysis['secteur_recommendations']:
                prompt += f"- {secteur.nom_secteur}: {secteur.description[:100]}...\n"
        
        prompt += """

INSTRUCTIONS:
Fournis une analyse structurée en 4 sections:

1. ÉVALUATION DU CHOIX INITIAL (2-3 phrases)
   - Évalue l'adéquation entre la filière actuelle et la carrière envisagée
   - Mentionne les opportunités et défis potentiels

2. NIVEAU D'ADÉQUATION (1-2 phrases)
   - Donne une évaluation claire: Excellente/Bonne/Moyenne/Faible adéquation
   - Justifie brièvement

3. CARRIÈRES ALTERNATIVES (si pertinent, 2-3 suggestions max)
   - Suggère des alternatives uniquement si l'adéquation est moyenne/faible
   - Privilégie les métiers à forte demande mentionnés ci-dessus

4. PARCOURS PERSONNALISÉ (5-6 points concrets)
   - Formations complémentaires spécifiques
   - Compétences clés à développer (avec emphase sur le numérique si pertinent)
   - Certifications utiles
   - Conseils pour l'insertion professionnelle au Bénin
   - Opportunités d'entrepreneuriat si applicable
   - Étapes chronologiques recommandées

Adapte tes recommandations au contexte béninois: marché local, économie numérique émergente, secteurs porteurs comme l'agro-industrie, le tourisme, et l'économie verte.
Sois concret, pratique et encourageant.
"""
        
        return prompt
    
    def _call_deepseek_api(self, prompt: str) -> str:
        """
        Appelle l'API DeepSeek via OpenRouter.
        
        Args:
            prompt: Prompt à envoyer
            
        Returns:
            str: Réponse de l'IA
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit.io",
            "X-Title": "Système Orientation Professionnelle Bénin"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Tu es un expert en orientation professionnelle spécialisé dans le marché du travail africain, particulièrement au Bénin. Tu fournis des conseils pratiques et adaptés au contexte local."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "top_p": 0.9
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=data,
                    timeout=60
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    if 'choices' in response_data and response_data['choices']:
                        return response_data['choices'][0]['message']['content']
                    else:
                        raise Exception("Réponse API invalide: pas de contenu")
                else:
                    error_msg = f"Erreur API ({response.status_code}): {response.text}"
                    if attempt == self.max_retries - 1:
                        raise Exception(error_msg)
                    logger.warning(f"Tentative {attempt + 1} échouée: {error_msg}")
                    time.sleep(self.retry_delay)
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Erreur de connexion: {str(e)}"
                if attempt == self.max_retries - 1:
                    raise Exception(error_msg)
                logger.warning(f"Tentative {attempt + 1} échouée: {error_msg}")
                time.sleep(self.retry_delay)
        
        raise Exception("Échec de tous les appels API")
    
    def _structure_recommendation(self, ai_response: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure la réponse de l'IA en sections organisées.
        
        Args:
            ai_response: Réponse brute de l'IA
            analysis: Analyse préliminaire
            
        Returns:
            Dict[str, Any]: Recommandation structurée
        """
        recommendation = {
            'full_recommendation': ai_response,
            'analysis': '',
            'adequacy_level': '',
            'alternative_careers': '',
            'personalized_path': '',
            'metadata': {
                'student_profile': analysis,
                'generation_timestamp': time.time()
            }
        }
        
        # Essayer de parser les sections de la réponse IA
        try:
            sections = self._parse_ai_sections(ai_response)
            recommendation.update(sections)
        except Exception as e:
            logger.warning(f"Impossible de parser les sections IA: {str(e)}")
            # Si le parsing échoue, garder la réponse complète
            recommendation['analysis'] = ai_response[:500] + "..." if len(ai_response) > 500 else ai_response
        
        return recommendation
    
    def _parse_ai_sections(self, ai_response: str) -> Dict[str, str]:
        """
        Parse les sections de la réponse IA.
        
        Args:
            ai_response: Réponse de l'IA
            
        Returns:
            Dict[str, str]: Sections parsées
        """
        sections = {
            'analysis': '',
            'adequacy_level': '',
            'alternative_careers': '',
            'personalized_path': ''
        }
        
        # Patterns de recherche pour les sections
        section_patterns = {
            'analysis': ['1. ÉVALUATION DU CHOIX INITIAL', 'ÉVALUATION DU CHOIX', 'ANALYSE'],
            'adequacy_level': ['2. NIVEAU D\'ADÉQUATION', 'NIVEAU D\'ADÉQUATION', 'ADÉQUATION'],
            'alternative_careers': ['3. CARRIÈRES ALTERNATIVES', 'CARRIÈRES ALTERNATIVES', 'ALTERNATIVES'],
            'personalized_path': ['4. PARCOURS PERSONNALISÉ', 'PARCOURS PERSONNALISÉ', 'PARCOURS']
        }
        
        lines = ai_response.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Vérifier si cette ligne commence une nouvelle section
            section_found = None
            for section_key, patterns in section_patterns.items():
                for pattern in patterns:
                    if pattern in line.upper():
                        section_found = section_key
                        break
                if section_found:
                    break
            
            if section_found:
                # Sauvegarder la section précédente
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Commencer la nouvelle section
                current_section = section_found
                current_content = []
                
                # Ajouter le contenu de la ligne actuelle (après le titre)
                content_after_title = line
                for pattern in section_patterns[section_found]:
                    if pattern in line.upper():
                        content_after_title = line[line.upper().find(pattern) + len(pattern):].strip()
                        break
                
                if content_after_title and content_after_title != line:
                    current_content.append(content_after_title)
            else:
                # Ajouter à la section courante
                if current_section:
                    current_content.append(line)
        
        # Sauvegarder la dernière section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # Si aucune section n'a été trouvée, mettre tout dans l'analyse
        if not any(sections.values()):
            sections['analysis'] = ai_response
        
        return sections
    
    def test_api_connection(self) -> Dict[str, Any]:
        """
        Teste la connexion à l'API DeepSeek.
        
        Returns:
            Dict[str, Any]: Résultat du test
        """
        try:
            test_prompt = "Bonjour, peux-tu confirmer que tu fonctionnes correctement ? Réponds simplement 'Test réussi'."
            
            response = self._call_deepseek_api(test_prompt)
            
            return {
                'success': True,
                'message': 'Connexion API réussie',
                'response': response[:100] + "..." if len(response) > 100 else response
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Échec de la connexion API: {str(e)}',
                'response': None
            }
    
    def get_engine_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques du moteur de recommandation.
        
        Returns:
            Dict[str, Any]: Statistiques
        """
        return {
            'model_used': self.model,
            'base_url': self.base_url,
            'knowledge_base_loaded': self.kb_manager.is_loaded,
            'knowledge_base_summary': self.kb_manager.get_knowledge_base_summary()
        }