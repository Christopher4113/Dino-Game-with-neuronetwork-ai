import pygame
import os
import random
import sys
import neat
import math

# Initialize Pygame
pygame.init()

GEN = 0

# Screen dimensions
Screen_height = 600
Screen_width = 1100

# Set up the display
Screen = pygame.display.set_mode((Screen_width, Screen_height))

# Load images
Running = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

Jumping = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

Ducking = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

Small_Cactus = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

Large_Cactus = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

Bird_imgs = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
             pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

Cloud_image = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5
    Y_POS_DUCK = 340

    def __init__(self):
        self.duck_img = Ducking
        self.run_img = Running
        self.jump_img = Jumping

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL

        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
    
    def is_on_ground(self):
        return self.dino_rect.y == self.Y_POS

    def update(self):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.dino_run = True

    def draw(self, Screen):
        Screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Cloud:
    def __init__(self, image, screen_width):
        self.image = image
        self.screen_width = screen_width
        self.width = self.image.get_width()
        self.x = self.screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)

    def update(self, game_speed):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = self.screen_width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, Screen):
        Screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = Screen_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, Screen):
        Screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, Screen):
        if self.index >= 9:
            self.index = 0
        Screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def distance(pos_a,pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def main(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, GEN
    run = True
    clock = pygame.time.Clock()
    cloud = Cloud(Cloud_image, Screen_width)
    game_speed = 14
    x_pos_bg, y_pos_bg = 0, 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    GEN += 1
    nets, ge, dino = [], [], []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dino.append(Dinosaur())
        g.fitness = 0
        ge.append(g)

    def score(gen):
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        Screen.blit(text, textRect)
        text = STAT_FONT.render("Gen: " + str(gen), 1, (0, 0, 0))
        Screen.blit(text, (10, 10))

    def background():
        global game_speed, x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        Screen.blit(BG, (x_pos_bg, y_pos_bg))
        Screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            Screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        jump_cooldown = 5
        jump_cool = [0] * len(dino)

        for x, d in enumerate(dino):
            ge[x].fitness += 0.1

            # Determine inputs for the neural network
            closest_obstacle = obstacles[0].rect if obstacles else None
            obstacle_type = obstacles[0].type if obstacles else None
            output = nets[x].activate((d.dino_rect.y,distance((d.dino_rect.x,d.dino_rect.y),closest_obstacle.rect.midtop)))

            if output[0] > 0.5 and d.is_on_ground() and jump_cooldown[x] == 0:  # Jump condition
                d.dino_jump = True
                d.dino_run = False
                d.dino_duck = False
                jump_cooldown[x] = jump_cool

            if jump_cooldown[x] > 0:
                jump_cooldown[x] -= 1 
            elif obstacle_type == 2 and not d.dino_jump:  # Duck condition (type 2 is Bird)
                d.dino_duck = True
                d.dino_run = False
                d.dino_jump = False
            else:
                d.dino_run = True
                d.dino_jump = False
                d.dino_duck = False

            d.update()

        for obstacle in list(obstacles):
            obstacle.update()
            for x, d in enumerate(dino):
                if obstacle.rect.colliderect(d.dino_rect):
                    ge[x].fitness -= 1
                    nets.pop(x)
                    ge.pop(x)
                    dino.pop(x)

        if len(dino) == 0:
            break

        if len(obstacles) == 0:
            obstacle_type = random.randint(0, 2)
            if obstacle_type == 0:
                obstacles.append(SmallCactus(Small_Cactus))
            elif obstacle_type == 1:
                obstacles.append(LargeCactus(Large_Cactus))
            else:
                obstacles.append(Bird(Bird_imgs))

        Screen.fill((255, 255, 255))
        for d in dino:
            d.draw(Screen)

        cloud.draw(Screen)
        cloud.update(game_speed)

        background()
        score(GEN)

        for obstacle in obstacles:
            obstacle.draw(Screen)

        pygame.display.update()
        clock.tick(30)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    run(config_path)

