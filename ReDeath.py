import pygame
import os
import random
import time
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

#Basics
HEIGHT = 1080
WIDTH = 1920
ACC = 0.75
FRIC = -0.12
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Re:Death")

#Timer
def timeFormat(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return("{0}".format(int(sec)))

starttime = time.time()
#Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #Texture
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0,0,255))
        self.rect = self.surf.get_rect()
        #Speed
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)


    #Movement
    def move(self):
        self.acc = vec(0,0.5)
 
        pressed_keys = pygame.key.get_pressed()
            
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x < 0:
            self.pos.x = 0
     
        self.rect.midbottom = self.pos
    #Jump
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -20

                
    #Prevents you from falling through blocks
    def update(self):
        hits = pygame.sprite.spritecollide(player1, platforms, False)
        if player1.vel.y > 0:        
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
    
#Set's platform information
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(200,WIDTH-30), random.randint(600, HEIGHT-20)))

    def move(self):
        pass

#Makes sure platforms aren't too close
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.right - entity.rect.left) < 50) and (abs(platform.rect.left - entity.rect.right) < 50):
                return True
        C = False

#Generates New Platforms
def platformGen():
    while len(platforms) < 7 :
        height = random.randrange(0,50)
        p  = platform()   
        C = True
        while C:      
            p  = platform()     
            p.rect.center = (random.randrange(WIDTH-50, WIDTH), random.randrange(0, HEIGHT - height))
            C = check(p, platforms)
        platforms.add(p)
        allsprites.add(p)



plat1 = platform()
player1 = Player()

plat1.surf = pygame.Surface((WIDTH, 20))
plat1.surf.fill((255,0,0))
plat1.rect = plat1.surf.get_rect(center = (50, HEIGHT - 10))

allsprites = pygame.sprite.Group()
allsprites.add(plat1)
allsprites.add(player1)

platforms = pygame.sprite.Group()
platforms.add(plat1)

for x in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    allsprites.add(pl)

#Game
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_UP:
                player1.jump()

    #Offloads platforms
    if player1.rect.right <= WIDTH / 3:
        player1.pos.x -= abs(player1.vel.x)
        for plat in platforms:
            plat.rect.x -= abs(player1.vel.x)
            if plat.rect.right <= 0:
                plat.kill()

    screen.fill((0,0,0))
    player1.update()
    platformGen()
    for entity in allsprites:
        screen.blit(entity.surf, entity.rect)
        entity.move()
    
    font = pygame.font.Font('freesansbold.ttf', 32)
    #Diplays score on screen
    endtime = time.time()
    diff = endtime - starttime
    timeformatted = timeFormat(diff)
    timetext = font.render(timeformatted + " seconds", True, (255, 255, 255), (0,0,0))
    timeRect = timetext.get_rect()
    timeRect.center = (WIDTH // 2, 40)
    screen.blit(timetext, timeRect)

    #Game Over Screen
    if player1.rect.top > HEIGHT:
        for entity in allsprites:
            entity.kill()
            screen.fill((0,0,0))
            endtime = time.time()
            diff = endtime - starttime
            timeformatted = timeFormat(diff)

            #Game Over Text
            gameover = font.render('Game Over', True, (255, 0, 0), (0,0,0))
            deathRect = gameover.get_rect()
            deathRect.center = (WIDTH // 2, HEIGHT // 3)
            screen.blit(gameover, deathRect)
            highscore = font.render("Highscore", True, (255, 255, 255), (0,0,0))
            highRect = highscore.get_rect()
            highRect.center = (WIDTH // 2, HEIGHT - (HEIGHT//3 + 40))
            screen.blit(highscore, highRect)
            timetext = font.render(timeformatted + " seconds", True, (255, 255, 255), (0,0,0))
            timeRect = timetext.get_rect()
            timeRect.center = (WIDTH // 2, HEIGHT - (HEIGHT//3))
            screen.blit(timetext, timeRect)
            pygame.display.update()

            time.sleep(10)
            pygame.quit()

    
    #Updates the screen
    pygame.display.update()
    FramePerSec.tick(FPS)