import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

win = Tk()
win.geometry('720x720')
win.resizable(width=False, height=False)
win.title("Imagist")

# Layout
fr = Frame(win)
fr.grid()
canvas = Canvas(fr, background='black', width=640, height=640)
canvas.grid(column=0, row=0)
Button(fr, text="Quit", command=win.destroy).grid(column=0, row=0)

# Load background
bg_img = PhotoImage(file="saturn.gif")
canvas.create_image(0, 0, image=bg_img, anchor=NW)

# Load & place player
spriteW = 50
spriteL = 50

left1 = tk.PhotoImage(file = "assets/leftChicken.png")
left2 = tk.PhotoImage(file = "assets/leftChicken2.png")
leftImg = [left1,left2]

right1 = tk.PhotoImage(file = "assets/rightChicken.png")
right2 = tk.PhotoImage(file = "assets/rightChicken2.png")
rightImg = [right1,right2]

playerImages = [leftImg , rightImg]

currentFrame = 0
player = canvas.create_image(320, 320, image=playerImages[0][currentFrame])
canvas.image = player  # keep reference

def loadSprite(path)

# Track which keys are down
keys_down = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
move_speed = 5

def on_key_press(event):
    if event.keysym in keys_down:
        keys_down[event.keysym] = True

def on_key_release(event):
    if event.keysym in keys_down:
        keys_down[event.keysym] = False

# Game loop: move player based on keys_down
def game_loop():
    dx = dy = 0
    if keys_down['Up']:
        dy -= move_speed
    if keys_down['Down']:
        dy += move_speed
    if keys_down['Left']:
        dx -= move_speed
    if keys_down['Right']:
        dx += move_speed
    if dx or dy:
        canvas.move(player, dx, dy)
    win.after(30, game_loop)  # ~33 FPS

# Bind press/release
win.bind("<KeyPress>", on_key_press)
win.bind("<KeyRelease>", on_key_release)

# Start loop
game_loop()
win.mainloop()

