import math
import pygame
import random
import neat
import os
pygame.init()

# daha temiz objeler
# stats
# oyunun zorlaştırılması
# nesillerin yenilenmesi

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

RUNNING = [pygame.image.load(os.path.join("assets", "frame1_.png")),
           pygame.image.load(os.path.join("assets", "frame2_.png")),
           pygame.image.load(os.path.join("assets", "frame4_.png"))]

JUMPING = pygame.image.load(os.path.join("assets", "frame3_.png"))

SLIDE = pygame.image.load(os.path.join("assets", "frame5_.png"))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT = pygame.font.SysFont("comicsans", 100)
FONT2 = pygame.font.SysFont("comicsans", 30)

EVENT = pygame.USEREVENT + 1

FPS = 60
pygame.display.set_caption("jumping_game")

class Dino():
    X = WIDTH/2 -200
    Y = HEIGHT / 2

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.vel = 8
        self.rect = pygame.Rect(self.X, self.Y, img.get_width(), img.get_height())
        self.is_run = True
        self.is_jump = False
        self.is_slide = False
        self.no_action = False
        self.score = 0
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.step_index = 0
        self.slide_index = 0
        self.no_action_index = 0

    def update(self):
        if self.is_run:
            self.image = RUNNING[int(self.step_index)]
            self.step_index += 0.2

        if self.is_jump:
            self.no_action = True
            self.no_action_index += 0.2
            self.image = JUMPING
            self.rect.y -= self.vel
            self.vel -= 0.4

        if self.is_slide:
            self.image = SLIDE
            self.rect.y = HEIGHT / 2 + 30
            self.slide_index += 1

            if self.slide_index >= 50:
                self.slide_index = 0
                self.is_slide = False
                self.is_run = True
                self.rect.y = HEIGHT / 2

        if self.vel < -9:
            self.is_jump = False
            self.is_run = True
            self.vel = 8

        if self.step_index >= 3:
            self.step_index = 0

        if self.no_action_index >= 50:
            self.no_action = False
            self.no_action_index = 0

    def collide(self, obstacle, score):
        if self.rect.colliderect(obstacle):
            self.score = int(score)
            return True
        else:
            return False

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

class Obstacle():

    def __init__(self, x, y, obstacle_vel, height):
        self.x = x
        self.y = y
        self.vel = obstacle_vel
        self.rect = pygame.Rect(x, y + 80 - height, 30, height)
        self.passed = False

    def update(self):
        self.rect.x -= self.vel
        if self.rect.x < 0 - self.rect.width:
            self.passed = True

    def draw(self):
        pygame.draw.rect(WIN, BLACK, self.rect)


def draw_window(dinos, obstacles, game_over, score,):
    WIN.fill(WHITE)

    score_text = FONT2.render(str(int(score)), 1, BLACK)
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - 200))

    for dino in dinos:
        dino.draw()
    for obstacle in obstacles:
        obstacle.draw()

    pygame.draw.line(WIN, BLACK, (0, HEIGHT/2 + 80), (WIDTH, HEIGHT/2 + 80))

    if game_over:
        game_over_text = FONT.render("GAME OVER", 1, BLACK)
        start_text = FONT2.render("press enter to start again", 1, BLACK)
        WIN.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - 150))
        WIN.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2 - 80))

    pygame.display.update()

def main():

    score = 0
    obstacle_vel = 4
    dinos = [Dino()]
    obstacles = [Obstacle(WIDTH, HEIGHT/2, obstacle_vel, 50)]

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

        for i,dino in enumerate(dinos):
            if dino.is_slide is False and dino.is_jump is False and keys_pressed[pygame.K_SPACE]:
                dino.is_jump = True
            if dino.is_slide is False and dino.is_jump is False and keys_pressed[pygame.K_x]:
                dino.is_slide = True
            dino.update()

        if game_over and keys_pressed[pygame.K_RETURN]:
            game_over = False
            dinos.append(Dino())
            score = 0
            obstacle_vel = 4
            obstacles = [Obstacle(WIDTH, HEIGHT / 2, obstacle_vel, 50)]

        for obstacle in obstacles:
            if obstacle.passed:
                obstacles.remove(obstacle)
                i = random.randrange(1, 4)
                if i == 1:
                    obstacles.append(Obstacle(WIDTH, HEIGHT / 2 - 60, obstacle_vel, 15))

                else:
                    obstacles.append(Obstacle(WIDTH, HEIGHT / 2, obstacle_vel, 50))

            for i, dino in enumerate(dinos):
                if dino.collide(obstacle, score):
                    dinos.pop()
                    if not dinos:
                        game_over = True
                        break

            obstacle.update()



        if game_over is False:
            score += 1/FPS


        draw_window(dinos, obstacles, game_over, score)




if __name__ == "__main__":
    main()
