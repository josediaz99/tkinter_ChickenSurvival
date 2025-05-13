import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk,ImageOps
import pygame
import time
import math
import random

pygame.mixer.init()

win = Tk()
win.geometry('1024x1024')
win.resizable(width=False, height=False)
win.title("coyote Survival")

def exit_fullscreen(event):
    win.attributes("-fullscreen", False)

win.bind("<Escape>", exit_fullscreen)

# Layout
fr = Frame(win)
fr.grid()
canvas = Canvas(fr, background='black', width=1000, height=1000)
canvas.grid(column=0, row=1)

game_started = False
start_text = canvas.create_text(500, 500, text="Press SPACE to Start", fill="white", font=("Arial", 30))

#====================================================================
#                          Load background
lastAttackTime = 0
coin = None
bg_img = PhotoImage(file="assets/background.png")
canvas.create_image(0, 0, image=bg_img, anchor=NW)

#===========================================================================
#                         load barriers
barriers = [#x1, x2, y1, y2
    (200,400,300,420)    
]

def draw_barriers(canvas, coords_list):
    for coords in coords_list:
        canvas.create_rectangle(*coords, fill='red', outline='black')

draw_barriers(canvas,barriers)

def will_collide(new_x, new_y):
    px, py = new_x, new_y
    # 50x50 is your player size
    for x1, y1, x2, y2 in barriers:
        if (px + 25 > x1 and px - 25 < x2 and
            py + 25 > y1 and py - 25 < y2):
            return True
    return False

#====================================================================
#                        load sounds
bgMusic = pygame.mixer.Sound("assets/sounds/backgroundSound.mp3")#sound by alexis g angeles from pixabay
bgMusic.play(-1)
endSound = pygame.mixer.Sound("assets//sounds/endGame.mp3")#sound by nematoki on pixabay
newCoyote = pygame.mixer.Sound("assets/sounds/newCayote.mp3")#by freesound_community on pixabay
playerAttack = pygame.mixer.Sound("assets/sounds/attackSound.mp3")
coyoteAttack = pygame.mixer.Sound("assets/sounds/coyoteAttack.mp3")
shotgunBlast = pygame.mixer.Sound("assets/sounds/shotgunBlast.mp3")
coinSound = pygame.mixer.Sound("assets/sounds/coin.mp3")
#==================================================================
#                       load token
coinImg = Image.open("assets/wholeEgg.png").resize((30,30))
coinTK = ImageTk.PhotoImage(coinImg)

coinsCollected = 0
coinText = None
def updateCoinText():
    global coinText
    if coinText:
        canvas.delete(coinText)
    coinText = canvas.create_text(
        980, 20,
        text=f"Coins: {coinsCollected}",
        fill="yellow",
        font=("Arial", 20),
        anchor=NE,
        tags="coinDisplay"
    )


def spawnCoin():
    global coin
    if coin:
        canvas.delete(coin)
        
    x = random.randint(50,950)
    y = random.randint(50,950)
    coin = canvas.create_image(x,y,image= coinTK, tags="coin")
    
def canCollect():
    global coinsCollected
    if coin:  # make sure coin exists
        px, py = canvas.coords(player)
        cx, cy = canvas.coords(coin)
        distance = ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
        if distance < 40:
            coinSound.play()
            canvas.delete(coin)
            coinsCollected += 1  
            updateCoinText()   
            spawnCoin()          

        
spawnCoin()
updateCoinText()
#==================================================================
#                       load player weapon
rightShotgun = Image.open("assets/shotgun.png").resize((100, 80))
leftShotgun = ImageOps.mirror(rightShotgun)

# Pre-convert both to PhotoImage
shotgunImg = [ImageTk.PhotoImage(leftShotgun), ImageTk.PhotoImage(rightShotgun)]

#================================================================
#                       load hearts
hearts = Image.open("assets/hearts.png")
hearts = hearts.resize((30,30))
heartsTK = ImageTk.PhotoImage(hearts)
canvas.heartImage = heartsTK

current_heart = None
heart_timer = None

def spawn_heart():
    global current_heart, heart_timer

    # If there's a heart already, don't spawn another
    if current_heart:
        return

    x = random.randint(50, 950)
    y = random.randint(50, 950)
    current_heart = canvas.create_image(x, y, image=heartsTK, anchor=NW)

    # Set timer to remove heart after 5 seconds
    heart_timer = canvas.after(5000, remove_heart)

def remove_heart():
    global current_heart, heart_timer

    if current_heart:
        canvas.delete(current_heart)
        current_heart = None

    # Set timer to spawn the next heart in 5 seconds
    heart_timer = canvas.after(3000, spawn_heart)


def check_heart_collision():
    global playerHealth, current_heart

    if current_heart:
        player_bbox = canvas.bbox(player)
        heart_bbox = canvas.bbox(current_heart)

        if player_bbox and heart_bbox:
            overlap = not (
                player_bbox[2] < heart_bbox[0] or
                player_bbox[0] > heart_bbox[2] or
                player_bbox[3] < heart_bbox[1] or
                player_bbox[1] > heart_bbox[3]
            )
            if overlap:
                canvas.delete(current_heart)
                current_heart = None
                playerHealth = min(playerHealth + 1, 10)
                showHealth(canvas, playerHealth, heartsTK)

                # Start the next spawn timer after 5 seconds
                canvas.after(5000, spawn_heart)

#==================================================================
#                       load player
initialPlayerPos = (400,400)
playerHealth = 10


def showHealth(canvas,health,heartImage):
    canvas.delete("heart")
    for i in range(health):
        canvas.create_image(10+i*35,10, anchor=NW, image = heartImage, tags= "heart")
        
showHealth(canvas, playerHealth,heartsTK)


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

player = canvas.create_image(*initialPlayerPos, image=playerImgs[lookRight][currentFrame])
shotgun = canvas.create_image(*initialPlayerPos, image=shotgunImg[lookRight])

canvas.image = player 

def drawPlayer(x, y, facing):
    global currentFrame
    currentFrame += 1
    frame = currentFrame % 2

    canvas.itemconfig(player, image=playerImgs[facing][frame])
    canvas.move(player, x, y)

    # Update shotgun image and position
    canvas.itemconfig(shotgun, image=shotgunImg[facing])
    px, py = canvas.coords(player)
    canvas.coords(shotgun, px + (10 if facing else -10), py - 5)

#============================================================
#                           load coyote
initialCoyotePos = (0,0)
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

coyote = canvas.create_image(*initialCoyotePos,image = coyoteImgs[lookRight][enemyFrame%3])

                             
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
        x = x*.8
        y = y*.8
        
    return[x,y,lookRight]
    
def reachedPlayer():
    """
    looks at the difference in the players and coyotes position to determine if the coyote can attack

    Returns:
        _type_: bool
    """
    chickenCords = canvas.coords(player)
    coyoteCords = canvas.coords(coyote)
    
    x = chickenCords[0] - coyoteCords[0]
    y = chickenCords[1] - coyoteCords[1]
    
    xDiff = abs(x)
    yDiff = abs(y)
    
    distance = xDiff**2 + yDiff**2
    if(distance**.5 < 100):
        return True
    return False
    
def attackPlayer():
    global playerHealth, lastAttackTime
    currentTime = time.time()
    if currentTime - lastAttackTime >= 1:
        playerHealth -= 1
        coyoteAttack.play()
        lastAttackTime = currentTime
        showHealth(canvas, playerHealth, heartsTK)
        if playerHealth <= 0:
            gameOver()
            
def gameOver():
    global game_started
    game_started = False
    canvas.create_rectangle(0, 0, 1000, 1000, fill="black", outline="black", tags="gameover")
    canvas.create_text(500, 400, text="GAME OVER", fill="red", font=("Arial", 60), tags="gameover")
    canvas.create_text(500, 500, text="Press SPACE to Restart", fill="white", font=("Arial", 30), tags="gameover")

    
#======================================================================================
# Track which keys are down
keys_down = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
move_speed = 5

def on_key_press(event):
    global game_started, playerHealth
    if not game_started:
        if event.keysym == "space":
            spawn_heart()
            canvas.delete("gameover")  # Clear game over screen
            canvas.delete("heart")     # Clear old hearts
            playerHealth = 10
            updateCoinText()
            coinsCollected = 0
            showHealth(canvas, playerHealth, heartsTK)
            
            #reset player & coyotw
            canvas.coords(player, *initialPlayerPos)
            canvas.coords(shotgun, *initialPlayerPos)
            canvas.coords(coyote, *initialCoyotePos)
            
            game_started = True
            canvas.delete(start_text)
            
            game_loop()
        return
    if event.keysym in keys_down:
        keys_down[event.keysym] = True
    if event.keysym == "space":
        shotgunBlast.play()
        if reachedPlayer():
            pushBack()
            
 
def pushBack():
    px,py = canvas.coords(player)
    cx,cy = canvas.coords(coyote)
    
    dx = cx-px
    dy = cy-py
    
    angle = math.atan2(dy,dx) #gets the radians
    
    push = 500
    
    pushX = math.cos(angle) * push
    pushY = math.sin(angle) * push
    
    canvas.move(coyote,pushX,pushY)
    canvas.move(player,-pushX*.1,-pushY*.1)

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
        # Get current player position
        px, py = canvas.coords(player)
        new_x = px + dx
        new_y = py + dy

        # Check for collision before moving and make sure we can still move if we collide
        if not will_collide(new_x, new_y):
            drawPlayer(dx, dy, lookRight)
        elif not will_collide(px,new_y):
            drawPlayer(0,dy,lookRight)
        elif not will_collide(new_x,py):
            drawPlayer(dx,0,lookRight)

    move = chasePlayer()
    drawCoyote(move[0],move[1],move[2])
    if reachedPlayer():
        attackPlayer()
    
    #get coin if we can
    canCollect()
    check_heart_collision()
    
    win.after(33, game_loop)  # ~33 FPS

# Bind press/release
win.bind("<KeyPress>", on_key_press)
win.bind("<KeyRelease>", on_key_release)

# Start loop
#game_loop()
win.mainloop()

