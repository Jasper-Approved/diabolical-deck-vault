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
#import yaml
import os

app = Flask(__name__)
app.secret_key = 'vernon-scroll-secret'  # 🔐 Needed for session tracking

# 📜 Load scroll from YAML
def load_scroll(path="scrolls/vernon-scroll.yaml"):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        return data['scroll']

# 🏠 Home route: Show scroll metadata
@app.route('/')
def index():
    scroll = load_scroll()
    session['lineage'] = []
    session['step_index'] = 0
    return render_template('index.html', scroll=scroll)

# 🧭 Step route: Interpret one step at a time
@app.route('/step', methods=['GET', 'POST'])
def step():
    scroll = load_scroll()
    steps = scroll['remedy']['steps']
    index = session.get('step_index', 0)
    lineage = session.get('lineage', [])

    if request.method == 'POST':
        response = request.form.get('response')
        question = request.form.get('question')
        if response and question:
            lineage.append(f"Q: {question} → {response.capitalize()}")
            session['lineage'] = lineage

        # Advance index or branch
        branch = request.form.get('branch')
        if branch:
            steps = eval(branch)  # ⚠️ Replace with safe branching later
            session['branch_steps'] = steps
            session['step_index'] = 0
        else:
            session['step_index'] = index + 1

    # Handle branching
    branch_steps = session.get('branch_steps')
    if branch_steps:
        steps = branch_steps
        index = session['step_index']

    if index >= len(steps):
        return redirect(url_for('lineage'))

    return render_template('step.html', step=steps[index], index=index)

# 🧬 Lineage route: Show final log
@app.route('/lineage')
def lineage():
    lineage = session.get('lineage', [])
    return render_template('lineage.html', lineage=lineage)

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Scroll is alive."

if __name__ == "__main__":
    app.run()

