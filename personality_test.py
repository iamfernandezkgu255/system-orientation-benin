# personality_test.py

MBTI_QUESTIONS = {
    "EI": {
        "E": [
            "Vous êtes dynamique",
            "Vous aimez parler",
            "Vous pensez à voix haute",
            "Vous agissez, puis pensez",
            "Vous n'aimez pas être seul",
            "Vous aimez établir de nouveaux contacts",
            "Vous préférez parler plutôt qu'écrire",
            "Vous pouvez facilement être distrait",
            "Vous préférez faire plusieurs choses à la fois",
            "Vous avez parfois un discours changeant"
        ],
        "I": [
            "Vous êtes calme",
            "Vous aimez écouter",
            "Vous réfléchissez posément",
            "Vous pensez, puis agissez",
            "Vous vous sentez bien quand vous êtes seul",
            "Vous aimez approfondir vos contacts",
            "Vous êtes considéré comme plutôt secret et réservé",
            "Vous possédez une bonne capacité de concentration",
            "Vous préférez vous concentrer sur une seule chose à la fois",
            "Vous êtes indépendant"
        ]
    },
    "SN": {
        "S": [
            "Vous vous attachez aux faits et aux détails",
            "Vous aimez les choses utiles",
            "Vous vivez dans l'instant présent",
            "Vous faites confiance à l'expérience",
            "Vous aimez approfondir vos compétences",
            "Vous restez fidèle aux méthodes qui ont fait leurs preuves",
            "Vous préférez les instructions étape par étape",
            "Vous êtes pratique",
            "Vous aimez ce qui est concret, réel, directement observable",
            "Vous êtes réaliste : vous voyez ce qui existe"
        ],
        "N": [
            "Vous vous intéressez aux idées",
            "Vous remarquez tout ce qui est nouveau et différent",
            "Vous pensez aux implications futures",
            "Vous suivez votre instinct",
            "Vous aimez apprendre de nouvelles compétences",
            "Vous n'aimez pas la routine",
            "Vous cherchez à comprendre",
            "Vous êtes théorique",
            "Vous êtes attirés par les idées originales",
            "Vous êtes imaginatifs : vous voyez les possibilités"
        ]
    },
    "TF": {
        "T": [
            "Vous vous efforcez d'être objectif dans vos décisions",
            "Vous apparaissez calme et réservé",
            "Vous avez un sens aigu de la justice",
            "Vous vous impliquez peu, vous prenez de la distance",
            "Vous êtes critique (vous remarquez vite les failles et les défauts)",
            "Vous adorez argumenter pour le plaisir",
            "Vous êtes franc et direct",
            "Vous êtes motivé par vos projets",
            "Vous aimez vous placer en observateur",
            "Vous êtes sensible à la logique"
        ],
        "F": [
            "Vous fondez vos décisions sur vos valeurs et vos sentiments",
            "Vous êtes sociable et amical",
            "Vous avez tendance à la clémence",
            "Vous prenez les choses à cœur",
            "Vous tentez de faire plaisir (prompt à faire des compliments)",
            "Vous évitez la discussion et le conflit",
            "Vous êtes diplomate et faîtes preuve de tact",
            "Vous êtes motivé par l'estime des autres",
            "Vous êtes sensible (facilement blessé)",
            "Vous faîtes confiance à vos impressions"
        ]
    },
    "JP": {
        "J": [
            "Vous aimez organiser et planifier",
            "Vous êtes sérieux et conventionnel",
            "Vous suivez votre calendrier et êtes parfaitement ponctuel",
            "Vous aimez terminer vos projets",
            "Vous travaillez d'abord, vous vous amusez ensuite",
            "Vous n'aimez pas le stress de dernière minute",
            "Vous ne discutez pas les règles",
            "Vous cherchez à maîtriser",
            "Vous êtes à l'aise au sein de structures bien définies",
            "Vous n'aimez pas le provisoire, l'incertain"
        ],
        "P": [
            "Vous aimez vivre de façon flexible",
            "Vous êtes ludique et non-conventionnel",
            "Vous n'avez ni heure ni délais",
            "Vous aimez démarrer des projets",
            "Vous vous amusez d'abord et travaillez ensuite",
            "Vous rechignez à vous engager",
            "Vous discutez les règles",
            "Vous cherchez à comprendre",
            "Vous aimez conserver votre liberté d'action",
            "Vous restez ouvert, aimez vivre des expériences, vous adapter"
        ]
    }
}

MBTI_DESCRIPTIONS = {
    "ISTJ": {
        "title": "ISTJ - Le Contrôleur",
        "group": "Les Gardiens (SJ)",
        "summary": "Sérieux, réservé, et factuel (S). Il est logique, méthodique et responsable (T). Il valorise la tradition, l'ordre et la précision, et s'assure que les choses sont faites correctement et dans les règles (J)."
    },
    "ISFJ": {
        "title": "ISFJ - Le Protecteur",
        "group": "Les Gardiens (SJ)",
        "summary": "Dévoué, calme (I), et méticuleux (S). Il est loyal, fiable et profondément attentionné aux sentiments des autres (F). Il apprécie la structure et la tradition (J) et travaille en coulisses pour assurer le bien-être de son entourage."
    },
    "INFJ": {
        "title": "INFJ - Le Conseiller",
        "group": "Les Idéalistes (NF)",
        "summary": "Perspicace, réservé (I), et orienté vers les possibilités et le sens profond (N). Il est profondément empathique et dévoué à aider les autres (F). Il est déterminé, organisé dans sa quête d'idéaux et de visions à long terme (J)."
    },
    "INTJ": {
        "title": "INTJ - Le Cerveau (ou Architecte)",
        "group": "Les Rationnels (NT)",
        "summary": "Indépendant, conceptuel (I), et visionnaire (N). Il est très logique, analytique et critique (T). Il est un excellent stratège, planificateur à long terme et déterminé à mettre en œuvre ses idées (J)."
    },
    "ISTP": {
        "title": "ISTP - L'Artisan",
        "group": "Les Artisans (SP)",
        "summary": "Observateur, calme (I), et très doué pour comprendre comment les choses fonctionnent (S). Il est logique, analytique et excellent pour le dépannage et la résolution de problèmes concrets (T). Il est flexible, indépendant et aime l'action pratique (P)."
    },
    "ISFP": {
        "title": "ISFP - Le Compositeur",
        "group": "Les Artisans (SP)",
        "summary": "Doux, sensible (I), et très attentif à son environnement et à l'esthétique (S). Il est guidé par ses valeurs profondes et son désir d'harmonie (F). Il est flexible, adaptable et préfère s'exprimer par des actions concrètes plutôt que par des mots (P)."
    },
    "INFP": {
        "title": "INFP - Le Guérisseur (ou Médiateur)",
        "group": "Les Idéalistes (NF)",
        "summary": "Idéaliste, calme (I), et en quête de sens et d'authenticité (N). Il est profondément attaché à ses valeurs et à l'harmonie (F). Il est flexible, ouvert d'esprit et cherche à vivre en accord avec ses idéaux (P)."
    },
    "INTP": {
        "title": "INTP - L'Architecte (concepteur de systèmes)",
        "group": "Les Rationnels (NT)",
        "summary": "Analytique, réservé (I), et fasciné par les théories et les concepts complexes (N). Il est extrêmement logique, précis et cherche à comprendre le fonctionnement profond des choses (T). Il est flexible, curieux et aime explorer les idées pour elles-mêmes (P)."
    },
    "ESTP": {
        "title": "ESTP - L'Organisateur",
        "group": "Les Artisans (SP)",
        "summary": "Énergique, orienté vers l'action (E) et très pragmatique (S). Il est logique, direct et doué pour résoudre les problèmes de manière inventive (T). Il est adaptable, aime les défis et sait improviser (P)."
    },
    "ESFP": {
        "title": "ESFP - L'Artiste Interprète",
        "group": "Les Artisans (SP)",
        "summary": "Enthousiaste, sociable et plein de vie (E). Il aime l'action, vit dans l'instant présent (S) et est très sensible à l'ambiance et aux émotions (F). Il est flexible, spontané et aime divertir et engager les autres (P)."
    },
    "ENFP": {
        "title": "ENFP - Le Défenseur (Champion/Inspirateur)",
        "group": "Les Idéalistes (NF)",
        "summary": "Enthousiaste, créatif (E), et plein d'idées (N). Il est motivé par ses valeurs et son désir d'aider les autres à s'épanouir (F). Il est spontané, adaptable et aime explorer de nouvelles possibilités (P)."
    },
    "ENTP": {
        "title": "ENTP - L'Inventeur",
        "group": "Les Rationnels (NT)",
        "summary": "Ingénieux, curieux (E), et toujours à la recherche de nouvelles idées et possibilités (N). Il est logique, aime débattre et remettre en question le statu quo (T). Il est flexible, adaptable et aime explorer de multiples options (P)."
    },
    "ESTJ": {
        "title": "ESTJ - Le Superviseur",
        "group": "Les Gardiens (SJ)",
        "summary": "Pragmatique, direct (E), et réaliste (S). Il est logique, organisé et aime prendre des décisions basées sur des faits objectifs (T). Il est doué pour la gestion, l'application des règles et la mise en place de structures efficaces (J)."
    },
    "ESFJ": {
        "title": "ESFJ - Le Soutien",
        "group": "Les Gardiens (SJ)",
        "summary": "Chaleureux, sociable (E), pratique et attentif aux besoins concrets des autres (S). Il est guidé par ses valeurs et son empathie (F) et aime l'ordre et l'organisation pour apporter son aide (J). C'est une personne qui aime prendre soin des autres et maintenir l'harmonie."
    },
    "ENFJ": {
        "title": "ENFJ - Le Professeur",
        "group": "Les Idéalistes (NF)",
        "summary": "Charismatique, empathique (E), et visionnaire (N). Il est sensible aux besoins et motivations des autres (F) et aime les aider à atteindre leur potentiel. Il est organisé et doué pour mobiliser les gens autour d'une cause commune (J)."
    },
    "ENTJ": {
        "title": "ENTJ - Le Maréchal (ou Commandant)",
        "group": "Les Rationnels (NT)",
        "summary": "Assertif, visionnaire (E), et stratégique (N). Il est logique, décidé et doué pour diriger et organiser des systèmes complexes (T). Il est un leader naturel, planificateur et orienté vers les objectifs (J)."
    }
}

MBTI_EXPLANATIONS = {
    "E": {"label": "Extraverti", "description": "Vous puisez votre énergie de l'environnement extérieur, les gens, les activités et les expériences. Vous êtes plutôt actif et expressif. [ACTION]"},
    "I": {"label": "Introverti", "description": "Vous puisez votre énergie de l'univers intérieur des idées, des souvenirs, des pensées et des émotions. Vous êtes plutôt réfléchi et réservé. [REFLEXION]"},
    "S": {"label": "Sensation", "description": "Vous remarquez les faits, les détails et les réalités du monde qui vous entoure. Vous recueillez des informations concrètes et tangibles. Vous êtes plutôt terre-à-terre. [PRESENT]"},
    "N": {"label": "Intuition", "description": "Vous abordez les données dans leur globalité et vous êtes davantage intéressé par leur sens, les relations entre les choses, et les possibilités, au-delà des faits directement observables. Vous recueillez des informations abstraites et intangibles. Vous êtes plutôt imaginatif. [FUTUR]"},
    "T": {"label": "Pensée", "description": "Vous prenez des décisions en vous basant sur des critères objectifs et impersonnels. Vous êtes logique. Vous recherchez la Vérité. [RAISON]"},
    "F": {"label": "Sentiment", "description": "Vous prenez des décisions en tenant compte de vos valeurs et de vos impressions personnelles. Vous êtes sensible. Vous recherchez l'Harmonie. [EMPATHIE]"},
    "J": {"label": "Jugement", "description": "Vous préférez vivre dans un environnement structuré, ordonné et prévisible, que vous pouvez contrôler. Vous êtes plutôt organisé et formel. [ORGANISATION]"},
    "P": {"label": "Perception", "description": "Vous préférez expérimenter autant que possible, vous êtes donc très ouverts aux changements. Vous êtes plutôt flexible, curieux et non conformiste. [ADAPTATION]"}
}

def calculate_mbti_profile(answers: dict) -> str:
    """
    Calcule le profil MBTI à partir des réponses.
    answers est un dictionnaire comme: {'EI': {'E': score, 'I': score}, ...}
    Retourne une chaîne de 4 lettres, ex: "INTP".
    """
    profile = ""
    if not answers:
        return "----"

    # Calcul pour E/I
    e_score = answers.get("EI", {}).get("E", 0)
    i_score = answers.get("EI", {}).get("I", 0)
    profile += "E" if e_score > i_score else "I"

    # Calcul pour S/N
    s_score = answers.get("SN", {}).get("S", 0)
    n_score = answers.get("SN", {}).get("N", 0)
    profile += "S" if s_score > n_score else "N"

    # Calcul pour T/F
    t_score = answers.get("TF", {}).get("T", 0)
    f_score = answers.get("TF", {}).get("F", 0)
    profile += "T" if t_score > f_score else "F"

    # Calcul pour J/P
    j_score = answers.get("JP", {}).get("J", 0)
    p_score = answers.get("JP", {}).get("P", 0)
    profile += "J" if j_score > p_score else "P"

    return profile

def get_mbti_description(profile_code: str) -> dict:
    """
    Retourne la description d'un profil MBTI.
    """
    return MBTI_DESCRIPTIONS.get(profile_code, {})

def get_mbti_explanations_for_profile(profile_code: str) -> dict:
    """
    Retourne les explications pour chaque lettre du profil MBTI.
    """
    if not profile_code or len(profile_code) != 4:
        return {}

    explanations = {
        "EI": MBTI_EXPLANATIONS.get(profile_code[0]),
        "SN": MBTI_EXPLANATIONS.get(profile_code[1]),
        "TF": MBTI_EXPLANATIONS.get(profile_code[2]),
        "JP": MBTI_EXPLANATIONS.get(profile_code[3]),
    }
    return explanations
