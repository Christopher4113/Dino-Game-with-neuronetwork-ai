import pygame
import os
import random
import sys

pygame.init()

Screen_height = 600
Screen_width = 1100

Screen = pygame.display.set_mode((Screen_width,Screen_height))

Running = [pygame.image.load(os.path.join("Assets/Dino","DinoRun1.png")),pygame.image.load(os.path.join("Assets/Dino","DinoRun2.png"))]

Jumping = pygame.image.load(os.path.join("Assets/Dino","DinoJump.png"))

Ducking = [pygame.image.load(os.path.join("Assets/Dino","DinoDuck1.png")),pygame.image.load(os.path.join("Assets/Dino","DinoDuck2.png"))]

Small_Cactus = [pygame.image.load(os.path.join("Assets/Cactus","SmallCactus1.png")),pygame.image.load(os.path.join("Assets/Cactus","SmallCactus2.png")),pygame.image.load(os.path.join("Assets/Cactus","SmallCactus3.png"))]

Large_Cactus = [pygame.image.load(os.path.join("Assets/Cactus","LargeCactus1.png")),pygame.image.load(os.path.join("Assets/Cactus","LargeCactus2.png")),pygame.image.load(os.path.join("Assets/Cactus","LargeCactus3.png"))]

Bird = [pygame.image.load(os.path.join("Assets/Bird","Bird1.png")),pygame.image.load(os.path.join("Assets/Bird","Bird2.png"))]

Cloud = pygame.image.load(os.path.join("Assets/Other","Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other","Track.png"))

FONT = pygame.font.Font('freesansbold.ttf',20)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 0.5

    def __init__(self):
        self.duck = Ducking
        self.jump = Jumping
        self.run = Running







def main():
    run = True

    clock = pygame.time.Clock()
    player = Dinosaur()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
        
        Screen.fill((255,255,255))
        userInput = pygame.key.get_pressed()
        player.draw(Screen)
        player.update(userInput)

        
        clock.tick(30) #30 fps
        pygame.display.update()




main()