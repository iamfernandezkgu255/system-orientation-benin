import os
from typing import Dict, Any

class Config:
    """
    Classe de configuration pour l'application d'orientation professionnelle.
    """
    
    # Configuration API OpenRouter
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    DEFAULT_MODEL = "deepseek/deepseek-chat"
    
    # Configuration de l'application
    APP_TITLE = "Système d'Aide à l'Orientation Professionnelle IA - Bénin"
    APP_DESCRIPTION = "Guidez vos étudiants vers des carrières adaptées au marché du travail béninois"
    VERSION = "1.0.0"
    
    # Fichiers et chemins
    KNOWLEDGE_BASE_FILE = "knowledge_base_benin.json"
    LOG_FILE = "app.log"
    
    # Configuration IA
    DEFAULT_TEMPERATURE = 0.7
    MAX_TOKENS = 2000
    TOP_P = 0.9
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    
    # Paramètres de l'interface
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    SUPPORTED_FILE_TYPES = ['xlsx', 'docx']
    
    # Colonnes requises dans les fichiers d'étudiants
    REQUIRED_STUDENT_COLUMNS = [
        'Nom', 'Prénom', 'Date de Naissance', 
        'Lieu de Naissance', 'Filière Actuelle', 'Carrière Envisagée'
    ]
    
    # Messages d'erreur
    ERROR_MESSAGES = {
        'no_api_key': "🔑 Veuillez configurer votre clé API OpenRouter dans la barre latérale.",
        'no_knowledge_base': "📚 La base de connaissances n'est pas disponible. Vérifiez le fichier knowledge_base_benin.json.",
        'file_too_large': f"📁 Le fichier est trop volumineux. Taille maximale: {MAX_FILE_SIZE // (1024*1024)} MB",
        'unsupported_format': "📁 Format de fichier non supporté. Utilisez .xlsx ou .docx",
        'api_error': "🤖 Erreur lors de la communication avec l'IA. Vérifiez votre clé API.",
        'parsing_error': "📖 Erreur lors de la lecture du fichier. Vérifiez le format des données."
    }
    
    # Messages de succès
    SUCCESS_MESSAGES = {
        'file_loaded': "✅ Fichier chargé avec succès",
        'analysis_complete': "🎯 Analyse terminée avec succès",
        'api_test_success': "✅ Test de connexion API réussi"
    }
    
    @classmethod
    def get_api_key(cls) -> str:
        """Récupère la clé API depuis les variables d'environnement."""
        return os.getenv('OPENROUTER_API_KEY', '')
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """Retourne la configuration du modèle IA."""
        return {
            'model': cls.DEFAULT_MODEL,
            'temperature': cls.DEFAULT_TEMPERATURE,
            'max_tokens': cls.MAX_TOKENS,
            'top_p': cls.TOP_P
        }
    
    @classmethod
    def get_app_config(cls) -> Dict[str, Any]:
        """Retourne la configuration générale de l'application."""
        return {
            'title': cls.APP_TITLE,
            'description': cls.APP_DESCRIPTION,
            'version': cls.VERSION,
            'max_file_size': cls.MAX_FILE_SIZE,
            'supported_formats': cls.SUPPORTED_FILE_TYPES
        }