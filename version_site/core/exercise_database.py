"""
Base de données centralisée de tous les exercices
Chaque exercice est défini une seule fois avec toutes ses propriétés
"""

EXERCISE_DATABASE = {
    # PUSH - Horizontal Push (Chest)
    "Bench press": {
        "name": "Bench press",
        "category": "push",
        "pattern": "Horizontal Push (Chest)",
        "type": "polyarticulaire",
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Triceps", "Epaules"],
        "all_muscles": ["Pectoraux", "Triceps", "Epaules"],
        "equipment": "Barbell",
        "difficulty": "intermediate",
    "image_path": "images/jpg2png-2/bench1.png"
    },
    
    "Dips": {
        "name": "Dips",
        "category": "push", 
        "pattern": "Horizontal Push (Chest)",
        "type": "polyarticulaire",
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Triceps", "Epaules"],
        "all_muscles": ["Pectoraux", "Triceps", "Epaules"],
        "equipment": "Bodyweight",
        "difficulty": "intermediate",
    "image_path": "images/jpg2png-2/dips.png"
    },
    
    "Chest Press": {
        "name": "Chest Press",
        "category": "push",
        "pattern": "Horizontal Push (Chest)",
        "type": "polyarticulaire",
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Triceps", "Epaules"],
        "all_muscles": ["Pectoraux", "Triceps", "Epaules"],
        "equipment": "Chest Press Machine",
        "image_path": "exercices2/machine-chest-press-resized.png.webp"
    },
    "Push ups": {
        "name": "Push ups",
        "category": "push",
        "pattern": "Horizontal Push (Chest)",
        "type": "polyarticulaire",
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Triceps", "Epaules"],
        "all_muscles": ["Pectoraux", "Triceps", "Epaules"],
        "equipment": "Bodyweight",
        "image_path": "exercices2/pushups.png"
    },
    "Dumbell Bench Press": {
        "name": "Dumbell Bench Press",
        "category": "push",
        "pattern": "Horizontal Push (Chest)",
        "type": "polyarticulaire",
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Triceps", "Epaules"],
        "all_muscles": ["Pectoraux", "Triceps", "Epaules"],
        "equipment": "Dumbells",
        "image_path": "exercices2/dumbell_bench_press.png"
    },

    # PUSH - Vertical Push
    "Overhead press": {
        "name": "Overhead press",
        "category": "push",
        "pattern": "Vertical Push", 
        "type": "polyarticulaire",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": ["Triceps"],
        "all_muscles": ["Epaules", "Triceps"],
        "equipment": "Barbell",
    "image_path": "images/jpg2png-2/jpg2png-3/overheadpress1.png"
    },

    "Machine Overhead press": {
        "name": "Machine Overhead press",
        "category": "push",
        "pattern": "Vertical Push", 
        "type": "polyarticulaire",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": ["Triceps"],
        "all_muscles": ["Epaules", "Triceps"],
        "equipment": "Overhead Press Machine",
    "image_path": "exercices2/lever-seated-shoulder-press.webp"
    },

    "Seated Dumbell Overhead press": {
        "name": "Seated Dumbell Overhead press",
        "category": "push",
        "pattern": "Vertical Push", 
        "type": "polyarticulaire",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": ["Triceps"],
        "all_muscles": ["Epaules", "Triceps"],
        "equipment": ["Dumbells","Bench"],
    "image_path": "exercices2/dumbell_bench_press.png"
    },
    
    "Incline press": {
        "name": "Incline press",
        "category": "push",
        "pattern": "Incline Push",
        "type": "polyarticulaire", 
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Epaules", "Triceps"],
        "all_muscles": ["Pectoraux", "Epaules", "Triceps"],
        "equipment": "Barbell",
    "image_path": "images/jpg2png-2/incline_press_1.png"
    },
    
    # PUSH - Isolations
    "Lateral raises": {
        "name": "Lateral raises",
        "category": "push",
        "pattern": "Side Raise",
        "type": "isolation",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": ["Trapèzes"],
        "all_muscles": ["Epaules", "Trapèzes"],
        "equipment": "Dumbbells",
    "image_path": "images/jpg2png-2/jpg2png-3/lateral raises.png"
    },
    
    "Cable Lateral raises": {
        "name": "Lateral raises",
        "category": "push",
        "pattern": "Side Raise",
        "type": "isolation",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": ["Trapèzes"],
        "all_muscles": ["Epaules", "Trapèzes"],
        "equipment": "cable station",
    "image_path": "exercices2/cable_lr.png"
    },
    
    "Y raise": {
        "name": "Y raise",
        "category": "push",
        "pattern": "Frontal Raise",
        "type": "isolation",
        "primary_muscles": ["Epaules", "Trapèzes"],
        "secondary_muscles": [],
        "all_muscles": ["Epaules", "Trapèzes"],
        "equipment": ["Dumbbells", "Bench"],
    "image_path": "exercices2/Y_raise.png"
    },
    

    "Front raise": {
        "name": "Front raise", 
        "category": "push",
        "pattern": "Frontal Raise",
        "type": "isolation",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": ["Pectoraux"],
        "all_muscles": ["Epaules", "Pectoraux"],
        "equipment": "Dumbbells", 
    "image_path": "images/jpg2png-2/front raises.png"
    },
    
    "Rear delt fly": {
        "name": "Rear delt fly",
        "category": "push", 
        "pattern": "Rear Delt",
        "type": "isolation",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": [],
        "all_muscles": ["Epaules"],
        "equipment": "Dumbbells", 
    "image_path": "images/jpg2png-2/jpg2png-3/rear delt fly.png"
    },

    "Face pulls": {
        "name": "Face pulls",
        "category": "pull", 
        "pattern": "Rear Delt",
        "type": "isolation",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": ["Trapèzes"],
        "all_muscles": ["Epaules", "Trapèzes"],
        "equipment": "cable station", 
    "image_path": "exercices2/face_pull.png"
    },
    
    
    "Pushdown": {
        "name": "Pushdown",
        "category": "push",
        "pattern": "Tricep Extension", 
        "type": "isolation",
        "primary_muscles": ["Triceps"],
        "secondary_muscles": [],
        "all_muscles": ["Triceps"],
        "equipment": "Cable",
    "image_path": "images/jpg2png-2/jpg2png-3/pushdown.png"
    },

    "Skull crushers": {
        "name": "Skull crushers",
        "category": "push",
        "pattern": "Tricep Extension", 
        "type": "isolation",
        "primary_muscles": ["Triceps"],
        "secondary_muscles": [],
        "all_muscles": ["Triceps"],
        "equipment": ["Bench", "Dumbbels"],
    "image_path": "exercices2/skull_crusher.png"
    },
    
    "Tricep extension": {
        "name": "Tricep extension",
        "category": "push",
        "pattern": "Tricep Extension",
        "type": "isolation", 
        "primary_muscles": ["Triceps"],
        "secondary_muscles": [],
        "all_muscles": ["Triceps"],
        "equipment": "Dumbbells",
    "image_path": "images/jpg2png-2/extension tricep.png"
    },
    
    # PULL - Horizontal Pull
    "Bent over row": {
        "name": "Bent over row",
        "category": "pull",
        "pattern": "Horizontal Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps", "Epaules"],
        "all_muscles": ["Dorsaux", "Biceps", "Epaules"],
        "equipment": "Barbell", 
    "image_path": "images/jpg2png-2/bent_over_row_1.png"
    },
    
    "Machine row": {
        "name": "Machine row",
        "category": "pull",
        "pattern": "Horizontal Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps"],
        "all_muscles": ["Dorsaux", "Biceps"],
        "equipment": "Machine",
    "image_path": "images/jpg2png-2/jpg2png-3/machine row.png"
    },
    
    # PULL - Vertical Pull  
    "Pull up": {
        "name": "Pull up",
        "category": "pull",
        "pattern": "Vertical Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps"],
        "all_muscles": ["Dorsaux", "Biceps"],
        "equipment": "Bodyweight",
    "image_path": "images/jpg2png-2/jpg2png-3/pull_up_1.png"
    },

    "Lat Pulldown": {
        "name": "Lat Pulldown",
        "category": "pull",
        "pattern": "Vertical Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps"],
        "all_muscles": ["Dorsaux", "Biceps"],
        "equipment": "Lat Pulldown Machine",
    "image_path": "exercices2/lat_pulldown.png"
    },
    
    "Chin up": {
        "name": "Chin up", 
        "category": "pull",
        "pattern": "Vertical Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps"],
        "all_muscles": ["Dorsaux", "Biceps"],
        "equipment": "Bodyweight",
    "image_path": "images/jpg2png-2/chin_up_1.png"
    },
    
    # PULL - Isolations
    "Curl": {
        "name": "Curl",
        "category": "pull",
        "pattern": "Bicep Curl",
        "type": "isolation",
        "primary_muscles": ["Biceps"],
        "secondary_muscles": [],
        "all_muscles": ["Biceps"],
        "equipment": "Dumbbells",
    "image_path": "images/jpg2png-2/curl.png"
    },
    
    "Cable Curl": {
        "name": "Cable Curl",
        "category": "pull",
        "pattern": "Bicep Curl",
        "type": "isolation",
        "primary_muscles": ["Biceps"],
        "secondary_muscles": [],
        "all_muscles": ["Biceps"],
        "equipment": "Cable station",
    "image_path": "exercices2/cable_curl.png"
    },

    "Hammer curl": {
        "name": "Hammer curl",
        "category": "pull", 
        "pattern": "Bicep Curl",
        "type": "isolation",
        "primary_muscles": ["Biceps"],
        "secondary_muscles": [],
        "all_muscles": ["Biceps"],
        "equipment": "Dumbbells",
    "image_path": "images/jpg2png-2/hammercurl.png"
    },
    
    "Preacher curl": {
        "name": "Preacher curl",
        "category": "pull",
        "pattern": "Bicep Curl",
        "type": "isolation",
        "primary_muscles": ["Biceps"],
        "secondary_muscles": [],
        "all_muscles": ["Biceps"],
        "equipment": "Barbell", 
    "image_path": "images/jpg2png-2/jpg2png-3/preachercurl.png"
    },
    
    # LEGS - Squat Pattern
    "Barbell squat": {
        "name": "Barbell squat",
        "category": "legs",
        "pattern": "Squat",
        "type": "polyarticulaire",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": ["Fessiers", "Lombaires"],
        "all_muscles": ["Quadriceps", "Fessiers", "Lombaires"],
        "equipment": "Barbell",
    "image_path": "images/jpg2png-2/barbell_squat_1.png"
    },

    "Hack squat": {
        "name": "Hack squat",
        "category": "legs",
        "pattern": "Squat",
        "type": "polyarticulaire",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": ["Fessiers"],
        "all_muscles": ["Quadriceps", "Fessiers"],
        "equipment": "Hack squat machine",
    "image_path": "exercices2/hack_squat.png"
    },
    
    "Bulgarian split squat": {
        "name": "Bulgarian split squat",
        "category": "legs",
        "pattern": "Single Leg", 
        "type": "polyarticulaire",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": ["Fessiers"],
        "all_muscles": ["Quadriceps", "Fessiers"],
        "equipment": ["Bodyweight" "Dumbbels"],
    "image_path": "images/jpg2png-2/bulgarian_split_squat_1.png"
    },
    
    # LEGS - Hip Hinge Pattern
    "Stiff leg deadlift": {
        "name": "Stiff leg deadlift",
        "category": "legs",
        "pattern": "Hip Hinge",
        "type": "polyarticulaire", 
        "primary_muscles": ["Isquios-jambiers"],
        "secondary_muscles": ["Fessiers", "Lombaires"],
        "all_muscles": ["Isquios-jambiers", "Fessiers", "Lombaires"],
        "equipment": "Barbell",
    "image_path": "images/jpg2png-2/jpg2png-3/SLDL_1.png"
    },
    
    "Back hyperextension": {
        "name": "Back hyperextension",
        "category": "legs",
        "pattern": "Hip Hinge",
        "type": "isolation",
        "primary_muscles": ["Lombaires"],
        "secondary_muscles": ["Isquios-jambiers", "Fessiers"],
        "all_muscles": ["Lombaires", "Isquios-jambiers", "Fessiers"],
        "equipment": "Machine",
    "image_path": "images/jpg2png-2/back_hyper.png"
    },
    
    # LEGS - Isolations
    "Leg extension": {
        "name": "Leg extension",
        "category": "legs",
        "pattern": "Leg Extension",
        "type": "isolation",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": [],
        "all_muscles": ["Quadriceps"],
        "equipment": "Machine",
    "image_path": "images/jpg2png-2/jpg2png-3/legextension.png"
    },
    
    "Sissy squat": {
        "name": "Sissy squat",
        "category": "legs", 
        "pattern": "Leg Extension",
        "type": "isolation",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": [],
        "all_muscles": ["Quadriceps"],
        "equipment": "Bodyweight",
    "image_path": "images/jpg2png-2/jpg2png-3/sissysquat.png"
    },
    
    "Seated leg curl": {
        "name": "Seated leg curl",
        "category": "legs",
        "pattern": "Leg Curl",
        "type": "isolation",
        "primary_muscles": ["Isquios-jambiers"],
        "secondary_muscles": [],
        "all_muscles": ["Isquios-jambiers"],
        "equipment": "Machine", 
    "image_path": "images/jpg2png-2/jpg2png-3/seatedlegcurl.png"
    },
    
    "Nordic curl": {
        "name": "Nordic curl",
        "category": "legs",
        "pattern": "Leg Curl", 
        "type": "isolation",
        "primary_muscles": ["Isquios-jambiers"],
        "secondary_muscles": [],
        "all_muscles": ["Isquios-jambiers"],
        "equipment": "Bodyweight",
    "image_path": "images/jpg2png-2/jpg2png-3/nordic_curl.png"
    },
    
    # CORE - Abdominaux (tous isolations)
    "Machine ab crunch": {
        "name": "Machine ab crunch",
        "category": "core",
        "pattern": "Abs",
        "type": "isolation",
        "primary_muscles": ["Abdominaux"],
        "secondary_muscles": [],
        "all_muscles": ["Abdominaux"],
        "equipment": "Machine",
    "image_path": "images/jpg2png-2/jpg2png-3/machinecrunch.png"
    },
    
    "Hanging leg raises": {
        "name": "Hanging leg raises",
        "category": "core",
        "pattern": "Abs",
        "type": "isolation",
        "primary_muscles": ["Abdominaux"],
        "secondary_muscles": [],
        "all_muscles": ["Abdominaux"],
        "equipment": "Bodyweight", 
    "image_path": "images/jpg2png-2/hanginglegraises.png"
    }
}

def get_exercise_info(exercise_name):
    """Récupère toutes les informations d'un exercice"""
    return EXERCISE_DATABASE.get(exercise_name, None)

def get_all_exercises():
    """Récupère tous les noms d'exercices"""
    return list(EXERCISE_DATABASE.keys())

def get_exercises_by_category(category):
    """Récupère tous les exercices d'une catégorie (push, pull, legs, core)"""
    return [name for name, info in EXERCISE_DATABASE.items() if info["category"] == category]

def get_exercises_by_type(exercise_type):
    """Récupère tous les exercices d'un type (polyarticulaire, isolation)"""
    return [name for name, info in EXERCISE_DATABASE.items() if info["type"] == exercise_type]

def get_exercises_by_pattern(pattern):
    """Récupère tous les exercices d'un pattern donné"""
    return [name for name, info in EXERCISE_DATABASE.items() if info["pattern"] == pattern]

def get_exercises_by_muscle(muscle):
    """Récupère tous les exercices qui travaillent un muscle donné"""
    return [name for name, info in EXERCISE_DATABASE.items() if muscle in info["all_muscles"]]

def is_polyarticular(exercise_name):
    """Vérifie si un exercice est polyarticulaire"""
    info = get_exercise_info(exercise_name)
    return info["type"] == "polyarticulaire" if info else False

def is_isolation(exercise_name):
    """Vérifie si un exercice est d'isolation"""
    info = get_exercise_info(exercise_name)  
    return info["type"] == "isolation" if info else False

# Métadonnées des muscles (centralisées)
MUSCLE_INFO = {
    "Pectoraux": {
        "name": "Pectoraux",
        "category": "upper",
        "description": "Muscles de la poitrine",
        "primary_functions": ["Poussée horizontale", "Adduction bras"],
    "image_path": "images/jpg2png/pec1.png"
    },
    "Epaules": {
        "name": "Epaules",
        "category": "upper", 
        "description": "Deltoïdes antérieur, moyen et postérieur",
        "primary_functions": ["Poussée verticale", "Élévations"],
    "image_path": "images/jpg2png/epaule1.png"
    },
    "Dorsaux": {
        "name": "Dorsaux",
        "category": "upper",
        "description": "Grand dorsal et rhomboïdes",
        "primary_functions": ["Tirage vertical", "Tirage horizontal"],
    "image_path": "images/lat1.png"
    },
    "Biceps": {
        "name": "Biceps",
        "category": "upper",
        "description": "Biceps brachial",
        "primary_functions": ["Flexion coude", "Supination"],
    "image_path": "images/biceps.png"
    },
    "Triceps": {
        "name": "Triceps", 
        "category": "upper",
        "description": "Triceps brachial",
        "primary_functions": ["Extension coude"],
    "image_path": "images/jpg2png/tricep1.png"
    },
    "Abdominaux": {
        "name": "Abdominaux",
        "category": "core",
        "description": "Grand droit et obliques",
        "primary_functions": ["Flexion tronc", "Stabilisation"],
    "image_path": "images/jpg2png/ab1.png"
    },
    "Quadriceps": {
        "name": "Quadriceps",
        "category": "lower",
        "description": "4 muscles avant de la cuisse",
        "primary_functions": ["Extension genou", "Flexion hanche"],
    "image_path": "images/jpg2png/quad1.png"
    },
    "Isquios-jambiers": {
        "name": "Isquios-jambiers",
        "category": "lower",
        "description": "Muscles arrière de la cuisse", 
        "primary_functions": ["Flexion genou", "Extension hanche"],
    "image_path": "images/jpg2png/ham1.png"
    },
    "Fessiers": {
        "name": "Fessiers",
        "category": "lower",
        "description": "Grand, moyen et petit fessier",
        "primary_functions": ["Extension hanche", "Abduction"],
    "image_path": "images/jpg2png/glute1.png"
    },
    "Lombaires": {
        "name": "Lombaires",
        "category": "lower",
        "description": "Erecteurs du rachis",
        "primary_functions": ["Extension dos", "Stabilisation"],
    "image_path": "images/jpg2png/lb1.png"
    }
}

def get_muscle_info(muscle_name):
    """Récupère les informations d'un muscle"""
    return MUSCLE_INFO.get(muscle_name, None)

def get_all_muscles():
    """Récupère tous les noms de muscles"""
    return list(MUSCLE_INFO.keys())

def get_muscles_by_category(category):
    """Récupère les muscles par catégorie (upper, lower, core)"""
    return [name for name, info in MUSCLE_INFO.items() if info["category"] == category]

# Objectifs de volume centralisés
VOLUME_TARGETS = {
    "maintenance": {
        "description": "Maintien de la masse musculaire",
        "weekly_sets": [4, 5, 6],
        "recommended": 5
    },
    "normal_growth": {
        "description": "Croissance musculaire normale",
        "weekly_sets": [7, 8, 9, 10],
        "recommended": 8
    },
    "prioritised_growth": {
        "description": "Croissance musculaire prioritaire",
        "weekly_sets": [11, 12, 13],
        "recommended": 12
    }
}

def get_volume_target(goal):
    """Récupère les informations d'un objectif de volume"""
    return VOLUME_TARGETS.get(goal, None)

def get_all_volume_goals():
    """Récupère tous les objectifs de volume disponibles"""
    return list(VOLUME_TARGETS.keys())

def get_muscle_list_with_images():
    """Génère la liste des muscles avec leurs images depuis la base centralisée"""
    return [(name, info["image_path"]) for name, info in MUSCLE_INFO.items()]

# Mapping des noms de patterns vers les noms d'interface
PATTERN_INTERFACE_NAMES = {
    "Horizontal Push (Chest)": "Press horizontale",
    "Vertical Push": "Press verticale",
    "Incline Push": "Press verticale", 
    "Horizontal Pull": "Tirage horizontal",
    "Vertical Pull": "Tirage vertical",
    "Squat": "Squat pattern",
    "Single Leg": "Squat pattern",
    "Hip Hinge": "Hinge pattern", 
    "Abs": "Spine flexion",
    "Leg Extension": "Quad iso",
    "Leg Curl": "Hamstring isolation",
    "Bicep Curl": "Bicep isolation",
    "Tricep Extension": "Tricep isolation",
    "Lateral Raise": "Delt isolation",
    "Rear Delt": "Delt isolation"
}

def get_interface_pattern_name(pattern):
    """Récupère le nom d'interface pour un pattern donné"""
    return PATTERN_INTERFACE_NAMES.get(pattern, pattern)

def get_pattern_list_for_interface():
    """Génère la liste des patterns groupés par nom d'interface"""
    patterns = {}
    
    # Grouper les exercices par pattern
    for exercise_name, exercise_info in EXERCISE_DATABASE.items():
        pattern = exercise_info["pattern"]
        if pattern not in patterns:
            patterns[pattern] = []
        patterns[pattern].append((exercise_name, exercise_info["image_path"]))
    
    # Regrouper par nom d'interface
    interface_patterns = {}
    for pattern, exercises in patterns.items():
        interface_name = get_interface_pattern_name(pattern)
        if interface_name not in interface_patterns:
            interface_patterns[interface_name] = []
        interface_patterns[interface_name].extend(exercises)
    
    return [(name, exercises) for name, exercises in interface_patterns.items() if exercises]