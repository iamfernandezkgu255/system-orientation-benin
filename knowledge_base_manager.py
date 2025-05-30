import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Metier:
    """Classe représentant un métier/carrière."""
    nom_metier: str
    description: str
    secteur_activite: str
    competences_requises_techniques: List[str]
    competences_requises_transversales: List[str]
    formations_typiques: List[str]
    niveau_demande_marche: str  # "élevé", "moyen", "faible"
    perspectives_croissance: bool
    pertinence_realites_africaines_benin: str

@dataclass
class Secteur:
    """Classe représentant un secteur d'activité."""
    nom_secteur: str
    description: str
    metiers_associes: List[str]

@dataclass
class Competence:
    """Classe représentant une compétence."""
    nom_competence: str
    type_competence: str  # "technique", "transversale", "numérique"
    description: Optional[str] = ""

@dataclass
class Formation:
    """Classe représentant une formation."""
    nom_formation: str
    description: str
    metiers_prepares: List[str]
    institutions_references: List[str]

class KnowledgeBaseManager:
    """
    Gestionnaire de la base de connaissances sur le marché du travail béninois.
    """
    
    def __init__(self):
        self.metiers: Dict[str, Metier] = {}
        self.secteurs: Dict[str, Secteur] = {}
        self.competences: Dict[str, Competence] = {}
        self.formations: Dict[str, Formation] = {}
        self.is_loaded = False
    
    def load_knowledge_base(self, file_path: str) -> bool:
        """
        Charge la base de connaissances depuis un fichier JSON.
        
        Args:
            file_path: Chemin vers le fichier JSON
            
        Returns:
            bool: True si le chargement est réussi
        """
        try:
            if not Path(file_path).exists():
                logger.error(f"Fichier de base de connaissances non trouvé: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Charger les métiers
            if 'metiers' in data:
                for metier_data in data['metiers']:
                    metier = Metier(**metier_data)
                    self.metiers[metier.nom_metier.lower()] = metier
            
            # Charger les secteurs
            if 'secteurs_porteurs' in data:
                for secteur_data in data['secteurs_porteurs']:
                    secteur = Secteur(**secteur_data)
                    self.secteurs[secteur.nom_secteur.lower()] = secteur
            
            # Charger les compétences
            if 'competences' in data:
                for comp_data in data['competences']:
                    competence = Competence(**comp_data)
                    self.competences[competence.nom_competence.lower()] = competence
            
            # Charger les formations
            if 'formations' in data:
                for form_data in data['formations']:
                    formation = Formation(**form_data)
                    self.formations[formation.nom_formation.lower()] = formation
            
            self.is_loaded = True
            logger.info(f"Base de connaissances chargée: {len(self.metiers)} métiers, "
                       f"{len(self.secteurs)} secteurs, {len(self.competences)} compétences, "
                       f"{len(self.formations)} formations")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la base de connaissances: {str(e)}")
            return False
    
    def find_metier(self, nom_metier: str) -> Optional[Metier]:
        """
        Recherche un métier par nom (recherche flexible).
        
        Args:
            nom_metier: Nom du métier à rechercher
            
        Returns:
            Optional[Metier]: Métier trouvé ou None
        """
        if not nom_metier:
            return None
        
        nom_recherche = nom_metier.lower().strip()
        
        # Recherche exacte
        if nom_recherche in self.metiers:
            return self.metiers[nom_recherche]
        
        # Recherche partielle
        for nom, metier in self.metiers.items():
            if nom_recherche in nom or nom in nom_recherche:
                return metier
        
        # Recherche par mots-clés
        mots_recherche = nom_recherche.split()
        for nom, metier in self.metiers.items():
            if any(mot in nom for mot in mots_recherche):
                return metier
        
        return None
    
    def find_secteur(self, nom_secteur: str) -> Optional[Secteur]:
        """
        Recherche un secteur par nom.
        
        Args:
            nom_secteur: Nom du secteur à rechercher
            
        Returns:
            Optional[Secteur]: Secteur trouvé ou None
        """
        if not nom_secteur:
            return None
        
        nom_recherche = nom_secteur.lower().strip()
        
        # Recherche exacte
        if nom_recherche in self.secteurs:
            return self.secteurs[nom_recherche]
        
        # Recherche partielle
        for nom, secteur in self.secteurs.items():
            if nom_recherche in nom or nom in nom_recherche:
                return secteur
        
        return None
    
    def get_metiers_by_secteur(self, nom_secteur: str) -> List[Metier]:
        """
        Récupère tous les métiers d'un secteur donné.
        
        Args:
            nom_secteur: Nom du secteur
            
        Returns:
            List[Metier]: Liste des métiers du secteur
        """
        secteur = self.find_secteur(nom_secteur)
        if not secteur:
            return []
        
        metiers_secteur = []
        for nom_metier in secteur.metiers_associes:
            metier = self.find_metier(nom_metier)
            if metier:
                metiers_secteur.append(metier)
        
        return metiers_secteur
    
    def get_metiers_high_demand(self) -> List[Metier]:
        """
        Récupère les métiers à forte demande.
        
        Returns:
            List[Metier]: Liste des métiers à forte demande
        """
        return [metier for metier in self.metiers.values() 
                if metier.niveau_demande_marche.lower() == "élevé"]
    
    def get_metiers_with_growth(self) -> List[Metier]:
        """
        Récupère les métiers avec de bonnes perspectives de croissance.
        
        Returns:
            List[Metier]: Liste des métiers avec perspectives de croissance
        """
        return [metier for metier in self.metiers.values() 
                if metier.perspectives_croissance]
    
    def find_similar_metiers(self, metier_reference: Metier, max_results: int = 3) -> List[Metier]:
        """
        Trouve des métiers similaires basés sur les compétences et le secteur.
        
        Args:
            metier_reference: Métier de référence
            max_results: Nombre maximum de résultats
            
        Returns:
            List[Metier]: Liste des métiers similaires
        """
        metiers_similaires = []
        
        for metier in self.metiers.values():
            if metier.nom_metier == metier_reference.nom_metier:
                continue
            
            score_similarite = 0
            
            # Score basé sur le secteur
            if metier.secteur_activite.lower() == metier_reference.secteur_activite.lower():
                score_similarite += 3
            
            # Score basé sur les compétences techniques communes
            competences_communes = set(metier.competences_requises_techniques) & \
                                 set(metier_reference.competences_requises_techniques)
            score_similarite += len(competences_communes)
            
            # Score basé sur les compétences transversales communes
            competences_trans_communes = set(metier.competences_requises_transversales) & \
                                       set(metier_reference.competences_requises_transversales)
            score_similarite += len(competences_trans_communes) * 0.5
            
            if score_similarite > 0:
                metiers_similaires.append((metier, score_similarite))
        
        # Trier par score de similarité décroissant
        metiers_similaires.sort(key=lambda x: x[1], reverse=True)
        
        return [metier for metier, _ in metiers_similaires[:max_results]]
    
    def get_formations_for_metier(self, nom_metier: str) -> List[Formation]:
        """
        Récupère les formations qui préparent à un métier donné.
        
        Args:
            nom_metier: Nom du métier
            
        Returns:
            List[Formation]: Liste des formations pertinentes
        """
        formations_pertinentes = []
        
        for formation in self.formations.values():
            if any(nom_metier.lower() in metier_prepare.lower() 
                   for metier_prepare in formation.metiers_prepares):
                formations_pertinentes.append(formation)
        
        return formations_pertinentes
    
    def analyze_filiere_metier_compatibility(self, filiere: str, metier_envisage: str) -> Dict[str, Any]:
        """
        Analyse la compatibilité entre une filière et un métier envisagé.
        
        Args:
            filiere: Filière actuelle de l'étudiant
            metier_envisage: Métier envisagé par l'étudiant
            
        Returns:
            Dict[str, Any]: Analyse de compatibilité
        """
        analysis = {
            'metier_trouve': False,
            'metier_data': None,
            'compatibility_score': 0,
            'formations_matching': [],
            'competences_gaps': [],
            'recommendations': []
        }
        
        # Rechercher le métier envisagé
        metier = self.find_metier(metier_envisage)
        if metier:
            analysis['metier_trouve'] = True
            analysis['metier_data'] = metier
            
            # Analyser les formations typiques pour ce métier
            formations_matching = []
            for formation_nom in metier.formations_typiques:
                if filiere.lower() in formation_nom.lower() or formation_nom.lower() in filiere.lower():
                    formations_matching.append(formation_nom)
            
            analysis['formations_matching'] = formations_matching
            
            # Calculer un score de compatibilité
            if formations_matching:
                analysis['compatibility_score'] = 8  # Forte compatibilité
            else:
                # Vérifier les compétences transversales
                if metier.competences_requises_transversales:
                    analysis['compatibility_score'] = 5  # Compatibilité moyenne
                else:
                    analysis['compatibility_score'] = 2  # Faible compatibilité
            
            # Identifier les gaps de compétences potentiels
            if not formations_matching:
                analysis['competences_gaps'] = metier.competences_requises_techniques
            
            # Générer des recommandations
            if analysis['compatibility_score'] >= 7:
                analysis['recommendations'].append("Excellente adéquation entre votre filière et le métier envisagé.")
            elif analysis['compatibility_score'] >= 5:
                analysis['recommendations'].append("Adéquation correcte. Considérez des formations complémentaires.")
            else:
                analysis['recommendations'].append("Faible adéquation. Explorez d'autres métiers ou formations de transition.")
        
        return analysis
    
    def get_secteurs_porteurs(self) -> List[Secteur]:
        """
        Récupère tous les secteurs porteurs.
        
        Returns:
            List[Secteur]: Liste des secteurs porteurs
        """
        return list(self.secteurs.values())
    
    def get_knowledge_base_summary(self) -> Dict[str, Any]:
        """
        Génère un résumé de la base de connaissances.
        
        Returns:
            Dict[str, Any]: Résumé des données disponibles
        """
        if not self.is_loaded:
            return {"error": "Base de connaissances non chargée"}
        
        summary = {
            "total_metiers": len(self.metiers),
            "total_secteurs": len(self.secteurs),
            "total_competences": len(self.competences),
            "total_formations": len(self.formations),
            "metiers_forte_demande": len(self.get_metiers_high_demand()),
            "metiers_croissance": len(self.get_metiers_with_growth()),
            "secteurs_disponibles": [secteur.nom_secteur for secteur in self.secteurs.values()],
            "is_loaded": self.is_loaded
        }
        
        return summary
    
    def search_metiers_by_keywords(self, keywords: List[str]) -> List[Metier]:
        """
        Recherche des métiers par mots-clés dans la description ou les compétences.
        
        Args:
            keywords: Liste de mots-clés à rechercher
            
        Returns:
            List[Metier]: Liste des métiers correspondants
        """
        if not keywords:
            return []
        
        metiers_found = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for metier in self.metiers.values():
            score = 0
            
            # Recherche dans la description
            description_lower = metier.description.lower()
            for keyword in keywords_lower:
                if keyword in description_lower:
                    score += 2
            
            # Recherche dans les compétences techniques
            for competence in metier.competences_requises_techniques:
                comp_lower = competence.lower()
                for keyword in keywords_lower:
                    if keyword in comp_lower:
                        score += 1
            
            # Recherche dans les compétences transversales
            for competence in metier.competences_requises_transversales:
                comp_lower = competence.lower()
                for keyword in keywords_lower:
                    if keyword in comp_lower:
                        score += 1
            
            if score > 0:
                metiers_found.append((metier, score))
        
        # Trier par score décroissant
        metiers_found.sort(key=lambda x: x[1], reverse=True)
        
        return [metier for metier, _ in metiers_found]
    
    def validate_knowledge_base(self) -> Dict[str, Any]:
        """
        Valide l'intégrité de la base de connaissances.
        
        Returns:
            Dict[str, Any]: Rapport de validation
        """
        validation_report = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': self.get_knowledge_base_summary()
        }
        
        if not self.is_loaded:
            validation_report['is_valid'] = False
            validation_report['errors'].append("Base de connaissances non chargée")
            return validation_report
        
        # Vérifier les métiers
        for nom, metier in self.metiers.items():
            if not metier.description:
                validation_report['warnings'].append(f"Métier '{nom}' sans description")
            if not metier.competences_requises_techniques:
                validation_report['warnings'].append(f"Métier '{nom}' sans compétences techniques")
        
        # Vérifier les secteurs
        for nom, secteur in self.secteurs.items():
            if not secteur.metiers_associes:
                validation_report['warnings'].append(f"Secteur '{nom}' sans métiers associés")
        
        return validation_report 