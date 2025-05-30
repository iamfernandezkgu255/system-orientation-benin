# 🎓 Système d'Aide à l'Orientation Professionnelle IA pour le Bénin

Une application web développée en Python avec Streamlit qui aide les chefs d'établissements scolaires au Bénin à guider leurs élèves/étudiants dans leurs choix de carrière en utilisant l'intelligence artificielle.

## 📋 Description

Cette application analyse le profil des étudiants (filière actuelle, carrière envisagée) et le confronte aux réalités du marché du travail béninois pour proposer :
- Une évaluation du choix de carrière initial
- Un niveau d'adéquation avec la filière actuelle
- Des suggestions de carrières alternatives si pertinent
- Un parcours personnalisé détaillé

## 🚀 Fonctionnalités

- **Interface utilisateur intuitive** avec Streamlit
- **Analyse de fichiers** Excel (.xlsx) et Word (.docx)
- **Intelligence artificielle** via l'API DeepSeek (OpenRouter)
- **Base de connaissances** adaptée au marché béninois
- **Recommandations personnalisées** pour chaque étudiant
- **Export des résultats** en format JSON

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- Une clé API OpenRouter (obtenez-la sur [openrouter.ai](https://openrouter.ai))

### Étapes d'installation

1. **Cloner ou télécharger le projet**
```bash
git clone <url-du-repository>
cd systeme-orientation-benin
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer la base de connaissances**
   - Le fichier `knowledge_base_benin.json` doit être présent dans le répertoire racine
   - Un exemple est fourni, vous devez l'adapter avec vos données spécifiques

4. **Lancer l'application**
```bash
streamlit run app.py
```

## 📊 Structure des Fichiers

```
systeme-orientation-benin/
├── app.py                          # Application Streamlit principale
├── file_parser.py                  # Module de parsing des fichiers
├── knowledge_base_manager.py       # Gestionnaire de base de connaissances
├── recommendation_engine.py        # Moteur de recommandation IA
├── config.py                      # Configuration de l'application
├── requirements.txt               # Dépendances Python
├── knowledge_base_benin.json      # Base de données du marché béninois
└── README.md                      # Ce fichier
```

## 🗂️ Format des Fichiers Étudiants

### Fichier Excel (.xlsx)
Le fichier doit contenir les colonnes suivantes :
- **Nom** : Nom de famille de l'étudiant
- **Prénom** : Prénom de l'étudiant
- **Date de Naissance** : Date de naissance
- **Lieu de Naissance** : Lieu de naissance
- **Filière Actuelle** : Filière d'études actuelle
- **Carrière Envisagée** : Métier/carrière souhaité(e)

### Fichier Word (.docx)
Deux formats supportés :
1. **Tableau** : Même structure que l'Excel
2. **Texte libre** avec format :
```
Nom: John Doe
Prénom: Jane
Date de Naissance: 01/01/2000
Lieu de Naissance: Cotonou
Filière Actuelle: Informatique
Carrière Envisagée: Développeur Web

[Ligne vide pour séparer les étudiants]
```

## ⚙️ Configuration

### 1. Clé API OpenRouter
- Obtenez votre clé API sur [openrouter.ai](https://openrouter.ai)
- Entrez-la dans la barre latérale de l'application
- Ou définissez la variable d'environnement `OPENROUTER_API_KEY`

### 2. Base de Connaissances
Le fichier `knowledge_base_benin.json` contient :
- **Métiers** : Descriptions, compétences requises, formations, demande du marché
- **Secteurs porteurs** : Secteurs d'activité en croissance au Bénin
- **Compétences** : Compétences techniques et transversales
- **Formations** : Formations disponibles et institutions

#### Structure d'un métier :
```json
{
  "nom_metier": "Développeur Web et Mobile",
  "description": "Conçoit, développe et maintient des sites web...",
  "secteur_activite": "Numérique",
  "competences_requises_techniques": ["HTML/CSS", "JavaScript", "Python"],
  "competences_requises_transversales": ["Résolution de problèmes", "Travail d'équipe"],
  "formations_typiques": ["Licence en Informatique", "Bootcamp de programmation"],
  "niveau_demande_marche": "élevé",
  "perspectives_croissance": true,
  "pertinence_realites_africaines_benin": "Secteur en forte croissance..."
}
```

## 🔧 Utilisation

1. **Démarrage** : Lancez l'application avec `streamlit run app.py`
2. **Configuration** : Entrez votre clé API OpenRouter dans la barre latérale
3. **Téléversement** : Chargez votre fichier d'étudiants (.xlsx ou .docx)
4. **Analyse** : L'application traite automatiquement chaque étudiant
5. **Résultats** : Consultez les recommandations détaillées pour chaque étudiant
6. **Export** : Téléchargez le rapport complet en JSON

## 🎯 Fonctionnement de l'IA

L'application utilise le modèle DeepSeek via OpenRouter pour :
1. **Analyser** l'adéquation filière-métier envisagé
2. **Évaluer** les opportunités et défis potentiels
3. **Suggérer** des carrières alternatives si nécessaire
4. **Proposer** un parcours personnalisé avec :
   - Formations complémentaires
   - Compétences à développer
   - Certifications utiles
   - Conseils d'insertion professionnelle
   - Opportunités d'entrepreneuriat

## 📈 Secteurs Couverts

- **Numérique** : Développement web, cybersécurité, data science
- **Agro-industrie** : Agriculture durable, transformation alimentaire
- **Économie Verte** : Énergies renouvelables, gestion environnementale
- **Tourisme** : Guide touristique, hôtellerie, événementiel
- **Maintenance** : Maintenance industrielle, électrotechnique
- **BTP** : Construction, génie civil, architecture

## ⚠️ Prérequis Techniques

- **Python 3.8+** recommandé
- **Connexion Internet** pour l'API DeepSeek
- **Mémoire** : 512 MB minimum
- **Stockage** : 100 MB d'espace libre

## 🔒 Sécurité et Confidentialité

- Les clés API ne sont jamais stockées de façon permanente
- Les données des étudiants ne sont pas conservées après la session
- Toutes les communications avec l'API sont chiffrées (HTTPS)
- Respect du RGPD pour le traitement des données personnelles

## 🐛 Résolution de Problèmes

### Erreurs courantes :

**"Base de connaissances non trouvée"**
- Vérifiez que `knowledge_base_benin.json` est dans le répertoire racine
- Vérifiez la syntaxe JSON du fichier

**"Erreur API"**
- Vérifiez votre clé API OpenRouter
- Contrôlez votre connexion Internet
- Vérifiez les quotas de votre compte OpenRouter

**"Erreur de parsing"**
- Vérifiez le format de votre fichier étudiant
- Assurez-vous que toutes les colonnes requises sont présentes
- Vérifiez l'encodage du fichier (UTF-8 recommandé)

## 📞 Support

Pour toute question ou problème :
1. Vérifiez cette documentation
2. Consultez les logs de l'application
3. Vérifiez les prérequis et la configuration

## 🚀 Déploiement

### Streamlit Community Cloud
1. Forkez le repository sur GitHub
2. Connectez-vous à [share.streamlit.io](https://share.streamlit.io)
3. Déployez directement depuis votre repository
4. Configurez les secrets pour la clé API

### Déploiement Local
```bash
streamlit run app.py 
```

## 📝 Licence

Ce projet est développé pour l'éducation et l'orientation professionnelle au Bénin.

## 🤝 Contribution

Contributions bienvenues pour :
- Enrichir la base de connaissances béninoise
- Améliorer l'interface utilisateur
- Ajouter de nouvelles fonctionnalités
- Corriger les bugs

---

**Développé avec ❤️ pour l'avenir des étudiants béninois**