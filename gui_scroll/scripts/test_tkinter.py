import tkinter as tk
from PIL import Image, ImageTk
import yaml

# 🧬 Load the scroll
with open('scrolls/vernon-scroll.yaml', 'r') as f:
    scroll_data = yaml.safe_load(f)['scroll']
steps = scroll_data['remedy']['steps']

# 🖼️ GUI Setup
root = tk.Tk()
root.title("Vernon Repairs Scroll Test")
root.geometry("540x960")  # 9:16 aspect ratio

# 🌫️ Background Image
bg_image = Image.open("assets/blue_fog_espresso.png").resize((540, 960))
bg_image.putalpha(80)  # ~30% opacity
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
        step_text.set("🧬 Scroll complete.")

def next_step():
    global step_index
    step_index += 1
    render_step()

label = tk.Label(root, textvariable=step_text, wraplength=500, font=("Helvetica", 16), bg="#000000", fg="#ffffff")
label.place(x=20, y=700)

button = tk.Button(root, text="Next", command=next_step)
button.place(x=220, y=850)

render_step()
root.mainloop()
