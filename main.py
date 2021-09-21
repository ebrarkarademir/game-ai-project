import math
import pygame
import random
import neat
import os
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

generation = 1
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT = pygame.font.SysFont("comicsans", 100)
FONT2 = pygame.font.SysFont("comicsans", 30)

EVENT = pygame.USEREVENT + 1

FPS = 60
pygame.display.set_caption("jumping_game_ai")

class Box():

    def __init__(self, x, y):
        self.vel = 8
        self.rect = pygame.Rect(x, y, 30, 70)
        self.is_jump = False
        self.score = 0
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.is_run = True
        self.is_jump = False
        self.is_slide = False
        self.step_index = 0
        self.slide_index = 0

    def update(self):
        if self.is_run:
            self.step_index += 0.2

        if self.is_jump:
            self.rect.y -= self.vel
            self.vel -= 0.4

        if self.is_slide:
            self.rect.height = 20
            self.rect.y = HEIGHT / 2 + 50
            self.slide_index += 1

            if self.slide_index >= 50:
                self.slide_index = 0
                self.is_slide = False
                self.is_run = True
                self.rect.y = HEIGHT / 2
                self.rect.height = 70

        if self.vel < -9:
            self.is_jump = False
            self.is_run = True
            self.vel = 8

        if self.step_index >= 3:
            self.step_index = 0


    def collide(self, obstacle, score):
        if self.rect.colliderect(obstacle):
            self.score = int(score)
            return True
        else:
            return False

    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)

class Obstacle():

    def __init__(self, x, y, obstacle_vel, height):
        self.x = x
        self.y = y
        self.vel = obstacle_vel
        self.rect = pygame.Rect(x, y + 70 - height, 30, height)
        self.passed = False

    def update(self):
        self.rect.x -= self.vel
        if self.rect.x < 0 - self.rect.width:
            self.passed = True

    def draw(self):
        pygame.draw.rect(WIN, BLACK, self.rect)

    def check_high(self):
        if self.rect.height == 50:
            return 1
        if self.rect.height == 40:
            return 0

def draw_window(boxes, obstacles, game_over, score, generation, alive, level_one, level_two, level_three):
    WIN.fill(WHITE)

    score_text = FONT2.render(str(int(score)), 1, BLACK)
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - 200))

    for box in boxes:
        box.draw()
    for obstacle in obstacles:
        obstacle.draw()

    pygame.draw.line(WIN, BLACK, (0, HEIGHT/2 + 70), (WIDTH, HEIGHT/2 + 70))

    generation_text = FONT2.render("Generation : " + str(generation), 1, BLACK)
    alive_text = FONT2.render("Alive : "+ str(alive), 1, BLACK)
    WIN.blit(generation_text, (30, HEIGHT/2 + 100))
    WIN.blit(alive_text, (30, HEIGHT / 2 + 120))


    if level_one:
        level_one_text = FONT2.render("LEVEL 1", 1, BLACK)
        WIN.blit(level_one_text, (WIDTH / 2 - level_one_text.get_width() / 2, HEIGHT / 2 - 150))
    if level_two:
        level_two_text = FONT2.render("LEVEL 2", 1, BLACK)
        WIN.blit(level_two_text, (WIDTH / 2 - level_two_text.get_width() / 2, HEIGHT / 2 - 150))
    if level_three:
        level_three_text = FONT2.render("LEVEL 3", 1, BLACK)
        WIN.blit(level_three_text, (WIDTH / 2 - level_three_text.get_width() / 2, HEIGHT / 2 - 150))

    pygame.display.update()

def remove(index, boxes, ge, nets):
    boxes.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2+dy**2)

def main(genomes, config):
    global generation, FPS
    score = 0
    obstacle_vel = 4
    boxes = []
    obstacles = [Obstacle(WIDTH , HEIGHT / 2, obstacle_vel, 50)]
    alive = 0
    level_count = 0
    level_one = True
    level_two = False
    level_three = False

    ge = []
    nets = []
    for genome_id, genome in genomes:
        boxes.append(Box(WIDTH/2 - 200 , HEIGHT/2))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    game_over = False
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == EVENT:
                pass

        keys_pressed = pygame.key.get_pressed()

        if len(boxes) == 0:
            generation += 1
            break

        alive = len(boxes)

        for i,box in enumerate(boxes):

            output = nets[i].activate((box.rect.y, box.rect.height, distance((box.rect.x, box.rect.y), obstacles[0].rect.midtop), obstacles[0].rect.height))
            if box.is_jump is False and box.is_slide is False and output[0] > 0.5:
                box.is_slide = True
            elif box.is_jump is False and box.is_slide is False and output[1] > 0.5:
                box.is_jump = True
            box.update()

        for obstacle in obstacles:
            if obstacle.passed:
                obstacles.remove(obstacle)
                level_count += 1
                if level_count >= 8 and level_count <= 20:
                    level_two = True
                    level_one = False
                    obstacles.append(Obstacle(WIDTH, HEIGHT / 2 - 60, obstacle_vel, 30))
                elif level_count >= 20:
                    level_two = False
                    level_three = True
                    i = random.randrange(1, 3)
                    if i == 1:
                        obstacles.append(Obstacle(WIDTH, HEIGHT / 2 - 60, obstacle_vel, 30)) # high
                    elif i == 2:
                        obstacles.append(Obstacle(WIDTH , HEIGHT / 2, obstacle_vel, 50)) # middle
                else:
                    obstacles.append(Obstacle(WIDTH , HEIGHT / 2, obstacle_vel, 50)) # only normal obstacles
            for i, dino in enumerate(boxes):
                if dino.collide(obstacle, score):
                    ge[i].fitness -= 1
                    remove(i, boxes, ge, nets)
                    if not boxes:
                        # game_over = True
                        break

            obstacle.update()

        if game_over is False:
            score += 1/FPS

        if keys_pressed[pygame.K_KP_MINUS]:
            FPS = 60
        if keys_pressed[pygame.K_KP_PLUS]:
            FPS = 360

        draw_window(boxes, obstacles, game_over, score, generation, alive, level_one, level_two, level_three)

def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(main, 10000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join("assets", "config.txt")
    run(config_path)

