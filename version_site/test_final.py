import sys
sys.path.insert(0, '/Users/alexpeirano/Desktop/personal coding/tinker_project')

from version_site.core.prog import generate_workout_program

muscles_obj = {
    'Quadriceps': 'prioritised_growth',
    'Isquios-jambiers': 'maintenance',
    'Fessiers': 'normal_growth',
    'Mollets': 'maintenance',
    'Pectoraux': 'prioritised_growth',
    'Dos (largeur)': 'normal_growth',
    'Dos (épaisseur)': 'normal_growth',
    'Épaules (deltoïde antérieur)': 'normal_growth',
    'Épaules (deltoïde latéral)': 'normal_growth',
    'Épaules (deltoïde postérieur)': 'normal_growth',
    'Triceps': 'normal_growth',
    'Biceps': 'normal_growth',
    'Lombaires': 'normal_growth',
    'Abdominaux': 'normal_growth'
}

exercices_choisis = [
    'Barbell squat',
    'Stiff leg deadlift',
    'Barbell Hip Thrust',
    'Standing calf raise',
    'Barbell Bench Press',
    'Pull up',
    'Bent over row',
    'Barbell Overhead Press',
    'Lateral raise',
    'Rear delt fly',
    'Dips',
    'Barbell Curl',
    'Back hyperextension',
    'Crunch'
]

programme = generate_workout_program(
    nb_jours=3,
    objectifs_muscles=muscles_obj,
    exercices_choisis=exercices_choisis,
    level='beginner'
)

# Compter les apparitions
exo_counts = {}
print("=== PROGRAMME COMPLET ===")
volumes = {}
for session_name, exos in programme.items():
    print(f"\n{session_name}:")
    for exo in exos:
        nom = exo.get('nom', exo.get('exercice', 'Unknown'))
        series = exo.get('series', 0)
        print(f"  - {nom}: {series} séries")
        
        exo_counts[nom] = exo_counts.get(nom, 0) + 1
        
        # Calculer volumes
        for muscle in exo.get('muscles', []):
            if isinstance(series, int):
                volumes[muscle] = volumes.get(muscle, 0) + series

print("\n=== STIFF LEG DEADLIFT ===")
if 'Stiff leg deadlift' in exo_counts:
    print(f"Apparaît {exo_counts['Stiff leg deadlift']} fois (devrait être 1)")
else:
    print("N'apparaît pas!")

print("\n=== VOLUMES HEBDOMADAIRES ===")
objectifs_vol = {
    'maintenance': 3,
    'normal_growth': 6,
    'prioritised_growth': 9
}
for m in sorted(volumes.keys()):
    obj_type = muscles_obj.get(m, 'unknown')
    obj_vol = objectifs_vol.get(obj_type, '?')
    status = 'OK' if volumes[m] == obj_vol else f'ERREUR: {volumes[m]}/{obj_vol}'
    print(f"{m}: {status}")
