import pygame
import random
from enum import Enum
from collections import namedtuple


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('point', 'x , y')
pygame.init()
font = pygame.font.SysFont('arial', 25)

BLOCK_SIZE = 20
SPEED = 40


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('snake')
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None

    def place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food == Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def play_step(self):
        self.update_ui()
        self.clock.tick(SPEED)
        gameover = False
        return gameover, self.score

    def update_ui(self):
        self.display.fill((255, 255, 255))
        for point in self.snake:
            pygame.draw.rect(self.display, (0, 0, 255), pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, (0, 0, 255), pygame.Rect(point.x + 4, point.y + 4, BLOCK_SIZE - 8,BLOCK_SIZE - 8))

        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, (0, 0, 0))
        self.display.blit(text, [0, 0])
        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGame()
    while True:
        gameover, score = game.play_step()
        if gameover == True:
            break
        print('final score is : ', score)
