"""
Générateur de programme d'entraînement basé sur une philosophie stricte :
1. Split selon jours : 2-3j=Full Body, 4-5j=Upper/Lower, 6j=Push/Pull/Legs
2. Volume hebdomadaire exact selon priorité et niveau (débutant vs avancé)
3. Les exercices peuvent être répétés plusieurs fois/semaine pour atteindre le volume
4. Le volume total est identique quel que soit le nb de jours (dépend uniquement du choix utilisateur)
5. Exercices répartis par ordre de priorité (polyarticulaires en premier)
6. Volume réparti uniformément entre les séances
7. Full Body : seulement UN tirage OU UN push par séance (pas horiz + vert)
8. N'utiliser que les exercices nécessaires pour atteindre le volume
"""
from version_site.core.exercise_database import get_exercise_info


# Volumes d'entraînement hebdomadaires selon objectif et niveau
VOLUME_OBJECTIFS = {
    "beginner": {
        "maintenance": [3],
        "normal_growth": [6],
        "prioritised_growth": [9]
    },
    "advanced": {
        "maintenance": [4, 5, 6],
        "normal_growth": [7, 8, 9, 10],
        "prioritised_growth": [11, 12, 13]
    }
}


class Split:
    """Définit les splits d'entraînement"""
    def __init__(self, name, sessions):
        self.name = name
        self.sessions = sessions


def create_prog(nb_jours):
    """Crée le split approprié selon le nombre de jours"""
    if nb_jours in [2, 3]:
        return Split("Full Body", {
            "session_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                         "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "session_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                         "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "session_C": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                         "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
        })
    elif nb_jours in [4, 5]:
        return Split("Upper/Lower", {
            "upper_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
            "lower_A": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "upper_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
            "lower_B": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
        })
    elif nb_jours == 6:
        return Split("Push/Pull/Legs", {
            "push_A": ["Pectoraux", "Epaules", "Triceps", "Abdominaux"],
            "pull_A": ["Dorsaux", "Biceps"],
            "legs_A": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "push_B": ["Pectoraux", "Epaules", "Triceps", "Abdominaux"],
            "pull_B": ["Dorsaux", "Biceps"],
            "legs_B": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
        })
    else:
        raise ValueError(f"Nombre de jours non supporté: {nb_jours}")


def trier_exercices_par_priorite(exercices_choisis):
    """Trie les exercices par ordre de priorité : polys jambes, polys haut, isolations"""
    polys_jambes = []
    polys_haut = []
    isolations = []
    
    for exo_name in exercices_choisis:
        info = get_exercise_info(exo_name)
        if not info:
            continue
        
        if info['type'] == 'polyarticulaire':
            if info['category'] == 'legs':
                polys_jambes.append(exo_name)
            else:
                polys_haut.append(exo_name)
        else:
            isolations.append(exo_name)
    
    return polys_jambes + polys_haut + isolations


def calculer_volume_hebdomadaire(objectifs_muscles, level="advanced"):
    """Calcule le volume hebdomadaire cible pour chaque muscle selon le niveau"""
    volumes = {}
    for muscle, objectif in objectifs_muscles.items():
        volume_range = VOLUME_OBJECTIFS[level][objectif]
        volumes[muscle] = volume_range[len(volume_range) // 2]
    return volumes


def selectionner_exercices_necessaires(exercices_choisis, volumes_hebdo, split, level="advanced"):
    """Sélectionne uniquement les exercices NÉCESSAIRES pour atteindre EXACTEMENT le volume cible
    
    NOUVELLE APPROCHE GLOBALE :
    - Alloue chaque exercice UNE SEULE FOIS (pas de doublons pour exercices multi-muscles)
    - Compte le volume pour TOUS les muscles primaires simultanément
    - Utilise le minimum d'exercices nécessaires pour atteindre tous les volumes
    """
    exercices_tries = trier_exercices_par_priorite(exercices_choisis)
    
    # Tracker global des exercices déjà alloués (éviter doublons)
    exercices_alloues = {}  # {exo_name: [(muscle, series), ...]}
    volumes_restants = dict(volumes_hebdo)  # Copie modifiable
    nb_sessions = len(split.sessions)
    
    # Phase 1: Polyarticulaires en priorité
    for exo_name in exercices_tries:
        info = get_exercise_info(exo_name)
        if not info or info['type'] != 'polyarticulaire':
            continue
        
        # Quels muscles de cet exercice ont encore besoin de volume ?
        muscles_cibles = [m for m in info['primary_muscles'] if m in volumes_restants and volumes_restants[m] > 0]
        
        if not muscles_cibles:
            continue  # Cet exercice ne sert aucun muscle qui a besoin de volume
        
        # Calculer combien de séries allouer pour cet exercice
        # On prend le MIN des besoins de chaque muscle (pour ne pas dépasser)
        volume_max_possible = min(volumes_restants[m] for m in muscles_cibles)
        
        if level == "beginner":
            series = min(3, volume_max_possible)
        else:
            series = min(4, volume_max_possible)
        
        series = min(series, 5)
        
        if series == 0:
            continue
        
        # Allouer cet exercice pour TOUS ses muscles primaires concernés
        exercices_alloues[exo_name] = [(m, series) for m in muscles_cibles]
        
        # Déduire le volume de TOUS les muscles primaires
        for muscle in muscles_cibles:
            volumes_restants[muscle] -= series
    
    # Phase 2: Isolations pour compléter
    for exo_name in exercices_tries:
        info = get_exercise_info(exo_name)
        if not info or info['type'] != 'isolation':
            continue
        
        # Quels muscles de cet exercice ont encore besoin de volume ?
        muscles_cibles = [m for m in info['primary_muscles'] if m in volumes_restants and volumes_restants[m] > 0]
        
        if not muscles_cibles:
            continue
        
        # Pour les isolations, on peut répéter plusieurs fois si nécessaire
        nb_apparitions = 0
        
        while nb_apparitions < nb_sessions:
            # Recalculer à chaque itération
            muscles_encore_besoin = [m for m in muscles_cibles if volumes_restants[m] > 0]
            if not muscles_encore_besoin:
                break
            
            volume_max_possible = min(volumes_restants[m] for m in muscles_encore_besoin)
            
            if volume_max_possible == 0:
                break
            
            # ÉVITER LES SÉRIES UNIQUES : Si volume_max_possible = 1, essayer d'ajouter à une apparition existante
            if volume_max_possible == 1 and exo_name in exercices_alloues:
                # Chercher une apparition existante de cet exercice pour ces muscles
                for i, (m, series) in enumerate(exercices_alloues[exo_name]):
                    if m in muscles_encore_besoin and series < 5:
                        # Ajouter 1 série à cette apparition existante
                        exercices_alloues[exo_name][i] = (m, series + 1)
                        volumes_restants[m] -= 1
                        
                        # Réduire le volume des autres muscles concernés aussi
                        for autre_m in muscles_encore_besoin:
                            if autre_m != m and volumes_restants[autre_m] > 0:
                                # Trouver et mettre à jour l'apparition pour cet autre muscle
                                for j, (m2, s2) in enumerate(exercices_alloues[exo_name]):
                                    if m2 == autre_m and s2 < 5:
                                        exercices_alloues[exo_name][j] = (m2, s2 + 1)
                                        volumes_restants[autre_m] -= 1
                                        break
                        break
                # Passer à l'exercice suivant
                break
            
            if level == "beginner":
                series = min(2, volume_max_possible)
            else:
                series = min(3, volume_max_possible)
            
            series = min(series, 5)
            
            if series == 0:
                break
            
            # Ajouter une apparition
            if exo_name not in exercices_alloues:
                exercices_alloues[exo_name] = []
            
            exercices_alloues[exo_name].extend([(m, series) for m in muscles_encore_besoin])
            
            # Déduire le volume
            for muscle in muscles_encore_besoin:
                volumes_restants[muscle] = max(0, volumes_restants[muscle] - series)
            
            nb_apparitions += 1
    
    # Phase 3: Si encore du volume manquant, répéter les polys
    for exo_name in exercices_tries:
        info = get_exercise_info(exo_name)
        if not info or info['type'] != 'polyarticulaire':
            continue
        
        muscles_cibles = [m for m in info['primary_muscles'] if m in volumes_restants and volumes_restants[m] > 0]
        
        if not muscles_cibles:
            continue
        
        # Combien d'apparitions déjà ?
        nb_apparitions_actuelles = len([x for x in exercices_alloues.get(exo_name, [])]) // len(info['primary_muscles'])
        
        while nb_apparitions_actuelles < nb_sessions:
            volume_max_possible = min(volumes_restants[m] for m in muscles_cibles)
            
            if volume_max_possible == 0:
                break
            
            # Éviter les séries uniques sur polys
            if volume_max_possible < 2:
                break
            
            if level == "beginner":
                series = min(3, volume_max_possible)
            else:
                series = min(4, volume_max_possible)
            
            series = min(series, 5)
            
            if series == 0:
                break
            
            exercices_alloues[exo_name].extend([(m, series) for m in muscles_cibles])
            
            for muscle in muscles_cibles:
                volumes_restants[muscle] -= series
            
            nb_apparitions_actuelles += 1
    
    # Phase 4: ÉLIMINER LES SÉRIES UNIQUES
    # Si des muscles ont encore 1 série restante, les redistribuer vers des exercices existants
    for muscle, volume_restant in list(volumes_restants.items()):
        if volume_restant == 0:
            continue
        
        # Trouver un exercice déjà alloué pour ce muscle
        for exo_name, muscles_series_list in exercices_alloues.items():
            info = get_exercise_info(exo_name)
            if not info:
                continue
            
            # Cet exercice travaille-t-il ce muscle ?
            if muscle not in info['primary_muscles']:
                continue
            
            # Trouver une apparition existante de cet exercice pour ce muscle
            for i, (m, series) in enumerate(muscles_series_list):
                if m == muscle:
                    # Ajouter le volume restant à cette apparition
                    nouvelle_series = min(series + volume_restant, 5)
                    ajout = nouvelle_series - series
                    
                    if ajout > 0:
                        # Mettre à jour les séries
                        muscles_series_list[i] = (m, nouvelle_series)
                        volumes_restants[muscle] -= ajout
                        
                        if volumes_restants[muscle] <= 0:
                            break
            
            if volumes_restants[muscle] <= 0:
                break
    
    # Convertir en format d'allocation par muscle
    allocation = {muscle: [] for muscle in volumes_hebdo.keys()}
    
    for exo_name, muscles_series_list in exercices_alloues.items():
        # Grouper par muscle
        par_muscle = {}
        for muscle, series in muscles_series_list:
            if muscle not in par_muscle:
                par_muscle[muscle] = []
            par_muscle[muscle].append(series)
        
        # Ajouter à l'allocation
        for muscle, series_list in par_muscle.items():
            for series in series_list:
                allocation[muscle].append((exo_name, 1, series))
    
    return allocation


def repartir_exercices_full_body(allocation_exercices, volumes_hebdo, nb_jours, level="advanced"):
    """Répartit les exercices sur les séances Full Body
    
    CRITIQUE: Quand un exercice a plusieurs muscles primaires, il faut créer UNE SEULE
    apparition physique qui compte pour TOUS ces muscles simultanément.
    """
    nb_sessions = min(nb_jours, 3)
    sessions = {f"session_{chr(65+i)}": [] for i in range(nb_sessions)}
    volumes_par_session = {s: 0 for s in sessions.keys()}
    patterns_utilises = {s: set() for s in sessions.keys()}
    exercices_par_session = {s: {} for s in sessions.keys()}
    
    # Créer les apparitions en évitant les doublons pour exercices multi-muscles
    apparitions = []
    apparitions_traitees = set()  # (exo_name, series, muscle_index)
    
    # D'abord, identifier toutes les entrées de l'allocation
    toutes_entrees = []
    for muscle, exercices_list in allocation_exercices.items():
        for idx, (exo_name, nb_apparitions, series_exactes) in enumerate(exercices_list):
            toutes_entrees.append((muscle, exo_name, series_exactes, idx))
    
    # Grouper les entrées par (exo_name, series) pour détecter les muscles multiples
    for muscle, exo_name, series_exactes, idx in toutes_entrees:
        # Clé unique pour cette entrée spécifique
        entree_key = (exo_name, series_exactes, muscle, idx)
        
        if entree_key in apparitions_traitees:
            continue
        
        info = get_exercise_info(exo_name)
        if not info:
            continue
        
        # Trouver TOUS les muscles de cette allocation qui partagent cette apparition
        # (même exercice, même nombre de séries, même index)
        muscles_concernes = [muscle]
        apparitions_traitees.add(entree_key)
        
        # Chercher les autres muscles primaires de cet exercice
        for autre_muscle in info['primary_muscles']:
            if autre_muscle == muscle or autre_muscle not in allocation_exercices:
                continue
            
            # Vérifier si ce muscle a aussi cet exercice avec ces séries au même index
            autres_exos = allocation_exercices[autre_muscle]
            if idx < len(autres_exos):
                autre_exo, autre_nb, autre_series = autres_exos[idx]
                if autre_exo == exo_name and autre_series == series_exactes:
                    muscles_concernes.append(autre_muscle)
                    apparitions_traitees.add((exo_name, series_exactes, autre_muscle, idx))
        
        # Créer UNE apparition avec TOUS les muscles concernés
        apparitions.append((exo_name, muscles_concernes, info, series_exactes))
    
    # Trier les apparitions (polyarticulaires jambes en premier)
    apparitions.sort(key=lambda x: (
        0 if x[2]['type'] == 'polyarticulaire' and x[2]['category'] == 'legs' else
        1 if x[2]['type'] == 'polyarticulaire' else 2
    ))
    
    # Distribuer chaque apparition
    for exo_name, muscles_concernes, info, series_exactes in apparitions:
        pattern = info['pattern']
        session_choisie = None
        min_volume = float('inf')
        
        for session_name in sessions.keys():
            # RÈGLE 1: Un exercice peut apparaître plusieurs fois dans le programme
            # mais limite raisonnable dans une même session (max 1 fois par session généralement)
            if exercices_par_session[session_name].get(exo_name, 0) >= 1:
                continue
            
            # RÈGLE 2: Contrainte Full Body UNIQUEMENT pour 3+ jours
            # Pour 2 jours, on priorise le VOLUME - pas de contraintes push/pull
            if nb_jours >= 3 and info['type'] == 'polyarticulaire':
                push_patterns = {'Horizontal Push (Chest)', 'Vertical Push', 'Incline Push'}
                pull_patterns = {'Horizontal Pull', 'Vertical Pull'}
                
                # Si c'est un push polyarticulaire et la session contient déjà un push polyarticulaire, on skip
                if pattern in push_patterns:
                    if patterns_utilises[session_name] & push_patterns:
                        continue
                # Si c'est un pull polyarticulaire et la session contient déjà un pull polyarticulaire, on skip
                if pattern in pull_patterns:
                    if patterns_utilises[session_name] & pull_patterns:
                        continue
            
            # Choisir session avec moins de volume
            if volumes_par_session[session_name] < min_volume:
                min_volume = volumes_par_session[session_name]
                session_choisie = session_name
        
        # Si aucune session ne respecte les contraintes, prendre n'importe quelle session disponible
        if session_choisie is None:
            # Prendre la session avec le moins de volume, sans contraintes
            session_choisie = min(sessions.keys(), key=lambda s: volumes_par_session[s])
        
        # Ajouter l'exercice
        sessions[session_choisie].append({
            "exercice": exo_name,
            "series": str(series_exactes),
            "muscles": muscles_concernes  # TOUS les muscles primaires de l'allocation
        })
        
        # Mettre à jour les trackers
        if nb_jours >= 3 and info['type'] == 'polyarticulaire':
            patterns_utilises[session_choisie].add(pattern)
        exercices_par_session[session_choisie][exo_name] = exercices_par_session[session_choisie].get(exo_name, 0) + 1
        volumes_par_session[session_choisie] += series_exactes
    
    # Trier (polyarticulaires en premier)
    for session_name in sessions.keys():
        sessions[session_name].sort(key=lambda x: (
            0 if get_exercise_info(x['exercice'])['type'] == 'polyarticulaire' else 1,
            0 if get_exercise_info(x['exercice'])['category'] == 'legs' else 1
        ))
    
    return sessions


def repartir_exercices_upper_lower(allocation_exercices, volumes_hebdo, nb_jours, level="advanced"):
    """Répartit les exercices sur les séances Upper/Lower
    
    IMPORTANT: Grouper les exercices multi-muscles pour éviter les doublons.
    """
    sessions = {
        "upper_A": [],
        "lower_A": [],
        "upper_B": [],
        "lower_B": []
    }
    volumes_par_session = {s: 0 for s in sessions.keys()}
    exercices_par_session = {s: {} for s in sessions.keys()}
    
    # Créer les apparitions en évitant les doublons pour exercices multi-muscles
    apparitions = []
    apparitions_traitees = set()
    
    toutes_entrees = []
    for muscle, exercices_list in allocation_exercices.items():
        for idx, (exo_name, nb_apparitions, series_exactes) in enumerate(exercices_list):
            toutes_entrees.append((muscle, exo_name, series_exactes, idx))
    
    for muscle, exo_name, series_exactes, idx in toutes_entrees:
        entree_key = (exo_name, series_exactes, muscle, idx)
        
        if entree_key in apparitions_traitees:
            continue
        
        info = get_exercise_info(exo_name)
        if not info:
            continue
        
        muscles_concernes = [muscle]
        apparitions_traitees.add(entree_key)
        
        for autre_muscle in info['primary_muscles']:
            if autre_muscle == muscle or autre_muscle not in allocation_exercices:
                continue
            
            autres_exos = allocation_exercices[autre_muscle]
            if idx < len(autres_exos):
                autre_exo, autre_nb, autre_series = autres_exos[idx]
                if autre_exo == exo_name and autre_series == series_exactes:
                    muscles_concernes.append(autre_muscle)
                    apparitions_traitees.add((exo_name, series_exactes, autre_muscle, idx))
        
        apparitions.append((exo_name, muscles_concernes, info, series_exactes))
    
    # Trier les apparitions (polyarticulaires en premier)
    apparitions.sort(key=lambda x: (
        0 if x[2]['type'] == 'polyarticulaire' and x[2]['category'] == 'legs' else
        1 if x[2]['type'] == 'polyarticulaire' else 2
    ))
    
    # Distribuer chaque apparition
    for exo_name, muscles_concernes, info, series_exactes in apparitions:
        if info['category'] in ['push', 'pull', 'core']:
            sessions_cibles = ['upper_A', 'upper_B']
        else:
            sessions_cibles = ['lower_A', 'lower_B']
        
        # Trouver session qui n'a pas encore cet exercice et a le moins de volume
        session_choisie = None
        min_volume = float('inf')
        
        for s in sessions_cibles:
            if exercices_par_session[s].get(exo_name, 0) < 1:
                if volumes_par_session[s] < min_volume:
                    min_volume = volumes_par_session[s]
                    session_choisie = s
        
        # Si l'exercice est déjà dans toutes les sessions, prendre celle avec moins de volume
        if session_choisie is None:
            session_choisie = min(sessions_cibles, key=lambda s: volumes_par_session[s])
        
        sessions[session_choisie].append({
            "exercice": exo_name,
            "series": str(series_exactes),
            "muscles": muscles_concernes  # TOUS les muscles
        })
        
        exercices_par_session[session_choisie][exo_name] = exercices_par_session[session_choisie].get(exo_name, 0) + 1
        volumes_par_session[session_choisie] += series_exactes
    
    for session_name in sessions.keys():
        sessions[session_name].sort(key=lambda x: (
            0 if get_exercise_info(x['exercice'])['type'] == 'polyarticulaire' else 1
        ))
    
    return sessions


def repartir_exercices_ppl(allocation_exercices, volumes_hebdo, level="advanced"):
    """Répartit les exercices sur les séances Push/Pull/Legs
    
    IMPORTANT: Grouper les exercices multi-muscles pour éviter les doublons.
    """
    sessions = {
        "push_A": [],
        "pull_A": [],
        "legs_A": [],
        "push_B": [],
        "pull_B": [],
        "legs_B": []
    }
    volumes_par_session = {s: 0 for s in sessions.keys()}
    exercices_par_session = {s: {} for s in sessions.keys()}
    
    # Créer les apparitions en évitant les doublons pour exercices multi-muscles
    apparitions = []
    apparitions_traitees = set()
    
    toutes_entrees = []
    for muscle, exercices_list in allocation_exercices.items():
        for idx, (exo_name, nb_apparitions, series_exactes) in enumerate(exercices_list):
            toutes_entrees.append((muscle, exo_name, series_exactes, idx))
    
    for muscle, exo_name, series_exactes, idx in toutes_entrees:
        entree_key = (exo_name, series_exactes, muscle, idx)
        
        if entree_key in apparitions_traitees:
            continue
        
        info = get_exercise_info(exo_name)
        if not info:
            continue
        
        muscles_concernes = [muscle]
        apparitions_traitees.add(entree_key)
        
        for autre_muscle in info['primary_muscles']:
            if autre_muscle == muscle or autre_muscle not in allocation_exercices:
                continue
            
            autres_exos = allocation_exercices[autre_muscle]
            if idx < len(autres_exos):
                autre_exo, autre_nb, autre_series = autres_exos[idx]
                if autre_exo == exo_name and autre_series == series_exactes:
                    muscles_concernes.append(autre_muscle)
                    apparitions_traitees.add((exo_name, series_exactes, autre_muscle, idx))
        
        apparitions.append((exo_name, muscles_concernes, info, series_exactes))
    
    # Trier les apparitions (polyarticulaires en premier)
    apparitions.sort(key=lambda x: (
        0 if x[2]['type'] == 'polyarticulaire' and x[2]['category'] == 'legs' else
        1 if x[2]['type'] == 'polyarticulaire' else 2
    ))
    
    # Distribuer chaque apparition
    for exo_name, muscles_concernes, info, series_exactes in apparitions:
        if info['category'] == 'push' or info['category'] == 'core':
            sessions_cibles = ['push_A', 'push_B']
        elif info['category'] == 'pull':
            sessions_cibles = ['pull_A', 'pull_B']
        else:
            sessions_cibles = ['legs_A', 'legs_B']
        
        # Trouver session qui n'a pas encore cet exercice et a le moins de volume
        session_choisie = None
        min_volume = float('inf')
        
        for s in sessions_cibles:
            if exercices_par_session[s].get(exo_name, 0) < 1:
                if volumes_par_session[s] < min_volume:
                    min_volume = volumes_par_session[s]
                    session_choisie = s
        
        # Si l'exercice est déjà dans toutes les sessions, prendre celle avec moins de volume
        if session_choisie is None:
            session_choisie = min(sessions_cibles, key=lambda s: volumes_par_session[s])
        
        sessions[session_choisie].append({
            "exercice": exo_name,
            "series": str(series_exactes),
            "muscles": muscles_concernes  # TOUS les muscles
        })
        
        exercices_par_session[session_choisie][exo_name] = exercices_par_session[session_choisie].get(exo_name, 0) + 1
        volumes_par_session[session_choisie] += series_exactes
    
    for session_name in sessions.keys():
        sessions[session_name].sort(key=lambda x: (
            0 if get_exercise_info(x['exercice'])['type'] == 'polyarticulaire' else 1
        ))
    
    return sessions


def ajuster_volumes_exacts(programme, volumes_hebdo):
    """Ajuste les séries pour atteindre exactement les volumes cibles"""
    MAX_ITERATIONS = 10
    
    for iteration in range(MAX_ITERATIONS):
        # Calculer volume actuel par muscle
        volumes_actuels = {}
        exercices_par_muscle = {}
        
        for session_name, exercices in programme.items():
            for exo in exercices:
                muscle = exo['muscles'][0]
                series_str = exo['series']
                
                if '-' in series_str:
                    min_s, max_s = map(int, series_str.split('-'))
                    avg = (min_s + max_s) / 2.0
                else:
                    avg = float(series_str)
                
                volumes_actuels[muscle] = volumes_actuels.get(muscle, 0) + avg
                
                if muscle not in exercices_par_muscle:
                    exercices_par_muscle[muscle] = []
                exercices_par_muscle[muscle].append((session_name, exo))
        
        # Vérifier convergence
        tout_bon = True
        
        # Ajuster chaque muscle
        for muscle, volume_cible in volumes_hebdo.items():
            volume_actuel = volumes_actuels.get(muscle, 0)
            diff = volume_cible - volume_actuel
            
            if abs(diff) < 0.1:
                continue
            
            tout_bon = False
            
            if muscle not in exercices_par_muscle:
                continue
            
            exos = exercices_par_muscle[muscle]
            nb_exos = len(exos)
            
            # Calculer l'ajustement total nécessaire
            series_totales_a_ajuster = abs(diff)
            
            # Distribuer l'ajustement sur tous les exercices
            for idx, (session_name, exo) in enumerate(exos):
                series_str = exo['series']
                
                if '-' in series_str:
                    min_s, max_s = map(int, series_str.split('-'))
                else:
                    min_s = max_s = int(series_str)
                
                # Part de l'ajustement pour cet exercice
                ajustement = series_totales_a_ajuster / nb_exos
                
                if diff > 0:
                    # Augmenter
                    # Stratégie: augmenter le max et parfois le min
                    if ajustement >= 1.5:
                        # Grosse augmentation nécessaire
                        new_max = 5
                        new_min = min(5, max(2, min_s + int(ajustement / 2)))
                    elif ajustement >= 0.8:
                        # Augmentation moyenne
                        new_max = min(5, max_s + 1)
                        new_min = max(2, min(new_max, min_s))
                    else:
                        # Petite augmentation
                        new_max = min(5, max_s + 1)
                        new_min = min_s
                else:
                    # Diminuer
                    # Stratégie: diminuer le min et parfois le max
                    if ajustement >= 1.5:
                        new_min = 2
                        new_max = max(2, min(5, max_s - int(ajustement / 2)))
                    elif ajustement >= 0.8:
                        new_min = max(2, min_s - 1)
                        new_max = max(new_min, min(5, max_s))
                    else:
                        new_min = max(2, min_s - 1)
                        new_max = max_s
                
                # Mettre à jour
                if new_min == new_max:
                    exo['series'] = str(new_max)
                else:
                    exo['series'] = f"{new_min}-{new_max}"
        
        if tout_bon:
            break


def generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, level="advanced", pattern_muscles=None):
    """Génère un programme d'entraînement complet avec volumes EXACTS"""
    split = create_prog(nb_jours)
    volumes_hebdo = calculer_volume_hebdomadaire(objectifs_muscles, level)
    allocation = selectionner_exercices_necessaires(exercices_choisis, volumes_hebdo, split, level)
    
    if split.name == "Full Body":
        programme = repartir_exercices_full_body(allocation, volumes_hebdo, nb_jours, level)
    elif split.name == "Upper/Lower":
        programme = repartir_exercices_upper_lower(allocation, volumes_hebdo, nb_jours, level)
    else:
        programme = repartir_exercices_ppl(allocation, volumes_hebdo, level)
    
    # Plus besoin d'ajuster - les volumes sont déjà exacts !
    
    return programme


def create_complete_program(nb_jours, objectifs_muscles, exercices_choisis, level="advanced"):
    """Fonction wrapper pour l'application web"""
    split = create_prog(nb_jours)
    programme = generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, level)
    sessions_order = list(split.sessions.keys())
    
    return programme, split.name, sessions_order


if __name__ == "__main__":
    print("Test du générateur de programme\n")
    
    sample_exercices = [
        'Bench press', 'Dips', 'Dumbell Bench Press', 
        'Overhead press', 'Machine Overhead press',
        'Bent over row', 'Pull up', 'Machine row',
        'Barbell squat', 'Hack squat',
        'Stiff leg deadlift', 'Barbell Hip Thrust',
        'Curl', 'Hammer curl', 'Preacher curl',
        'Pushdown', 'Tricep extension', 'Skull crushers',
        'Lateral raises', 'Machine ab crunch'
    ]
    
    sample_objectifs = {
        'Pectoraux': 'normal_growth',
        'Epaules': 'normal_growth',
        'Dorsaux': 'normal_growth',
        'Biceps': 'prioritised_growth',
        'Triceps': 'normal_growth',
        'Quadriceps': 'normal_growth',
        'Isquios-jambiers': 'maintenance',
        'Abdominaux': 'maintenance'
    }
    
    for jours in [2, 3, 4, 5, 6]:
        print(f"\n{'='*60}")
        print(f"Programme {jours} jours/semaine (ADVANCED)")
        print('='*60)
        
        prog, split_name, order = create_complete_program(jours, sample_objectifs, sample_exercices, "advanced")
        
        print(f"Split: {split_name}")
        print(f"Sessions: {order}\n")
        
        for session_name in order:
            if session_name not in prog or not prog[session_name]:
                continue
            print(f"\n{session_name.upper()}:")
            for exo in prog[session_name]:
                print(f"  - {exo['exercice']}: {exo['series']} séries ({exo['muscles']})")
        
        print("\nVérification volumes hebdomadaires:")
        volumes = {}
        for session_name, exercices in prog.items():
            for exo in exercices:
                muscle = exo['muscles'][0]
                series = exo['series']
                if '-' in series:
                    min_s, max_s = map(int, series.split('-'))
                    avg = (min_s + max_s) / 2
                else:
                    avg = float(series)
                volumes[muscle] = volumes.get(muscle, 0) + avg
        
        for muscle, vol in sorted(volumes.items()):
            objectif = sample_objectifs.get(muscle, 'N/A')
            if objectif != 'N/A':
                cible = calculer_volume_hebdomadaire({muscle: objectif})[muscle]
                print(f"  {muscle}: {vol:.1f} séries (cible: {cible})")
