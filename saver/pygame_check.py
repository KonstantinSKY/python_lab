import pygame
import random
import math

SCREEN_DIM = (800, 600)


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("NewScreenSaver")
    while True:
        gameDisplay.fill((0, 97, 8))
