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
        var = self.food == Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        self.move(self.direction)
        self.snake.insert(0, self.head)

        gameover = False
        if self.is_collision():
            gameover = True
            return gameover, self.score

        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

        self.update_ui()
        self.clock.tick(SPEED)

        return gameover, self.score

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        self.head = Point(x, y)

    def update_ui(self):
        self.display.fill((255, 255, 255))
        for point in self.snake:
            pygame.draw.rect(self.display, (0, 0, 255), pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, (0, 0, 255),
                             pygame.Rect(point.x + 4, point.y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8))

        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, (0, 0, 0))
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False


if __name__ == '__main__':
    game = SnakeGame()
    while True:
        isgameover, score = game.play_step()
        if isgameover == True:
            break
        print('final score is : ', score)
