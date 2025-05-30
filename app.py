import streamlit as st
import pandas as pd
from pathlib import Path
import json
import os
from typing import Dict, List, Any

from file_parser import FileParser
from knowledge_base_manager import KnowledgeBaseManager
from recommendation_engine import RecommendationEngine

# Configuration de la page
st.set_page_config(
    page_title="Système d'Aide à l'Orientation Professionnelle IA - Bénin",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour améliorer l'apparence
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f4037 0%, #99f2c8 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
}
.main-header h1 {
    color: white;
    margin: 0;
    font-size: 2.5rem;
}
.main-header p {
    color: white;
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
    opacity: 0.9;
}
.student-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
    background-color: #f9f9f9;
}
.recommendation-section {
    background-color: #e8f5e8;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}
.alert-warning {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
.alert-success {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialise les variables de session."""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'processed_students' not in st.session_state:
        st.session_state.processed_students = []
    if 'knowledge_base_loaded' not in st.session_state:
        st.session_state.knowledge_base_loaded = False

def main():
    """Fonction principale de l'application."""
    initialize_session_state()
    
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Système d'Aide à l'Orientation Professionnelle IA</h1>
        <p>Guidez vos étudiants vers des carrières adaptées au marché du travail béninois</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barre latérale pour la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Configuration de la clé API
        st.subheader("🔑 Clé API OpenRouter")
        api_key = st.text_input(
            "Entrez votre clé API OpenRouter:",
            type="password",
            value=st.session_state.api_key,
            help="Obtenez votre clé API sur https://openrouter.ai"
        )
        
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
        
        # Vérification de la base de connaissances
        st.subheader("📚 Base de Connaissances")
        knowledge_file_path = "knowledge_base_benin.json"
        
        if os.path.exists(knowledge_file_path):
            st.success("✅ Base de connaissances trouvée")
            st.session_state.knowledge_base_loaded = True
        else:
            st.error("❌ Fichier knowledge_base_benin.json non trouvé")
            st.session_state.knowledge_base_loaded = False
            st.markdown("""
            <div class="alert-warning">
                <strong>⚠️ Attention:</strong> Le fichier knowledge_base_benin.json 
                doit être présent dans le répertoire racine pour que l'application fonctionne.
            </div>
            """, unsafe_allow_html=True)
        
        # Informations sur l'application
        st.subheader("ℹ️ À Propos")
        st.markdown("""
        Cette application analyse les profils d'étudiants et fournit des recommandations 
        d'orientation basées sur:
        - La filière actuelle de l'étudiant
        - Ses aspirations professionnelles
        - Les réalités du marché du travail béninois
        - L'intelligence artificielle (DeepSeek)
        """)
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Téléversement du Fichier Étudiants")
        
        uploaded_file = st.file_uploader(
            "Choisissez un fichier Excel (.xlsx) ou Word (.docx)",
            type=['xlsx', 'docx'],
            help="Le fichier doit contenir les colonnes: Nom, Prénom, Date de Naissance, Lieu de Naissance, Filière Actuelle, Carrière Envisagée"
        )
        
        if uploaded_file is not None:
            if not st.session_state.api_key:
                st.error("🔑 Veuillez d'abord configurer votre clé API OpenRouter dans la barre latérale.")
                return
            
            if not st.session_state.knowledge_base_loaded:
                st.error("📚 La base de connaissances n'est pas disponible. Vérifiez le fichier knowledge_base_benin.json.")
                return
            
            try:
                # Traitement du fichier
                with st.spinner("📖 Lecture du fichier..."):
                    file_parser = FileParser()
                    students_data = file_parser.parse_file(uploaded_file)
                
                if students_data:
                    st.success(f"✅ {len(students_data)} étudiants trouvés dans le fichier")
                    
                    # Chargement de la base de connaissances
                    with st.spinner("📚 Chargement de la base de connaissances..."):
                        kb_manager = KnowledgeBaseManager()
                        kb_manager.load_knowledge_base(knowledge_file_path)
                    
                    # Initialisation du moteur de recommandation
                    rec_engine = RecommendationEngine(st.session_state.api_key, kb_manager)
                    
                    # Traitement des recommandations
                    st.header("🎯 Analyse et Recommandations")
                    
                    processed_students = []
                    progress_bar = st.progress(0)
                    
                    for i, student in enumerate(students_data):
                        with st.spinner(f"🤖 Analyse en cours pour {student.get('Nom', 'N/A')} {student.get('Prénom', 'N/A')}..."):
                            try:
                                recommendation = rec_engine.generate_recommendation(student)
                                processed_students.append({
                                    'student': student,
                                    'recommendation': recommendation
                                })
                            except Exception as e:
                                st.error(f"❌ Erreur lors de l'analyse de {student.get('Nom', 'N/A')}: {str(e)}")
                                processed_students.append({
                                    'student': student,
                                    'recommendation': {'error': str(e)}
                                })
                        
                        progress_bar.progress((i + 1) / len(students_data))
                    
                    st.session_state.processed_students = processed_students
                    progress_bar.empty()
                    
                    # Affichage des résultats
                    display_results(processed_students)
                    
                else:
                    st.error("❌ Aucun étudiant trouvé dans le fichier. Vérifiez le format.")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors du traitement du fichier: {str(e)}")
    
    with col2:
        st.header("📊 Statistiques")
        if st.session_state.processed_students:
            total_students = len(st.session_state.processed_students)
            successful_analyses = sum(1 for item in st.session_state.processed_students 
                                    if 'error' not in item['recommendation'])
            
            st.metric("Étudiants analysés", total_students)
            st.metric("Analyses réussies", successful_analyses)
            st.metric("Taux de réussite", f"{(successful_analyses/total_students*100):.1f}%")
        else:
            st.info("📊 Les statistiques apparaîtront après l'analyse")

def display_results(processed_students: List[Dict[str, Any]]):
    """Affiche les résultats des analyses."""
    st.header("📋 Résultats Détaillés")
    
    for i, item in enumerate(processed_students):
        student = item['student']
        recommendation = item['recommendation']
        
        # Informations de base de l'étudiant
        student_name = f"{student.get('Nom', 'N/A')} {student.get('Prénom', 'N/A')}"
        
        with st.expander(f"👤 {student_name} - {student.get('Filière Actuelle', 'N/A')}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Profil Étudiant")
                st.write(f"**Nom:** {student.get('Nom', 'N/A')}")
                st.write(f"**Prénom:** {student.get('Prénom', 'N/A')}")
                st.write(f"**Date de Naissance:** {student.get('Date de Naissance', 'N/A')}")
                st.write(f"**Lieu de Naissance:** {student.get('Lieu de Naissance', 'N/A')}")
                st.write(f"**Filière Actuelle:** {student.get('Filière Actuelle', 'N/A')}")
                st.write(f"**Carrière Envisagée:** {student.get('Carrière Envisagée', 'N/A')}")
            
            with col2:
                if 'error' in recommendation:
                    st.error(f"❌ **Erreur d'analyse:** {recommendation['error']}")
                else:
                    st.subheader("🎯 Recommandations IA")
                    
                    # Affichage structuré des recommandations
                    if 'analysis' in recommendation:
                        st.markdown("**📊 Analyse:**")
                        st.write(recommendation['analysis'])
                    
                    if 'adequacy_level' in recommendation:
                        st.markdown("**⚖️ Niveau d'Adéquation:**")
                        st.write(recommendation['adequacy_level'])
                    
                    if 'alternative_careers' in recommendation:
                        st.markdown("**🔄 Carrières Alternatives:**")
                        st.write(recommendation['alternative_careers'])
                    
                    if 'personalized_path' in recommendation:
                        st.markdown("**🛤️ Parcours Personnalisé:**")
                        st.write(recommendation['personalized_path'])
            
            # Section complète de la recommandation
            if 'error' not in recommendation and 'full_recommendation' in recommendation:
                st.markdown("---")
                st.subheader("📄 Recommandation Complète")
                st.markdown(f"""
                <div class="recommendation-section">
                {recommendation['full_recommendation']}
                </div>
                """, unsafe_allow_html=True)
    
    # Bouton d'export (fonctionnalité future)
    if st.button("📤 Exporter les Résultats (JSON)", key="export_results"):
        export_data = {
            'students_analysis': processed_students,
            'generated_at': pd.Timestamp.now().isoformat()
        }
        
        st.download_button(
            label="💾 Télécharger le Rapport JSON",
            data=json.dumps(export_data, ensure_ascii=False, indent=2),
            file_name=f"rapport_orientation_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()