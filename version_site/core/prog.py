"""
Algorithme de génération de programme d'entraînement avec compteur de volume strict.

Règles :
1) Débutants : maintenance=3, normal=6, prioritised=9 séries/semaine
   - Tout en poly sauf prioritised (ajoute iso) et biceps/triceps/épaules (iso autorisée)
2) Avancés : maintenance=6, normal=9, prioritised=12 séries/semaine
   - Maintenance: que du poly
   - Normal: 6 poly + 3 iso
   - Prioritised: 6 poly + 6 iso
   - Biceps/triceps/épaules: iso autorisée
3) Split : 2-3j=Full Body, 4-5j=Upper/Lower, 6j=Push/Pull/Legs
4) Tous les exercices choisis ne sont pas forcément utilisés
5) Volume uniformément réparti sur la semaine
6) Un exercice = UNE SEULE ligne par séance avec ses séries
7) Poly avant iso dans l'affichage
"""

from collections import defaultdict
from typing import Dict, List, Literal, Tuple, Set

from .exercise_database import get_exercise_info, get_exercises_by_muscle

Level = Literal["beginner", "advanced"]
Objectif = Literal["maintenance", "normal_growth", "prioritised_growth"]

# Volumes hebdomadaires par muscle
VOLUME_OBJECTIFS: Dict[Level, Dict[Objectif, int]] = {
    "beginner": {
        "maintenance": 3,
        "normal_growth": 6,
        "prioritised_growth": 9,
    },
    "advanced": {
        "maintenance": 6,
        "normal_growth": 9,
        "prioritised_growth": 12,
    },
}


class Split:
    def __init__(self, name: str, sessions: Dict[str, List[str]]):
        self.name = name
        self.sessions = sessions  # { "session_A": ["Pectoraux", ...], ... }


# ---------- 0. Définition du split en fonction du nombre de jours ----------

def create_prog(nb_jours: int) -> Split:
    """
    Choix du format :
       - 2 ou 3 jours -> Full Body
       - 4 ou 5 jours -> Upper / Lower
       - 6 jours      -> Push / Pull / Legs
    """
    # Full Body : même template, on tronque simplement le nb de séances à nb_jours
    if nb_jours in (2, 3):
        fb_sessions = {
            "session_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps",
                          "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "session_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps",
                          "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "session_C": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps",
                          "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
        }
        return Split("Full Body", fb_sessions)

    # Upper / Lower
    if nb_jours in (4, 5):
        ul_sessions = {
            "upper_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
            "lower_A": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires", "Abdominaux"],
            "upper_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
            "lower_B": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires", "Abdominaux"],
            "upper_C": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
        }
        return Split("Upper/Lower", ul_sessions)

    # Push / Pull / Legs (6 jours)
    ppl_sessions = {
        "push_A": ["Pectoraux", "Epaules", "Triceps", "Abdominaux"],
        "pull_A": ["Dorsaux", "Biceps", "Epaules", "Lombaires", "Abdominaux"],
        "legs_A": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires", "Abdominaux"],
        "push_B": ["Pectoraux", "Epaules", "Triceps", "Abdominaux"],
        "pull_B": ["Dorsaux", "Biceps", "Epaules", "Lombaires", "Abdominaux"],
        "legs_B": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires", "Abdominaux"],
    }
    return Split("Push/Pull/Legs", ppl_sessions)


# ---------- 1. Cibles de volume par muscle : total, poly, iso ----------

def compute_muscle_targets(objectifs_muscles: Dict[str, Objectif],
                           level: Level) -> Dict[str, Dict[str, int]]:
    """
    Pour chaque muscle, calcule :
      - total : séries hebdo
      - poly  : séries à faire avec des poly
      - iso   : séries à faire avec des isolations
    """
    targets: Dict[str, Dict[str, int]] = {}
    for muscle, objectif in objectifs_muscles.items():
        total = VOLUME_OBJECTIFS[level][objectif]
        poly = 0
        iso = 0

        if level == "beginner":
            if objectif == "prioritised_growth":
                # On force au moins quelques séries d'iso pour priorisé
                iso = min(3, total) if total >= 3 else 1
                poly = max(0, total - iso)
            else:
                # maintenance / normal : tout en poly par défaut
                poly = total
                iso = 0
        else:  # advanced
            if objectif == "maintenance":
                poly = total
                iso = 0
            elif objectif == "normal_growth":
                # 6 poly, 3 iso (ou adapté si total < 9)
                poly = min(6, total)
                iso = max(0, total - poly)
            elif objectif == "prioritised_growth":
                # 6 poly, 6 iso si possible, sinon proportion
                if total >= 12:
                    poly = 6
                    iso = 6
                else:
                    poly = total // 2
                    iso = total - poly

        targets[muscle] = {"total": total, "poly": poly, "iso": iso}
    return targets


# ---------- 2. Construction des pools d'exercices ----------

def build_exercise_pools(exercices_choisis: List[str],
                         objectifs_muscles: Dict[str, Objectif],
                         level: Level):
    """
    Construit pour chaque muscle :
      pools[muscle]["poly"] = [liste d'exos poly]
      pools[muscle]["iso"] = [liste d'exos d'isolation]
    Retourne aussi un mapping pattern -> liste d'exos poly choisis.
    
    IMPORTANT: Trier les exercices par spécificité (un seul muscle ciblé d'abord).
    """
    pools: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: {"poly": [], "iso": []})
    pattern_to_poly_exos: Dict[str, List[str]] = defaultdict(list)

    # Si aucun exercice choisi, charger tous les exercices disponibles pour chaque muscle
    if not exercices_choisis:
        exercices_choisis = []
        for muscle in objectifs_muscles.keys():
            exercices_choisis.extend(get_exercises_by_muscle(muscle))
        # Dédupliquer
        exercices_choisis = list(set(exercices_choisis))

    # Collecter les exercices
    temp_pools = defaultdict(lambda: {"poly": [], "iso": []})
    
    for exo_name in exercices_choisis:
        info = get_exercise_info(exo_name)
        if not info:
            continue
        exo_type = info.get("type", "polyarticulaire")
        pattern = info.get("pattern", None)

        if exo_type == "polyarticulaire" and pattern:
            pattern_to_poly_exos[pattern].append(exo_name)

        # Utiliser primary_muscles pour éviter le double comptage des volumes
        for muscle in info.get("primary_muscles", []):
            if exo_type == "polyarticulaire":
                if exo_name not in temp_pools[muscle]["poly"]:
                    temp_pools[muscle]["poly"].append(exo_name)
            else:
                if exo_name not in temp_pools[muscle]["iso"]:
                    temp_pools[muscle]["iso"].append(exo_name)
    
    # Trier les exercices par spécificité
    # Pour BEGINNER: favoriser les exercices multi-muscles (plus de primary_muscles = prioritaire)
    # Pour ADVANCED: favoriser les exercices spécifiques (moins de primary_muscles = prioritaire)
    def exercise_specificity(exo_name):
        info = get_exercise_info(exo_name)
        if not info:
            return 999 if level == "beginner" else 0
        num_muscles = len(info.get("primary_muscles", []))
        # Beginner: ordre décroissant (plus = mieux), Advanced: ordre croissant (moins = mieux)
        return -num_muscles if level == "beginner" else num_muscles
    
    for muscle in temp_pools:
        pools[muscle]["poly"] = sorted(temp_pools[muscle]["poly"], key=exercise_specificity)
        pools[muscle]["iso"] = sorted(temp_pools[muscle]["iso"], key=exercise_specificity)

    # Gestion spécifique des épaules : side raise / rear delt si Epaules non en maintenance
    if "Epaules" in objectifs_muscles and objectifs_muscles["Epaules"] != "maintenance":
        shoulder_exos = get_exercises_by_muscle("Epaules")
        has_side = any(
            (get_exercise_info(e) or {}).get("pattern") == "Side Raise"
            for e in pools["Epaules"]["iso"]
        )
        has_rear = any(
            (get_exercise_info(e) or {}).get("pattern") == "Rear Delt"
            for e in pools["Epaules"]["iso"]
        )

        for exo_name in shoulder_exos:
            info = get_exercise_info(exo_name)
            if not info or info.get("type") != "isolation":
                continue
            pattern = info.get("pattern")
            if pattern == "Side Raise" and not has_side:
                pools["Epaules"]["iso"].append(exo_name)
                has_side = True
            elif pattern == "Rear Delt" and not has_rear:
                pools["Epaules"]["iso"].append(exo_name)
                has_rear = True
            if has_side and has_rear:
                break

    return pools, pattern_to_poly_exos


# ---------- 3. Répartition des séries par muscle sur les séances ----------

def distribute_muscle_volume_over_sessions(split: Split,
                                           nb_jours: int,
                                           muscle_targets: Dict[str, Dict[str, int]]
                                           ) -> Tuple[List[str], Dict[str, Dict[str, Dict[str, int]]]]:
    """
    Calcule, pour chaque séance, combien de séries poly / iso doit faire chaque muscle,
    en répartissant aussi uniformément que possible sur la semaine.
    """
    sessions_names = list(split.sessions.keys())[:nb_jours]
    session_targets: Dict[str, Dict[str, Dict[str, int]]] = {s: {} for s in sessions_names}

    for muscle, volumes in muscle_targets.items():
        days_for_muscle = [s for s in sessions_names if muscle in split.sessions[s]]
        if not days_for_muscle:
            continue
        n = len(days_for_muscle)

        for vol_type in ("poly", "iso"):
            total = volumes[vol_type]
            if total <= 0:
                continue
            base = total // n
            extra = total % n
            for idx, session in enumerate(days_for_muscle):
                sets_here = base + (1 if idx < extra else 0)
                if sets_here == 0:
                    continue
                if muscle not in session_targets[session]:
                    session_targets[session][muscle] = {"poly": 0, "iso": 0}
                session_targets[session][muscle][vol_type] += sets_here

    return sessions_names, session_targets


# ---------- 4. Sélection d'exercice avec rotation & priorité poly ----------

def _pick_exercise_rotating(muscle: str,
                            vol_type: str,
                            pools,
                            level: Level,
                            objectifs_muscles: Dict[str, Objectif],
                            used_in_session: List[str],
                            rotation_state: Dict[Tuple[str, str], int]):
    """
    Choisit un exercice pour un muscle donné et un type (poly / iso) avec :
      - priorité aux polyarticulaires
      - rotation entre les exercices disponibles pour varier les séances
      - préférence pour les exercices non encore utilisés dans la séance
    """
    objectif = objectifs_muscles.get(muscle, "maintenance")

    # Pas d'iso en maintenance avancé
    if level == "advanced" and objectif == "maintenance" and vol_type == "iso":
        vol_type = "poly"

    candidates = pools[muscle][vol_type]

    # Si aucun n'est dispo, on tente l'autre type (surtout pour biceps / triceps / épaules ou débutant)
    if not candidates:
        other_type = "iso" if vol_type == "poly" else "poly"
        if muscle in ("Biceps", "Triceps", "Epaules") or level == "beginner":
            candidates = pools[muscle][other_type]
            vol_type = other_type

    if not candidates:
        return None

    key = (muscle, vol_type)
    idx = rotation_state.get(key, 0) % len(candidates)

    # Rotation + préférence exo non utilisé dans la séance
    ordered = candidates[idx:] + candidates[:idx]
    chosen = None
    for exo in ordered:
        if exo not in used_in_session:
            chosen = exo
            break
    if chosen is None:
        chosen = ordered[0]

    rotation_state[key] = idx + 1

    return chosen


# ---------- 5. Allocation des séries à des exercices concrets ----------

def allocate_exercises_to_sessions(sessions_names: List[str],
                                   session_targets,
                                   pools,
                                   level: Level,
                                   objectifs_muscles: Dict[str, Objectif]):
    """
    Transforme les volumes par séance et par muscle en un planning concret :
      programme[session] = [ { "exercice": nom, "series": nb }, ... ]

    Règles :
      - Un exercice ne figure qu'une seule fois par séance.
      - Un exercice compte pour TOUS ses primary_muscles simultanément.
      - Le nombre de séries d'un exercice = max(séries demandées par tous les muscles qu'il cible).
      - Les muscles déjà couverts par un exercice ne reçoivent pas d'exercices supplémentaires.
    """
    session_exo_muscle_demands: Dict[str, Dict[str, List[int]]] = {s: {} for s in sessions_names}
    rotation_state: Dict[Tuple[str, str], int] = {}

    for session in sessions_names:
        muscles_in_session = session_targets.get(session, {})
        used_exercises = set()
        covered_muscles = set()  # Muscles déjà couverts par un exercice dans cette session

        for muscle, vols in muscles_in_session.items():
            # Skip si ce muscle est déjà couvert par un exercice poly
            if muscle in covered_muscles:
                continue
                
            for vol_type in ("poly", "iso"):
                sets_to_place = vols[vol_type]
                if sets_to_place <= 0:
                    continue

                exo = _pick_exercise_rotating(
                    muscle,
                    vol_type,
                    pools,
                    level,
                    objectifs_muscles,
                    used_exercises,
                    rotation_state,
                )
                if exo is None:
                    continue

                used_exercises.add(exo)
                
                # Stocker la demande pour cet exercice
                if exo not in session_exo_muscle_demands[session]:
                    session_exo_muscle_demands[session][exo] = []
                session_exo_muscle_demands[session][exo].append(sets_to_place)
                
                # Marquer tous les primary muscles de cet exercice comme couverts (poly seulement)
                info = get_exercise_info(exo)
                if info and info.get("type") == "polyarticulaire":
                    for prim_muscle in info.get("primary_muscles", []):
                        covered_muscles.add(prim_muscle)

    # Convertir en programme: prendre le MAX des demandes pour chaque exercice
    programme_final: Dict[str, List[Dict[str, int]]] = {}

    for session, exos in session_exo_muscle_demands.items():
        exo_entries = []
        for exo_name, demands in exos.items():
            # Prendre le max des séries demandées
            total_sets = max(demands) if demands else 0
            if total_sets > 0:
                exo_entries.append(
                    {"exercice": exo_name, "series": total_sets}
                )

        # Tri poly d'abord, iso ensuite
        def sort_key(entry):
            info = get_exercise_info(entry["exercice"])
            if not info:
                return (1, entry["exercice"])
            exo_type = info.get("type", "polyarticulaire")
            return (0 if exo_type == "polyarticulaire" else 1, entry["exercice"])

        exo_entries.sort(key=sort_key)
        programme_final[session] = exo_entries

    return programme_final


# ---------- 6. Couverture minimale des patterns de mouvement (poly ONLY) ----------

def enforce_pattern_coverage(programme: Dict[str, List[Dict[str, int]]],
                             split: Split,
                             pattern_to_poly_exos: Dict[str, List[str]]):
    """
    S'assure que chaque pattern poly présent dans la sélection d'exercices
    apparaît au moins une fois dans le programme.
    On n'ajoute QUE des exos poly, et avec 1 série minimum.
    """
    # Patterns déjà utilisés dans le programme (poly uniquement)
    used_patterns = set()
    for exos in programme.values():
        for entry in exos:
            info = get_exercise_info(entry["exercice"])
            if info and info.get("type") == "polyarticulaire" and "pattern" in info:
                used_patterns.add(info["pattern"])

    available_patterns = set(pattern_to_poly_exos.keys())
    missing_patterns = available_patterns - used_patterns

    if not missing_patterns:
        return programme

    sessions_names = list(programme.keys())

    for pattern in missing_patterns:
        exo_list = pattern_to_poly_exos.get(pattern, [])
        if not exo_list:
            continue
        exo_name = exo_list[0]
        info = get_exercise_info(exo_name)
        if not info:
            continue

        primary_muscles = info.get("primary_muscles", [])
        target_session = sessions_names[0]

        for session in sessions_names:
            muscles_of_session = split.sessions.get(session, [])
            if any(m in muscles_of_session for m in primary_muscles):
                target_session = session
                break

        session_exos = programme[target_session]
        found = False
        for entry in session_exos:
            if entry["exercice"] == exo_name:
                entry["series"] = max(entry["series"], 1)
                found = True
                break
        if not found:
            session_exos.append({"exercice": exo_name, "series": 1})

        # On retrie poly/iso
        def sort_key(entry):
            info_e = get_exercise_info(entry["exercice"])
            if not info_e:
                return (1, entry["exercice"])
            exo_type = info_e.get("type", "polyarticulaire")
            return (0 if exo_type == "polyarticulaire" else 1, entry["exercice"])

        session_exos.sort(key=sort_key)

    return programme


# ---------- 7. Fonctions principales ----------

def generate_workout_program(nb_jours: int,
                             objectifs_muscles: Dict[str, Objectif],
                             exercices_choisis: List[str],
                             level: Level = "advanced"):
    """
    Génère un programme avec compteur strict de volume par muscle.
    RÈGLE CLÉ: Si un exercice existe déjà qui cible un muscle, on augmente ses séries
    au lieu d'ajouter un nouvel exercice pour ce muscle.
    """
    split = create_prog(nb_jours)
    sessions_names = list(split.sessions.keys())[:nb_jours]
    
    # 1. Initialiser les cibles de volume par muscle
    muscle_targets = compute_muscle_targets(objectifs_muscles, level)
    
    # 2. Construire les pools d'exercices
    pools, _ = build_exercise_pools(exercices_choisis, objectifs_muscles, level)
    
    # 3. Initialiser les compteurs de volume par muscle (volume hebdomadaire réalisé)
    muscle_counters = {muscle: 0 for muscle in objectifs_muscles.keys()}
    
    # 4. Initialiser le programme par session
    programme: Dict[str, List[Dict[str, any]]] = {s: [] for s in sessions_names}
    
    # 5. Rotation pour varier les exercices entre sessions
    rotation_index = {muscle: {vtype: 0 for vtype in ["poly", "iso"]} for muscle in objectifs_muscles.keys()}
    
    # 6. Tracker: quels exercices sont utilisés dans chaque session
    # Un exercice peut maintenant apparaître dans PLUSIEURS sessions
    exercise_in_session: Dict[str, Set[str]] = {}  # {exercice_name: {session_names}}
    # Tracker des propriétaires par session : {session_name: {exercice_name: muscle_owner}}
    exercise_owner_per_session: Dict[str, Dict[str, str]] = {s: {} for s in sessions_names}
    # Bénéficiaires par exercice et par session
    exercise_benefits_per_session: Dict[str, Dict[str, Set[str]]] = {s: {} for s in sessions_names}
    
    # 7. Allouer les exercices session par session en mode round-robin
    session_idx = 0
    max_iterations = 1000
    iteration = 0
    
    while any(muscle_counters[m] < muscle_targets[m]["total"] for m in objectifs_muscles.keys()) and iteration < max_iterations:
        iteration += 1
        session_name = sessions_names[session_idx % nb_jours]
        muscles_in_session = split.sessions[session_name]
        
        # Trouver un muscle qui a besoin de volume dans cette session
        muscle_added = False
        for muscle in muscles_in_session:
            if muscle not in objectifs_muscles:
                continue
            # Tolérance : si le muscle est à +/-1 série du target, le considérer comme satisfait
            # (on ne peut ajouter que par tranches de 2 séries minimum)
            current = muscle_counters[muscle]
            target = muscle_targets[muscle]["total"]
            if abs(current - target) <= 1 or current >= target:
                continue
            
            # Déterminer quel type d'exercice on veut ajouter (poly/iso)
            global_poly = 0
            global_iso = 0
            for sess in sessions_names:
                for exo_entry in programme[sess]:
                    exo_name = exo_entry["exercice"]
                    # Vérifier si cet exercice dans cette session appartient à ce muscle
                    is_owner = exo_name in exercise_owner_per_session[sess] and exercise_owner_per_session[sess][exo_name] == muscle
                    is_beneficiary = exo_name in exercise_benefits_per_session[sess] and muscle in exercise_benefits_per_session[sess][exo_name]
                    
                    if is_owner or is_beneficiary:
                        exo_info = get_exercise_info(exo_name)
                        if exo_info:
                            if exo_info.get("type") == "polyarticulaire":
                                global_poly += exo_entry["series"]
                            else:
                                global_iso += exo_entry["series"]
            
            # Déterminer quel type d'exercice ajouter
            vol_type = None
            if global_poly < muscle_targets[muscle]["poly"]:
                vol_type = "poly"
            elif global_iso < muscle_targets[muscle]["iso"]:
                vol_type = "iso"
            
            if not vol_type:
                continue
            
            # Maintenant chercher dans cette session si un exercice du bon type existe pour ce muscle
            existing_in_session = None
            for exo_entry in programme[session_name]:
                existing_exo_name = exo_entry["exercice"]
                existing_info = get_exercise_info(existing_exo_name)
                if existing_info:
                    existing_primary = existing_info.get("primary_muscles", [])
                    existing_type = existing_info.get("type", "")
                    
                    # Vérifier si cet exercice cible notre muscle ET est du bon type
                    if muscle in existing_primary:
                        if (vol_type == "poly" and existing_type == "polyarticulaire") or \
                           (vol_type == "iso" and existing_type == "isolation"):
                            # Vérifier que l'ajout de séries ne ferait pas dépasser les bénéficiaires
                            would_overflow_beneficiaries = False
                            for prim_muscle in existing_primary:
                                if prim_muscle in objectifs_muscles and prim_muscle != muscle:
                                    if muscle_counters[prim_muscle] >= muscle_targets[prim_muscle]["total"]:
                                        would_overflow_beneficiaries = True
                                        break
                            
                            # Seulement si aucun bénéficiaire ne dépasserait
                            if not would_overflow_beneficiaries:
                                existing_in_session = existing_exo_name
                                break
            
            # Si on a trouvé un exercice du bon type pour ce muscle, augmenter ses séries
            # MAIS limiter à 4 séries max par exercice dans une session
            if existing_in_session:
                current_series = 0
                for exo_entry in programme[session_name]:
                    if exo_entry["exercice"] == existing_in_session:
                        current_series = exo_entry["series"]
                        # Limiter à 4 séries max par exercice dans une session
                        if current_series < 4:
                            exo_entry["series"] += 2
                            
                            # Incrémenter les compteurs
                            muscle_counters[muscle] += 2
                            
                            # Si cet exercice a des bénéficiaires dans cette session, les incrémenter aussi
                            if existing_in_session in exercise_benefits_per_session[session_name]:
                                for beneficiary in list(exercise_benefits_per_session[session_name][existing_in_session]):
                                    if beneficiary in muscle_counters:
                                        # Vérifier si le bénéficiaire a encore besoin de volume
                                        if muscle_counters[beneficiary] < muscle_targets[beneficiary]["total"]:
                                            muscle_counters[beneficiary] += 2
                                        # Retirer ce muscle des bénéficiaires s'il a atteint son target
                                        if muscle_counters[beneficiary] >= muscle_targets[beneficiary]["total"]:
                                            exercise_benefits_per_session[session_name][existing_in_session].remove(beneficiary)
                            
                            muscle_added = True
                        # Si déjà à 4 séries, ne pas augmenter (on ajoutera un nouvel exercice)
                        break
                
                if muscle_added:
                    break
            
            # Pas d'exercice du bon type trouvé, continuer pour en choisir un nouveau
            
            # Choisir un exercice
            candidates = pools[muscle][vol_type]
            if not candidates:
                # Fallback pour biceps/triceps/épaules ou débutant
                other_type = "iso" if vol_type == "poly" else "poly"
                if muscle in ("Biceps", "Triceps", "Epaules") or level == "beginner":
                    candidates = pools[muscle][other_type]
                    vol_type = other_type if candidates else vol_type
            
            if not candidates:
                continue
            
            # Pour les muscles avec plusieurs patterns (ex: Dorsaux),
            # favoriser un pattern différent de ceux déjà utilisés GLOBALEMENT
            used_patterns = set()
            for sess in sessions_names:
                if sess in exercise_owner_per_session:
                    for exo_name_temp, owner in exercise_owner_per_session[sess].items():
                        if owner == muscle:
                            info_temp = get_exercise_info(exo_name_temp)
                            if info_temp and info_temp.get("pattern"):
                                used_patterns.add(info_temp.get("pattern"))
            
            # Trier les candidats : patterns non utilisés en premier
            candidates_new_pattern = []
            candidates_used_pattern = []
            
            for candidate in candidates:
                info_cand = get_exercise_info(candidate)
                if info_cand:
                    cand_pattern = info_cand.get("pattern")
                    if cand_pattern and cand_pattern not in used_patterns:
                        candidates_new_pattern.append(candidate)
                    else:
                        candidates_used_pattern.append(candidate)
            
            # Prioriser les nouveaux patterns, puis les patterns déjà utilisés
            candidates_sorted = candidates_new_pattern + candidates_used_pattern
            if not candidates_sorted:
                candidates_sorted = candidates
            
            # Rotation et sélection avec la liste triée
            # Un exercice peut maintenant être utilisé dans PLUSIEURS sessions
            exo_name = None
            for attempt in range(len(candidates_sorted)):
                idx = rotation_index[muscle][vol_type] % len(candidates_sorted)
                candidate = candidates_sorted[idx]
                rotation_index[muscle][vol_type] += 1
                
                # Vérifier si cet exercice est déjà dans CETTE session
                already_in_this_session = any(e["exercice"] == candidate for e in programme[session_name])
                if already_in_this_session:
                    continue
                
                # Vérifier les muscles ciblés par cet exercice
                candidate_info = get_exercise_info(candidate)
                if not candidate_info:
                    continue
                
                candidate_muscles = candidate_info.get("primary_muscles", [])
                
                # Vérifier si ajouter cet exercice ferait dépasser un muscle bénéficiaire
                would_overflow = False
                for prim_muscle in candidate_muscles:
                    if prim_muscle in objectifs_muscles and prim_muscle != muscle:
                        current_vol = muscle_counters[prim_muscle]
                        target_vol = muscle_targets[prim_muscle]["total"]
                        if current_vol >= target_vol:
                            would_overflow = True
                            break
                
                if not would_overflow:
                    exo_name = candidate
                    break
            
            # Si aucun exercice trouvé sans débordement, prendre le premier disponible qui n'est pas déjà dans cette session
            if not exo_name:
                for candidate in candidates_sorted:
                    already_in_this_session = any(e["exercice"] == candidate for e in programme[session_name])
                    if not already_in_this_session:
                        candidate_info = get_exercise_info(candidate)
                        if candidate_info:
                            exo_name = candidate
                            break
            
            # Si toujours rien, passer
            if not exo_name:
                continue
            
            # Récupérer les infos de l'exercice pour savoir quels muscles il cible
            exo_info = get_exercise_info(exo_name)
            if not exo_info:
                continue
            
            primary_muscles = exo_info.get("primary_muscles", [])
            
            # Assigner ce muscle comme propriétaire de l'exercice DANS CETTE SESSION
            exercise_owner_per_session[session_name][exo_name] = muscle
            
            # Tracker cet exercice dans cette session
            if exo_name not in exercise_in_session:
                exercise_in_session[exo_name] = set()
            exercise_in_session[exo_name].add(session_name)
            
            # Les autres muscles ciblés deviennent bénéficiaires (si besoin de volume ET ne dépassent pas)
            exercise_benefits_per_session[session_name][exo_name] = set()
            for prim_muscle in primary_muscles:
                if prim_muscle in objectifs_muscles and prim_muscle != muscle:
                    # Ajouter seulement si ce muscle n'a pas encore atteint son target
                    if muscle_counters[prim_muscle] < muscle_targets[prim_muscle]["total"]:
                        exercise_benefits_per_session[session_name][exo_name].add(prim_muscle)
            
            # Calculer le nombre de séries initial en fonction du volume restant et du nombre de jours
            # Pour éviter trop d'exercices à 2 séries, on commence avec plus de séries si nécessaire
            volume_restant = muscle_targets[muscle]["total"] - muscle_counters[muscle]
            series_per_day_needed = volume_restant / nb_jours
            
            # Déterminer le nombre de séries à ajouter
            if series_per_day_needed >= 4:
                initial_series = 4  # Maximum par exercice
            elif series_per_day_needed >= 3:
                initial_series = 4  # Mieux vaut 4 séries qu'ajouter un autre exercice
            else:
                initial_series = 2  # Par défaut
            
            # Ajouter l'exercice dans la session
            programme[session_name].append({"exercice": exo_name, "series": initial_series})
            
            # Mettre à jour le compteur du muscle propriétaire
            muscle_counters[muscle] += initial_series
            
            # ET AUSSI les compteurs des muscles bénéficiaires
            for beneficiary in exercise_benefits_per_session[session_name][exo_name]:
                muscle_counters[beneficiary] += initial_series
            
            muscle_added = True
            break
        
        # Passer à la session suivante
        if muscle_added:
            session_idx += 1
        else:
            session_idx += 1
    
    # 8. Consolider les exercices dupliqués et filtrer < 2 séries
    for session in sessions_names:
        # Consolider: fusionner les exercices identiques
        consolidated = {}
        for exo_entry in programme[session]:
            exo_name = exo_entry["exercice"]
            if exo_name in consolidated:
                consolidated[exo_name] += exo_entry["series"]
            else:
                consolidated[exo_name] = exo_entry["series"]
        
        # Reconstruire la liste
        programme[session] = [
            {"exercice": name, "series": sets}
            for name, sets in consolidated.items()
            if sets >= 2
        ]
        
        # Trier poly avant iso
        def sort_key(entry):
            info = get_exercise_info(entry["exercice"])
            if not info:
                return (1, entry["exercice"])
            exo_type = info.get("type", "polyarticulaire")
            return (0 if exo_type == "polyarticulaire" else 1, entry["exercice"])
        
        programme[session].sort(key=sort_key)
    
    return programme


def create_complete_program(nb_jours: int,
                            objectifs_muscles: Dict[str, Objectif],
                            exercices_choisis: List[str],
                            level: Level = "advanced"):
    """
    Wrapper pour le front :
      - programme détaillé
      - nom du split ("Full Body", "Upper/Lower", "Push/Pull/Legs")
      - ordre des sessions à afficher
    """
    split = create_prog(nb_jours)
    programme = generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, level)
    sessions_order = list(split.sessions.keys())[:nb_jours]
    return programme, split.name, sessions_order
