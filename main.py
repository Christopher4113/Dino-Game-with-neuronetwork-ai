import pygame
import os
import random
import sys
import neat
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

# Set up the display
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD_IMGS = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
             pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD_IMAGE = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5
    Y_POS_DUCK = 340
    DUCK_DURATION = 5  # Duck duration in seconds

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.duck_start_time = 0  # Initialize duck start time

        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self):
        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

        # Check if 5 seconds have passed since ducking started
        current_time = pygame.time.get_ticks()
        if (current_time - self.duck_start_time) / 1000 > self.DUCK_DURATION:
            self.dino_duck = False
            self.dino_run = True

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

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


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

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

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
        super().__init__(image, 0)  # Bird is always of type 0
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 10:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, ge, nets, points
    clock = pygame.time.Clock()
    points = 0

    obstacles = []
    dinosaurs = []
    ge = []
    nets = []

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f'Points:  {str(points)}', True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))

    def statistics():
        global dinosaurs, game_speed, ge
        text_1 = FONT.render(f'Dinosaurs Alive:  {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480))
        SCREEN.blit(text_3, (50, 510))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)

        if len(dinosaurs) == 0:
            break

        if len(obstacles) == 0:
            obstacle_type = random.randint(0, 2)
            if obstacle_type == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif obstacle_type == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD_IMGS))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()

            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.dino_rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1
                    remove(i)

                    if isinstance(obstacle, Bird):
                        # Adjust dinosaur behavior when encountering a bird
                        if not dinosaur.dino_duck:
                            dinosaur.dino_duck = True
                            dinosaur.duck_start_time = pygame.time.get_ticks()
                            dinosaur.dino_run = False
                            dinosaur.dino_jump = False
                    else:
                        dinosaur.dino_duck = False
                        dinosaur.dino_run = True
                        dinosaur.dino_jump = False

        for i, dinosaur in enumerate(dinosaurs):
            ge[i].fitness += 0.1

            if len(obstacles) > 0:
                closest_obstacle = obstacles[0]
                obstacle_type = 1 if isinstance(closest_obstacle, Bird) else 0
                output = nets[i].activate((
                    dinosaur.dino_rect.y,
                    distance((dinosaur.dino_rect.x, dinosaur.dino_rect.y), closest_obstacle.rect.midtop),
                    obstacle_type
                ))

                if obstacle_type == 0:  # Cactus
                    if output[0] > 0.5 and dinosaur.dino_rect.y == dinosaur.Y_POS:
                        dinosaur.dino_jump = True
                        dinosaur.dino_duck = False
                        dinosaur.dino_run = False
                        # Penalize unnecessary jumps
                        ge[i].fitness -= 0.05
                elif obstacle_type == 1:  # Bird
                    if output[1] > 0.5 and dinosaur.dino_rect.y == dinosaur.Y_POS:
                        if not dinosaur.dino_duck:
                            dinosaur.dino_duck = True
                            dinosaur.duck_start_time = pygame.time.get_ticks()
                            dinosaur.dino_run = False
                            dinosaur.dino_jump = False
                    else:
                        if isinstance(closest_obstacle, Bird):
                            if dinosaur.dino_rect.x > closest_obstacle.rect.x + closest_obstacle.rect.width:
                                # Dinosaur has passed the bird, stop ducking
                                dinosaur.dino_duck = False
                                dinosaur.dino_run = True
                                dinosaur.dino_jump = False
                        else:
                            dinosaur.dino_duck = False
                            dinosaur.dino_run = True
                            dinosaur.dino_jump = False

        background()
        statistics()
        score()
        clock.tick(30)
        pygame.display.update()




def run(config_path):
    global pop
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    run(config_path)
