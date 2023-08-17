import pygame
import random
import math
from pygame import mixer

#intialize the pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((800,600))

#bg
bg = pygame.image.load('background.png')

#bg sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet
# ready : you can't see the bullet on the screen
# Fire : the bullet is curreently moving

bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score = 0
fontScore = pygame.font.Font("freesansbold.ttf", 32)  

#game over text
fontGameOver = pygame.font.Font("freesansbold.ttf", 64)  

#functions to set the position of the objects
def player(x,y):
    screen.blit(playerImg,(x,y))

def game_over_text():
    over_text = fontGameOver.render("Game Over", True, (255,255,255))
    screen.blit(over_text,(200,250))

def enemy(x ,y ,i ):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow((enemyX-bulletX),2))+(math.pow((enemyY-bulletY),2)))
    if distance < 27:
        return True
    else:
        return False    

#game loop
running = True
enemy_killed = False

while running:
    
    #bg color
    screen.fill(( 0, 0, 0))
    
    #bg img
    screen.blit(bg,(0,0))
    
    # Render and display the score text
    score_text = fontScore.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # checking keyboard stroke is pressed or not    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    # get the current x coordinates of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
   

    # adjusting boundries to the spaceship
    playerX += playerX_change 
    if playerX <= 0:
        playerX = 0 
    elif playerX >= 736:
        playerX = 736

    # enemy movement    
    for i in range(num_of_enemies):
        
        #Game Over
        if enemyY[i] > 540:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break    
        enemyX[i] += enemyX_change[i]  
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] -= 4
            enemyY[i] += enemyY_change[i]
        
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        
        if collision:
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()        
            bulletY = 480
            bullet_state = "ready"   
            score += 1

            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
     

    player(playerX,playerY)
    pygame.display.update()
    
