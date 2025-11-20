import os
import sys
from flask import Flask, render_template, request, send_file, abort, url_for, redirect, session, jsonify

# make project root importable (assume exercise_database.py is at project root)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from version_site.core.exercise_database import get_pattern_list_for_interface, get_exercise_info, get_muscle_list_with_images
from version_site.core.prog import create_complete_program

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-please-change")
import logging
app.logger.setLevel(logging.INFO)


@app.before_request
def log_request_info():
    # Log every incoming request with a brief snapshot of important session keys
    try:
        sid = request.cookies.get(app.session_cookie_name)
    except Exception:
        sid = None
    app.logger.info('REQ %s %s sessionid=%s muscle_index=%r pattern_index=%r selected_exercises=%r',
                    request.method, request.path, sid, session.get('muscle_index'), session.get('pattern_index'), session.get('selected_exercises'))

def safe_join_root(rel_path):
    # Resolve path and ensure it's inside project root
    if os.path.isabs(rel_path):
        candidate = os.path.normpath(rel_path)
    else:
        candidate = os.path.normpath(os.path.join(PROJECT_ROOT, rel_path))
    
    # Define all possible image directories
    tk_images_root = os.path.normpath(os.path.join(PROJECT_ROOT, "version_tkinter", "images"))
    tk_images2_root = os.path.normpath(os.path.join(PROJECT_ROOT, "version_tkinter", "images 2"))
    site_exercices2_root = os.path.normpath(os.path.join(PROJECT_ROOT, "version_site", "exercices2"))
    
    if candidate.startswith(PROJECT_ROOT) and os.path.exists(candidate):
        return candidate
    
    # If candidate wasn't found at project root, try relative to version_tkinter/images
    alt = os.path.normpath(os.path.join(PROJECT_ROOT, rel_path))
    if os.path.exists(alt):
        return alt
    
    # Try direct path under version_tkinter/images
    alt2 = os.path.normpath(os.path.join(PROJECT_ROOT, "version_tkinter", rel_path))
    if os.path.exists(alt2):
        return alt2
    
    # Try joining rel_path to version_tkinter/images (when rel_path starts with images/...)
    alt3 = os.path.normpath(os.path.join(tk_images_root, os.path.relpath(rel_path, "images"))) if rel_path.startswith("images") else None
    if alt3 and os.path.exists(alt3):
        return alt3
    
    # Try in version_tkinter/images 2 folder
    alt4 = os.path.normpath(os.path.join(tk_images2_root, os.path.basename(rel_path)))
    if os.path.exists(alt4):
        return alt4
    
    # Try joining rel_path to version_tkinter/images 2
    alt5 = os.path.normpath(os.path.join(tk_images2_root, os.path.relpath(rel_path, "images"))) if rel_path.startswith("images") else None
    if alt5 and os.path.exists(alt5):
        return alt5
    
    # Try in version_site/exercices2 folder (for new exercises)
    if rel_path.startswith("exercices2/"):
        alt6 = os.path.normpath(os.path.join(site_exercices2_root, os.path.relpath(rel_path, "exercices2")))
        if os.path.exists(alt6):
            return alt6
    
    # Try direct path in version_site/exercices2
    alt7 = os.path.normpath(os.path.join(site_exercices2_root, os.path.basename(rel_path)))
    if os.path.exists(alt7):
        return alt7
    
    return None

@app.route("/media/<path:path>")
def media(path):
    real = safe_join_root(path)
    if not real or not os.path.exists(real):
        abort(404)
    return send_file(real)


@app.route('/', methods=['GET'])
def index():
    # Landing page: clear any stale session state and redirect to muscle selection
    # This ensures opening the app always starts a fresh flow instead of
    # immediately jumping to later pages when an old session cookie exists.
    for key in ('muscle_index', 'muscle_goals', 'pattern_index', 'selected_per_pattern', 'selected_exercises'):
        session.pop(key, None)
    return redirect(url_for('muscles'))


@app.route('/reset', methods=['GET'])
def reset():
    """Clear selection session state and restart the flow."""
    for key in ('muscle_index', 'muscle_goals', 'pattern_index', 'selected_per_pattern', 'selected_exercises'):
        session.pop(key, None)
    app.logger.info('RESET: session cleared')
    return redirect(url_for('muscles'))


@app.route('/muscles', methods=['GET', 'POST'])
def muscles():
    # Sequential muscle selection: show one muscle at a time (like Tkinter)
    muscles = get_muscle_list_with_images()
    total = len(muscles)
    idx = session.get('muscle_index', 0)
    goals = session.get('muscle_goals', {})

    app.logger.info('MUSCLES ENTER: idx=%r, goals_keys=%r, method=%s', idx, list(goals.keys()), request.method)
    if request.method == 'POST':
        # Expect a field 'goal' with value maintenance/normal_growth/prioritised_growth
        goal = request.form.get('goal')
        muscle_name = muscles[idx][0]
        if goal:
            goals[muscle_name] = goal
            session['muscle_goals'] = goals
            session.modified = True
            app.logger.info('MUSCLES POST: set goal %s for %s; muscle_index (before increment)=%s', goal, muscle_name, idx)

        # advance
        idx += 1
        session['muscle_index'] = idx
        session.modified = True
        app.logger.info('MUSCLES POST: advanced to muscle_index=%s', idx)
        if idx >= total:
            # reset pattern index and start patterns
            session['pattern_index'] = 0
            session['selected_per_pattern'] = {}
            session.modified = True
            app.logger.info('MUSCLES POST: finished muscles, initializing patterns')
            return redirect(url_for('patterns'))
        return redirect(url_for('muscles'))

    # GET: show current muscle
    if idx < 0:
        idx = 0
        session['muscle_index'] = 0

    # If index has reached or passed the end, move to patterns
    if idx >= total:
        session['muscle_index'] = total
        return redirect(url_for('patterns'))

    muscle_name, img = muscles[idx]
    return render_template('muscle_single.html', muscle=muscle_name, img_file=img, index=idx, total=total)


@app.route('/patterns', methods=['GET', 'POST'])
def patterns():
    # Sequential pattern selection: show one pattern at a time and let user pick up to 2 exercises
    patterns = get_pattern_list_for_interface()
    total = len(patterns)
    pidx = session.get('pattern_index', 0)
    selected_per_pattern = session.get('selected_per_pattern', {})

    app.logger.info('PATTERNS ENTER: pidx=%r, selected_per_pattern_keys=%r, method=%s', pidx, list(selected_per_pattern.keys()), request.method)
    if request.method == 'POST':
        # get selected indices (as strings) from form key 'chosen'
        choices = request.form.getlist('chosen')
        # map to exercise names, keep up to 2
        chosen_names = []
        for s in choices[:2]:
            try:
                j = int(s)
                if 0 <= j < len(patterns[pidx][1]):
                    chosen_names.append(patterns[pidx][1][j][0])
            except Exception:
                continue

        selected_per_pattern[str(pidx)] = chosen_names
        session['selected_per_pattern'] = selected_per_pattern
        session.modified = True
        app.logger.info('PATTERNS POST: pidx=%s chosen=%r; saved keys=%r', pidx, chosen_names, list(selected_per_pattern.keys()))

        pidx += 1
        session['pattern_index'] = pidx
        session.modified = True
        app.logger.info('PATTERNS POST: advanced to pattern_index=%s', pidx)
        if pidx >= total:
            # Convert selected_per_pattern dict to flat selected_exercises list
            flat = []
            seen = set()
            for k in sorted(selected_per_pattern.keys(), key=lambda x: int(x)):
                for name in selected_per_pattern[k]:
                    if name not in seen:
                        seen.add(name)
                        flat.append(name)
            session['selected_exercises'] = flat
            session.modified = True
            app.logger.info('PATTERNS POST: finished patterns; selected_exercises=%r', flat)
            return redirect(url_for('choose_days'))
        return redirect(url_for('patterns'))

    # GET: show current pattern
    if pidx < 0:
        pidx = 0
        session['pattern_index'] = 0

    if pidx >= total:
        return redirect(url_for('choose_days'))

    pattern_name, exercises = patterns[pidx]
    # Provide a snapshot of session state for debugging on the page
    session_info = {
        'muscle_index': session.get('muscle_index'),
        'muscle_goals': session.get('muscle_goals'),
        'pattern_index': session.get('pattern_index'),
        'selected_per_pattern': session.get('selected_per_pattern'),
        'selected_exercises': session.get('selected_exercises')
    }
    return render_template('pattern_single.html', pattern_name=pattern_name, exercises=exercises, index=pidx, total=total, session_info=session_info)


@app.route('/choose_days', methods=['GET', 'POST'])
def choose_days():
    if request.method == 'POST':
        try:
            days = int(request.form.get('days'))
            days = max(2, min(6, days))
        except Exception:
            days = 3
        return redirect(url_for('generate', days=days))
    return render_template('choose_days.html')


@app.route('/generate')
def generate():
    # Generate program using session data
    try:
        days = int(request.args.get('days', 3))
    except Exception:
        days = 3

    objectifs = session.get('muscle_goals', {})
    selected = session.get('selected_exercises', [])

    # create_complete_program returns a tuple (programme_by_session, split_name, sessions_order)
    programme_by_session, split_name, sessions_order = create_complete_program(days, objectifs, selected)
    # optional client-side dedupe flag: only enable dedupe script when explicitly requested
    dedupe_flag = bool(request.args.get('dedupe') in ('1', 'true', 'yes'))
    # Log the raw programme for debugging duplicates seen in UI
    # no debug logging here in normal UI

    # Map sessions to day numbers (round-robin over sessions_order)
    program_days = {d+1: [] for d in range(days)}
    for day in range(1, days+1):
        session_name = sessions_order[(day-1) % len(sessions_order)] if sessions_order else None
        if session_name and session_name in programme_by_session:
            exs = []
            seen = set()
            for item in programme_by_session[session_name]:
                name = item.get('exercice') if isinstance(item, dict) else (item[0] if isinstance(item, tuple) else str(item))
                series = item.get('series') if isinstance(item, dict) else ''
                if name in seen:
                    continue
                seen.add(name)
                info = get_exercise_info(name)
                path = info.get('image_path') if info else None
                exs.append((name, path, series))
            program_days[day] = exs
        else:
            program_days[day] = []

    return render_template('program.html', program=program_days, dedupe=dedupe_flag)


@app.route('/program_json')
def program_json():
    """Return the raw programme_by_session JSON for the current session selection.
    Useful for debugging server vs client differences. Call /program_json?days=3
    """
    try:
        days = int(request.args.get('days', 3))
    except Exception:
        days = 3
    objectifs = session.get('muscle_goals', {})
    selected = session.get('selected_exercises', [])
    programme_by_session, split_name, sessions_order = create_complete_program(days, objectifs, selected)
    return jsonify({
        'programme_by_session': programme_by_session,
        'split_name': split_name,
        'sessions_order': sessions_order
    })


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
