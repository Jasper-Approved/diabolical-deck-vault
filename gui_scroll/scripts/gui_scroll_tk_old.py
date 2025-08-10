"""
╔══════════════════════════════════════════════════════════════════╗
║  gui_scroll_tk.py — Tkinter Ritual Chamber                      ║
║                                                                  ║
║  A vertical scroll interface wrapped in fog and golden haze.    ║
║  Espresso glyphs whisper beneath each step.                     ║
║                                                                  ║
║  Audio, image, and lineage converge to guide the seeker.        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from PIL import Image, ImageTk
import yaml
import pygame  # For audio playback

# 🧬 Load the scroll
with open('scrolls/vernon-scroll.yaml', 'r') as f:
    scroll_data = yaml.safe_load(f)['scroll']
steps = scroll_data['remedy']['steps']

# 🎵 Initialize audio
pygame.mixer.init()
pygame.mixer.music.load('gui_scroll/assets/golden-haze-01.mp3')
pygame.mixer.music.play(-1)  # Loop indefinitely

# 🖼️ GUI Setup
root = tk.Tk()
root.title("Vernon Repairs Scroll Test")
root.geometry("540x960")  # 9:16 aspect ratio
root.resizable(False, False)

# 🌫️ Background Image
bg_image = Image.open("gui_scroll/assets/blue_fog_espresso.png").resize((540, 960))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=540, height=960)
canvas.pack()
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# 🔮 Scroll Step Renderer
step_index = 0
step_text = tk.StringVar()

def render_step():
    global step_index
    if step_index < len(steps):
        step = steps[step_index]
        if 'text' in step:
            step_text.set(step['text'])
        elif 'question' in step:
            step_text.set(step['question'])
    else:
        step_text.set("🧬 Scroll complete. Vernon repairs with dust.")

def next_step():
    global step_index
    step_index += 1
    render_step()

# 🧾 Title & Metadata
title_label = tk.Label(root, text=scroll_data['title'], font=("Georgia", 20, "bold"), fg="white", bg="#1e1e1e")
title_label.place(x=20, y=30)

caption_label = tk.Label(root, text=scroll_data['caption'], font=("Helvetica", 12), fg="white", bg="#1e1e1e", wraplength=500)
caption_label.place(x=20, y=70)

# 📜 Step Text
step_label = tk.Label(root, textvariable=step_text, font=("Helvetica", 16), fg="white", bg="#1e1e1e", wraplength=500, justify="center")
step_label.place(x=20, y=700)

# 🕯️ Button
button = tk.Button(root, text="Next", command=next_step, font=("Helvetica", 14), bg="#1e3a5f", fg="white", relief="raised", padx=10, pady=5)
button.place(x=220, y=850)

render_step()
root.mainloop()
