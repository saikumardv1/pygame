import pygame as p
import random
import math
p.init()  #initialize pygame

screen=p.display.set_mode((800,600))
p.display.set_caption("Space Invaders")
icon=p.image.load('ufo.png')
p.display.set_icon(icon)

background = p.image.load('background.png')
p.mixer.music.load("background.wav")
p.mixer.music.play(-1)

#player
playerimg=p.image.load('space-invaders.png')
playerX=370
playerY=480
playerX_change=0

#list of enemies
num_of_enemies = 5
enemyimg=p.image.load('monster.png')
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
for i in range(num_of_enemies):
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet
# state "ready" - to fire   "firing" - in motion
bulletimg=p.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

# score
score = 0
text = p.font.Font("freesansbold.ttf",32)
textX =10
textY =10

over_font = p.font.Font("freesansbold.ttf",64)
author = p.font.Font("freesansbold.ttf",32)
def show_score(x,y):
    s=text.render("Score :"+ str(score), True, (255,255,255))
    screen.blit(s, (x,y))

def game_over():
    s=over_font.render("GAME OVER", True, (255,255,255))
    s1=author.render(chr(0xa9)+" sai kumar d v", True, (255,255,255))
    screen.blit(s, (200,250))
    screen.blit(s1, (290,320))

#player function

def player(x,y):
    screen.blit(playerimg, (x,y))

#enemy function

def enemy(x,y):
    screen.blit(enemyimg, (x,y))

# bullet motion function

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16,y+10))
# checking whether enemy and bullet are colliding
def isCollision(enemyX,enemyY,bulletX,bulletY):
    d=math.sqrt((enemyX-bulletX)**2+(enemyY-bulletY)**2)
    if d<27:
        return True
    else:
        return False

# running the game window infinitely
running= True
while running:
    screen.fill((0,16,0))  #rgb

    screen.blit(background,(0,0))

    for i in p.event.get():
        if i.type == p.QUIT:  #stopping game
            running=False

        if i.type == p.KEYDOWN:
            if i.key == p.K_LEFT:
                playerX_change = -5
            if i.key == p.K_RIGHT:
                playerX_change = 5

            if i.key == p.K_SPACE and bullet_state=="ready":
                bullet_sound = p.mixer.Sound("laser.wav")
                bullet_sound.play()
                bulletX = playerX   # to fire bullet from current co ordinate of ship
                fire_bullet(bulletX, bulletY)
        if i.type == p.KEYUP:
            if i.key == p.K_LEFT or i.key == p.K_RIGHT:
                playerX_change = 0
    playerX+=playerX_change
    #boundaries for player 
    if playerX<=0:
        playerX=0
    elif playerX>=736:  ##800 - 64 px
        playerX=736

    for i in range(num_of_enemies):

        if enemyY[i]>=440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over()
            bullet_state="running"
            playerX=370
            break

        enemyX[i]+=enemyX_change[i]
        #boundaries for enemy
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:  ##800 - 64 px
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            e_sound = p.mixer.Sound("explosion.wav")
            e_sound.play()
            bulletY = 480
            bullet_state= "ready"
            score += 1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i])

    # motion of the bullet
    if bulletY<=0:
        bullet_state = "ready"
        bulletY=480
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)

    show_score(textX,textY)
        
    p.display.update()