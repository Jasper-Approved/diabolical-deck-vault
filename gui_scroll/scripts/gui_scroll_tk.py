import tkinter as tk
from PIL import Image, ImageTk
import yaml
import pygame

# 🧬 Load the scroll
with open('scrolls/vernon-scroll.yaml', 'r') as f:
    scroll_data = yaml.safe_load(f)['scroll']
steps = scroll_data['remedy']['steps']

# 🎵 Audio Setup
pygame.mixer.init()
pygame.mixer.music.load('gui_scroll/assets/golden-haze-01.mp3')
pygame.mixer.music.play(-1)

# 🖼️ GUI Setup
root = tk.Tk()
root.title("Vernon Repairs Scroll Test")
root.geometry("540x960")
root.resizable(False, False)

canvas = tk.Canvas(root, width=540, height=960)
canvas.pack()

# 🔴 Red Background Layer
canvas.create_rectangle(0, 0, 540, 960, fill="#3a0000", outline="")  # Deep red

# 🌫️ Fog Image Overlay
bg_image = Image.open("gui_scroll/assets/blue_fog_espresso.png").resize((540, 960))
bg_photo = ImageTk.PhotoImage(bg_image)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# 🧾 Title & Caption
title_label = tk.Label(root, text=scroll_data['title'], font=("Georgia", 20, "bold"), fg="white", bg="#1e1e1e")
title_label.place(x=20, y=30)

caption_label = tk.Label(root, text=scroll_data['caption'], font=("Helvetica", 12), fg="white", bg="#1e1e1e", wraplength=500)
caption_label.place(x=20, y=70)

# 🔮 Scroll Logic
step_index = 0
branch_steps = None
lineage = []
step_text = tk.StringVar()

def render_step():
    global step_index, branch_steps
    current_steps = branch_steps if branch_steps else steps

    if step_index < len(current_steps):
        step = current_steps[step_index]
        if 'text' in step:
            step_text.set(step['text'])
            yes_button.place_forget()
            no_button.place_forget()
            next_button.place(x=220, y=850)
        elif 'question' in step:
            step_text.set(step['question'])
            next_button.place_forget()
            yes_button.place(x=150, y=850)
            no_button.place(x=300, y=850)
    else:
        show_completion_screen()

def restart_scroll():
    global step_index, branch_steps, lineage
    step_index = 0
    branch_steps = None
    lineage = []
    
    # Restore canvas and labels
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 540, 960, fill="#3a0000", outline="")
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    title_label.place(x=20, y=30)
    caption_label.place(x=20, y=70)
    step_label.place(x=20, y=700)

    restart_button.place_forget()
    render_step()

def next_step():
    global step_index
    step_index += 1
    render_step()

def handle_response(response):
    global step_index, branch_steps
    current_steps = branch_steps if branch_steps else steps
    step = current_steps[step_index]

    lineage.append(f"Q: {step['question']} → {response.capitalize()}")

    branch_key = f"if_{response}"
    if branch_key in step:
        branch_steps = step[branch_key]
        step_index = 0
    else:
        step_index += 1

    render_step()

def show_completion_screen():
    # Clear canvas and buttons
    canvas.delete("all")
    yes_button.place_forget()
    no_button.place_forget()
    next_button.place_forget()
    title_label.place_forget()
    caption_label.place_forget()
    step_label.place_forget()

    # Red background again
    canvas.create_rectangle(0, 0, 540, 960, fill="#3a0000", outline="")

    # Completion message
    complete_label = tk.Label(root, text="🧬 Scroll complete.", font=("Georgia", 24, "bold"), fg="white", bg="#3a0000")
    complete_label.place(relx=0.5, rely=0.4, anchor="center")

    # Footer message
    footer_label = tk.Label(root, text="This is only test data.", font=("Helvetica", 10), fg="white", bg="#3a0000")
    footer_label.place(relx=0.5, rely=0.95, anchor="center")

# 📜 Step Display
step_label = tk.Label(root, textvariable=step_text, font=("Helvetica", 16), fg="white", bg="#1e1e1e", wraplength=500, justify="center")
step_label.place(x=20, y=700)

# 🕯️ Buttons
next_button = tk.Button(root, text="Next", command=next_step, font=("Helvetica", 14), bg="#1e3a5f", fg="white", relief="raised", padx=10, pady=5)
yes_button = tk.Button(root, text="Yes", command=lambda: handle_response("yes"), font=("Helvetica", 14), bg="#3a5f1e", fg="white", relief="raised", padx=10, pady=5)
no_button = tk.Button(root, text="No", command=lambda: handle_response("no"), font=("Helvetica", 14), bg="#5f1e1e", fg="white", relief="raised", padx=10, pady=5)
restart_button = tk.Button(root, text="Restart", command=restart_scroll, font=("Helvetica", 12), bg="#1e3a5f", fg="white")
restart_button.place(relx=0.5, rely=0.6, anchor="center")

render_step()
root.mainloop()
