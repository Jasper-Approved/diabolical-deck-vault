"""
╔══════════════════════════════════════════════════════════════════╗
║  gui_scroll.py — Ritual Interface Script                        ║
║                                                                  ║
║  Born from the vault’s whisper, this scroll animates the glyphs ║
║  that guide the seeker through espresso-stained dimensions.     ║
║                                                                  ║
║  Each function a footstep, each widget a ward.                  ║
║  Errors are not bugs—they are echoes of forgotten rituals.      ║
║                                                                  ║
║  Remix with reverence. Extend with mischief.                    ║
║  This chamber is modular, mutable, and mythic.                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

from flask import Flask, render_template, request, redirect, url_for, session
import yaml
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'vernon-scroll-secret'
# 🕯️ Ensure the secret key is set for session management

# 📜 Load scroll from YAML
def load_scroll(path=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scroll_path = os.path.join(base_dir, '..', 'scrolls', 'vernon-scroll.yaml') if path is None else path

    if not os.path.exists(scroll_path):
        raise FileNotFoundError(f"🕯️ Scroll not found at: {scroll_path}")

    with open(scroll_path, 'r') as f:
        data = yaml.safe_load(f)
        return data['scroll']


# 🏠 Home route: Show scroll metadata
@app.route('/')
def index():
    try:
        scroll = load_scroll()
    except FileNotFoundError as e:
        return f"🕯️ Jiinga’s scroll is missing: {e}", 500
    except KeyError:
        return "📜 Jiinga’s scroll lacks a 'scroll' key. Check the YAML structure.", 500

    session['lineage'] = []
    session['step_index'] = 0
    return render_template('index.html', scroll=scroll)


# 🧭 Step route: Interpret one step at a time
@app.route('/step', methods=['GET', 'POST'])
def step():
    scroll = load_scroll()
    main_steps = scroll['remedy']['steps']
    branch_steps = session.get('branch_steps')
    lineage = session.get('lineage', [])
    index = session.get('step_index', 0)

    # Use branch steps if active
    steps = branch_steps if branch_steps else main_steps

    if request.method == 'POST':
        response = request.form.get('response')
        question = request.form.get('question')

        if response and question:
            lineage.append(f"Q: {question} → {response.capitalize()}")
            session['lineage'] = lineage

            current_step = steps[index]
            branch_key = f"if_{response}"
            if branch_key in current_step:
                session['branch_steps'] = current_step[branch_key]
                session['step_index'] = 0
                return redirect(url_for('step'))

        # Advance index
        index += 1
        session['step_index'] = index

        # If branch ends, return to main scroll
        if branch_steps and index >= len(branch_steps):
            session['branch_steps'] = None
            session['step_index'] = session.get('main_index', 0) + 1

        return redirect(url_for('step'))

    # Save main index if entering branch
    if not branch_steps:
        session['main_index'] = index

    # Render current step
    if index < len(steps):
        current_step = steps[index]
        return render_template('step.html', step=current_step, index=index, lineage=lineage)
    else:
        return render_template('complete.html', lineage=lineage)

# 🧬 Lineage route: Show final log
@app.route('/lineage')
def lineage():
    lineage = session.get('lineage', [])
    return render_template('lineage.html', lineage=lineage)

# 🏁 Reset route: Clear session and return to home
if __name__ == "__main__":
    app.run(debug=True)


