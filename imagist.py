import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk,ImageOps
import pygame

pygame.mixer.init()

win = Tk()
win.geometry('1024x1024')
win.resizable(width=False, height=False)
win.title("Imagist")

# Layout
fr = Frame(win)
fr.grid()
canvas = Canvas(fr, background='black', width=1024, height=1024)
canvas.grid(column=0, row=1)

# Load background
bg_img = PhotoImage(file="assets/background.png")
canvas.create_image(0, 0, image=bg_img, anchor=NW)

#  load sounds and start background sound
bgMusic = pygame.mixer.Sound("assets/backgroundMusic.wav")
bgMusic.play()

endSound = pygame.mixer.Sound("assets/endGame.mp3")#sound by nematoki on pixabay
newCoyote = pygame.mixer.Sound("assets/newCayote.mp3")#by freesound_community on pixabay
playerAttack = pygame.mixer.Sound("assets/attackSound.mp3")
#==================================================================
#                       load player
lookRight = True
# Chicken left images
left1 = Image.open("assets/leftChicken.png").resize((50, 50))
left2 = Image.open("assets/leftChicken2.png").resize((50, 50))
leftImg = [ImageTk.PhotoImage(left1), ImageTk.PhotoImage(left2)]

# Chicken right images
right1 = Image.open("assets/rightChicken.png").resize((50, 50))
right2 = Image.open("assets/rightChicken2.png").resize((50, 50))
rightImg = [ImageTk.PhotoImage(right1), ImageTk.PhotoImage(right2)]

#keeps track of where we face and the image by keeping it in seporate lists
playerImgs = [leftImg , rightImg]

currentFrame = 0
player = canvas.create_image(320, 320, image=playerImgs[lookRight][currentFrame])
canvas.image = player 

def drawPlayer(x,y,facing):
    global currentFrame
    currentFrame += 1
    frame = currentFrame%2
    canvas.itemconfig(player,image = playerImgs[facing][frame])
    canvas.move(player,x,y)
    
#============================================================
#                           load coyote

#coyote animation
coyote1 = Image.open("assets/coyote1.png").resize((100, 75))
coyote2 = Image.open("assets/coyote2.png").resize((100, 75))
coyote3 = Image.open("assets/coyote3.png").resize((100, 75))
leftCoyoteImg = [
    ImageTk.PhotoImage(ImageOps.mirror(coyote1)),
    ImageTk.PhotoImage(ImageOps.mirror(coyote2)),
    ImageTk.PhotoImage(ImageOps.mirror(coyote3))
]
rightCoyoteImg = [
    ImageTk.PhotoImage(coyote1),
    ImageTk.PhotoImage(coyote2),
    ImageTk.PhotoImage(coyote3)
]
coyoteImgs = [
   leftCoyoteImg,
   rightCoyoteImg
]

enemyFrame = 0

coyote = canvas.create_image(0,0,image = coyoteImgs[lookRight][enemyFrame%3])

#======================================================================================
#                               
def drawCoyote(x,y,facing):
    global enemyFrame
    enemyFrame += 1
    frame = enemyFrame%3
    canvas.itemconfig(coyote,image = coyoteImgs[facing][frame])
    canvas.move(coyote,x,y)
    
def chasePlayer():
    """
    takes in the positions of the player and the chicken and returns and updated x,y
    as well as the position the Coyote should be in
    """
    chiCords = canvas.coords(player) #[x,y]
    coyCords = canvas.coords(coyote)
    
    global lookRight
    x = 0
    y = 0
    #check if we need to move the x
    if chiCords[0] > coyCords[0]:
        x = move_speed*1.2
        lookRight = True
    if chiCords[0] < coyCords[0]:
        x = -move_speed*1.2
        lookRight = False
    #check if wee need to move the y
    if chiCords[1] < coyCords[1]:
        y = -move_speed*1.2
    if chiCords[1] > coyCords[1]:
        y = move_speed*1.2
    if x and y:
        x = x*.9
        y = y*.9
        
    return[x,y,lookRight]
    
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
    global lookRight
    dx = dy = 0
    if keys_down['Up']:
        dy -= move_speed
    if keys_down['Down']:
        dy += move_speed
    if keys_down['Left']:
        lookRight = False
        dx -= move_speed
    if keys_down['Right']:
        dx += move_speed
        lookRight = True
    if dx or dy:
        drawPlayer(dx,dy,lookRight)
    move = chasePlayer()
    drawCoyote(move[0],move[1],move[2])
    win.after(33, game_loop)  # ~33 FPS

# Bind press/release
win.bind("<KeyPress>", on_key_press)
win.bind("<KeyRelease>", on_key_release)

# Start loop
game_loop()
win.mainloop()

