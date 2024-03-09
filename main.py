import tkinter as tk
from PIL import Image, ImageTk
import pygame
import random
import os
import sys

# Initiate pygame mixer
pygame.mixer.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def on_button_click(event = None):
    yippee_sound.play()
    generate_confetti()
    
def generate_confetti():
    confetti_count = 50
    confetti_size = (5, 15)
    confetti_color = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "white"]
    
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    for _ in range(confetti_count):
        x1 = random.randint(50, canvas_width - 50)
        y1 = random.randint(50, canvas_height - 50)
        size = random.randint(*confetti_size)
        x2 = x1 + size
        y2 = y1 + size
        color = random.choice(confetti_color)
        confetti = canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
        animate_confetti(confetti, canvas_width, canvas_height)
        
def animate_confetti(confetti, canvas_width, canvas_height, speed = 5):
    dx = random.randint(-speed, speed)
    dy = random.randint(-speed, speed)
    
    def move_confetti():
        canvas.move(confetti, dx, dy)
        x0, y0, x1, y1 = canvas.coords(confetti)
        if x0 < 0 or y0 < 0 or x1 > canvas_width or y1 > canvas_height:
            canvas.delete(confetti)
        else:
            canvas.after(50, move_confetti)
            
    move_confetti()
    
    canvas.after(4000, lambda: canvas.delete(confetti))

def resize_image(event):
    new_width = event.width
    new_height = event.height
    yippee_image_path = resource_path("yippee.jpg")
    image = Image.open(yippee_image_path)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    
    #update the canvas item with the new image
    canvas.itemconfig(image_on_canvas, image=photo)
    canvas.image = photo #keeping a reference to the photo
                  
                  
#load the sound
yippee_sound_path = resource_path("yippee-meme-sound-effect.mp3")
yippee_sound = pygame.mixer.Sound(yippee_sound_path)

         
root = tk.Tk()
root.title("Yippee")
root.geometry("400x400")

#create a canvas
canvas = tk.Canvas(root, height=400, width=400)
canvas.pack(fill=tk.BOTH, expand=True)

# Create a photoimage object of the image in the path
yippee_image_path = resource_path("yippee.jpg")
initial_image = Image.open(yippee_image_path)
initial_photo = ImageTk.PhotoImage(initial_image.resize((400, 400), Image.Resampling.LANCZOS))
image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=initial_photo)
canvas.image = initial_photo #keeping a reference to the photo

canvas.bind("<Configure>", resize_image)
canvas.tag_bind(image_on_canvas, "<Button-1>", on_button_click)

root.mainloop()