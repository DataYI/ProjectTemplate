import sys
import pygame
from pygame.locals import (
    QUIT
)

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('测试')


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))
    pygame.display.update()