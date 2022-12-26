import pygame
from pygame.locals import *
import sys
import random


class Snake():
    def __init__(self, size=3, color=(0, 255, 0), head_pos=(200, 200), direction="LEFT"):
        # Setup the body
        self.body = []
        self.size=size
        for i in range(size):
            if direction == "LEFT":
                self.body.append((head_pos[0] + 10*i, head_pos[1]))
            if direction == "RIGHT":
                self.body.append((head_pos[0] - 10*i, head_pos[1]))
            if direction == "UP":
                self.body.append((head_pos[0], head_pos[1] - 10*i))
            if direction == "DOWN":
                self.body.append((head_pos[0], head_pos[1] + 10*i))

        # Setup the skin
        self.skin = pygame.Surface((10, 10))
        self.skin.fill(color)
    
    def update(self, direction, apples):
    # Movement
        # Move the body (exlcluding the head)
        for i in range(len(self.body)-1,0,-1):
            self.body[i] = self.body[i-1]

        # Move the head
        if direction == "RIGHT":
            self.body[0] = (self.body[0][0]+10,self.body[0][1])
        elif direction == "LEFT":
            self.body[0] = (self.body[0][0]-10,self.body[0][1])
        elif direction == "UP":
            self.body[0] = (self.body[0][0], self.body[0][1]-10)
        elif direction == "DOWN":
            self.body[0] = (self.body[0][0], self.body[0][1]+10)

    # Collisions
        # Wall Collisions
        if self.body[0][0] >= 600 or self.body [0][1] >= 600 or self.body[0][0] < 0 or self.body[0][1] < 0:
            return "Dead"
        # Self collisions
        if self.body[0] in self.body[1:]:
            return "Dead"

        #Apple collisions
        for apple in apples:
            if self.body[0] == apple.pos:
                apple.move()
                if direction == "RIGHT":
                    self.body.append((self.body[len(self.body)-1][0]-10, self.body[len(self.body)-1][1]))
                elif direction == "LEFT":
                    self.body.append((self.body[len(self.body)-1][0]+10, self.body[len(self.body)-1][1]))
                elif direction == "UP":
                    self.body.append((self.body[len(self.body)-1][0], self.body[len(self.body)-1][1]+10))
                elif direction == "DOWN":
                    self.body.append((self.body[len(self.body)-1][0], self.body[len(self.body)-1][1]-10))
    
    def draw(self, screen):
        for pos in self.body:
            screen.blit(self.skin, pos)


class Apple():
    def __init__(self, pos=None, color=(255, 0, 0)):
        # Set an initial position
        self.pos = pos if pos != None else (random.randint(0, 59)*10, random.randint(0, 59)*10)

        # Setup the skin
        self.skin = pygame.Surface((10,10))
        self.skin.fill(color)
    
    def draw(self, screen):
        screen.blit(self.skin, self.pos)

    def move(self):
        self.pos = (random.randint(0, 59)*10, random.randint(0, 59)*10)


class Runner():
    def __init__(self):
        # Setup the screen
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Make snakes
        self.snakes = []
        self.snakes.append(Snake())
        for i in range(10):
            self.snakes.append(Snake(size=5, 
                                     color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                     head_pos=(200 + 10*i, 200 - 20*i)))

        # Set a default direction
        self.direction = "LEFT"

        # Make apples
        self.apples = []
        for i in range(50):
            self.apples.append(Apple(color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
    
    def update(self):
        self.clock.tick(20)
        # Get input data
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_UP:
                    self.direction = "UP"
                if event.key == K_DOWN:
                    self.direction = "DOWN"
                if event.key == K_LEFT:
                    self.direction = "LEFT"
                if event.key == K_RIGHT:
                    self.direction = "RIGHT"

        # Update the snakes
        for snake in self.snakes:
            if snake.update(self.direction, self.apples) == "Dead":
                text = self.font.render("Game Over", 1, (255, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = (300, 300)
                self.screen.blit(text, text_rect)
                pygame.display.update()
                pygame.time.delay(1000)
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill((0,0,0))
        # Draw snakes
        for snake in self.snakes:
            snake.draw(self.screen)
        # Draw apples
        for apple in self.apples:
            apple.draw(self.screen)

        # Calculate and display the score
        score = 0
        for snake in self.snakes:
            score += (len(snake.body)-snake.size)
        score_text = self.font.render(str(score), 1, (255, 255, 255))
        text_rect = score_text.get_rect()
        text_rect.topleft = (10, 10)
        self.screen.blit(score_text, text_rect)

        pygame.display.update()

pygame.init()
runner = Runner()
while True:
    runner.update()
    runner.draw()
