import streamlit as st
import pandas as pd
from pathlib import Path
import json
import os
from typing import Dict, List, Any

from personality_test import MBTI_QUESTIONS, calculate_mbti_profile, get_mbti_description, get_mbti_explanations_for_profile, MBTI_EXPLANATIONS
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
    if 'mbti_checkbox_states' not in st.session_state:
        st.session_state.mbti_checkbox_states = {}
    if 'mbti_answers' not in st.session_state:
        st.session_state.mbti_answers = {}
    if 'mbti_profile' not in st.session_state:
        st.session_state.mbti_profile = ""
    if 'show_mbti_results' not in st.session_state:
        st.session_state.show_mbti_results = False

def display_personality_test():
    st.header("Test de Personnalite (inspire du MBTI)")
    st.markdown("Cochez toutes les phrases qui vous correspondent. Votre profil sera determine par la lettre majoritaire dans chaque categorie.")

    if not st.session_state.mbti_checkbox_states or \
       any(dim not in st.session_state.mbti_checkbox_states for dim in MBTI_QUESTIONS.keys()):
        for dim_code, types_data_init in MBTI_QUESTIONS.items():
            if dim_code not in st.session_state.mbti_checkbox_states:
                st.session_state.mbti_checkbox_states[dim_code] = {}
            for type_code, questions_list in types_data_init.items():
                if type_code not in st.session_state.mbti_checkbox_states[dim_code]:
                    st.session_state.mbti_checkbox_states[dim_code][type_code] = [False] * len(questions_list)

    with st.form(key="mbti_form"):
        for i, (dim_code, types_data_form) in enumerate(MBTI_QUESTIONS.items()):
            st.subheader(f"{i+1}. Etes-vous plutot « {list(types_data_form.keys())[0]} » ou plutot « {list(types_data_form.keys())[1]} » ?")

            cols = st.columns(len(types_data_form))

            for idx_type, (type_code, questions) in enumerate(types_data_form.items()):
                with cols[idx_type]:
                    st.markdown(f"**{type_code}**")
                    for q_idx, question in enumerate(questions):
                        checkbox_key = f"cb_{dim_code}_{type_code}_{q_idx}"
                        current_val = st.session_state.mbti_checkbox_states.get(dim_code, {}).get(type_code, [False]*len(questions))[q_idx]
                        st.session_state.mbti_checkbox_states[dim_code][type_code][q_idx] = \
                            st.checkbox(question,
                                        value=current_val,
                                        key=checkbox_key)

        submit_button = st.form_submit_button("Voir mon profil MBTI")

    if submit_button:
        calculated_scores = {dim: {} for dim in MBTI_QUESTIONS.keys()}
        for dim_code, types_data_calc in st.session_state.mbti_checkbox_states.items():
            for type_code, question_states in types_data_calc.items():
                calculated_scores[dim_code][type_code] = sum(1 for state in question_states if state)

        st.session_state.mbti_answers = calculated_scores
        st.session_state.mbti_profile = calculate_mbti_profile(st.session_state.mbti_answers)
        st.session_state.show_mbti_results = True
        st.experimental_rerun()

    if st.session_state.get('show_mbti_results') == True and st.session_state.get('mbti_profile'):
        st.subheader(f"Votre profil MBTI est : {st.session_state.mbti_profile}")
        profile_info = get_mbti_description(st.session_state.mbti_profile)
        if profile_info:
            st.markdown(f"**{profile_info.get('title', '')} ({profile_info.get('group', '')})**")
            st.write(profile_info.get('summary', 'Description non disponible.'))

            st.markdown("---")
            st.subheader("Explication de votre profil :")
            current_profile = st.session_state.mbti_profile
            explanations_by_letter = get_mbti_explanations_for_profile(current_profile)

            if explanations_by_letter and current_profile and len(current_profile) == 4:
                letter_dims = ["EI", "SN", "TF", "JP"]
                for i, dim_key in enumerate(letter_dims):
                    letter_explanation = explanations_by_letter.get(dim_key)
                    if letter_explanation and letter_explanation.get('label'):
                        st.markdown(f"**{letter_explanation['label']} ({current_profile[i]})**: {letter_explanation['description']}")

        if st.button("Commencer l'analyse d'orientation"):
            st.session_state.show_mbti_results = 'completed'
            st.experimental_rerun()

    elif st.session_state.get('show_mbti_results') == 'completed':
        pass

def main():
    """Fonction principale de l'application."""
    initialize_session_state()

    st.markdown("<div class='main-header'><h1>Systeme d'Aide a l'Orientation Professionnelle IA</h1><p>Guidez vos etudiants vers des carrieres adaptees au marche du travail beninois</p></div>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("Configuration")

        st.subheader("Cle API OpenRouter")
        api_key_input = st.text_input(
            "Entrez votre cle API OpenRouter:",
            type="password",
            value=st.session_state.api_key,
            help="Obtenez votre cle API sur https://openrouter.ai"
        )

        if api_key_input != st.session_state.api_key:
            st.session_state.api_key = api_key_input

        st.subheader("Base de Connaissances")
        knowledge_file_path = "knowledge_base_benin.json"

        if os.path.exists(knowledge_file_path):
            st.success("(OK) Base de connaissances trouvee")
            st.session_state.knowledge_base_loaded = True
        else:
            st.error("(Erreur) Fichier knowledge_base_benin.json non trouve")
            st.session_state.knowledge_base_loaded = False
            st.markdown("<div class='alert-warning'><strong>(Attention) Attention:</strong> Le fichier knowledge_base_benin.json doit etre present.</div>", unsafe_allow_html=True)

        st.subheader("A Propos")
        # Splitting "A Propos" into multiple markdown calls
        st.markdown("Cette application analyse les profils d'etudiants et fournit des recommandations d'orientation basees sur:")
        st.markdown("- La filiere actuelle de l'etudiant")
        st.markdown("- Ses aspirations professionnelles")
        st.markdown("- Les realites du marche du travail beninois")
        st.markdown("- L'intelligence artificielle (DeepSeek)")
        st.markdown("- (Optionnel) Son profil de personnalite MBTI")

    if st.session_state.get('show_mbti_results') != 'completed':
        display_personality_test()
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.header("Televersement du Fichier Etudiants")

            uploaded_file = st.file_uploader(
                "Choisissez un fichier Excel (.xlsx) ou Word (.docx)",
                type=['xlsx', 'docx'],
                help="Le fichier doit contenir les colonnes: Nom, Prenom, Date de Naissance, Lieu de Naissance, Filiere Actuelle, Carriere Envisagee"
            )

            if uploaded_file is not None:
                if not st.session_state.api_key:
                    st.error("(Erreur) Veuillez d'abord configurer votre cle API OpenRouter dans la barre laterale.")
                    st.stop()

                if not st.session_state.knowledge_base_loaded:
                    st.error("(Erreur) La base de connaissances n'est pas disponible. Verifiez le fichier knowledge_base_benin.json.")
                    st.stop()

                try:
                    with st.spinner("Lecture du fichier..."):
                        file_parser = FileParser()
                        students_data = file_parser.parse_file(uploaded_file)

                    if students_data:
                        st.success(f"(OK) {len(students_data)} etudiants trouves dans le fichier")

                        with st.spinner("Chargement de la base de connaissances..."):
                            kb_manager = KnowledgeBaseManager()
                            kb_manager.load_knowledge_base(knowledge_file_path)

                        rec_engine = RecommendationEngine(st.session_state.api_key, kb_manager)

                        st.header("Analyse et Recommandations")

                        processed_students = []
                        progress_bar = st.progress(0)

                        for i, student_item in enumerate(students_data):
                            with st.spinner(f"Analyse en cours pour {student_item.get('Nom', 'N/A')} {student_item.get('Prénom', 'N/A')}..."):
                                try:
                                    # Retrieve MBTI profile from session state. Default to None if not found or not a string.
                                    mbti_profile_to_pass = st.session_state.get('mbti_profile')
                                    if not isinstance(mbti_profile_to_pass, str) or mbti_profile_to_pass == "----":
                                        mbti_profile_to_pass = None # Ensure we pass None if it's invalid or placeholder

                                    recommendation = rec_engine.generate_recommendation(student_item, mbti_profile=mbti_profile_to_pass)

                                    processed_students.append({
                                        'student': student_item,
                                        'recommendation': recommendation
                                    })
                                except Exception as e:
                                    st.error(f"(Erreur) Erreur lors de l'analyse de {student_item.get('Nom', 'N/A')}: {str(e)}")
                                    processed_students.append({
                                        'student': student_item,
                                        'recommendation': {'error': str(e)}
                                    })

                            progress_bar.progress((i + 1) / len(students_data))

                        st.session_state.processed_students = processed_students
                        progress_bar.empty()

                        display_results(processed_students)

                    else:
                        st.error("(Erreur) Aucun etudiant trouve dans le fichier. Verifiez le format.")

                except Exception as e:
                    st.error(f"(Erreur) Erreur lors du traitement du fichier: {str(e)}")

        with col2:
            st.header("Statistiques")
            if st.session_state.get('processed_students'):
                total_students = len(st.session_state.processed_students)
                successful_analyses = sum(1 for item in st.session_state.processed_students
                                        if 'error' not in item['recommendation'])

                st.metric("Etudiants analyses", total_students)
                st.metric("Analyses reussies", successful_analyses)
                if total_students > 0:
                    st.metric("Taux de reussite", f"{(successful_analyses/total_students*100):.1f}%")
                else:
                    st.metric("Taux de reussite", "N/A")
            else:
                st.info("Les statistiques apparaitront apres l'analyse")

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
