import asyncio

import pygame
from pygame import gfxdraw

from src import *

pygame.init()

TRAIN_IMAGE = pygame.transform.scale(pygame.image.load('./assets/train.png'), (64, 64))
TRAIN_IMAGE_REVERSED = pygame.transform.flip(TRAIN_IMAGE, True, False)

FONT = pygame.font.Font('./assets/Montserrat-Regular.ttf', 14)

COLOR_LINE = tuple(int('6ee7b7'[i:i+2], 16) for i in (0, 2, 4))
COLOR_CIRCLE = tuple(int('818cf8'[i:i+2], 16) for i in (0, 2, 4))


async def visualize(simulation: Simulation):
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('Omsk Subway Simulation | by AlexeyZavar')
    exit_requested = False

    while not exit_requested:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_requested = True

        screen.fill('#f0fdfa')

        # draw line
        pygame.draw.line(screen, COLOR_LINE, (60, 100), (1000 - 60, 100), 3)

        # draw stations
        gfxdraw.filled_circle(screen, 60, 100, 20, COLOR_CIRCLE)
        gfxdraw.filled_circle(screen, 60 + 6 * 50, 100, 20, COLOR_CIRCLE)
        gfxdraw.filled_circle(screen, 60 + 9 * 50, 100, 20, COLOR_CIRCLE)
        gfxdraw.filled_circle(screen, 60 + 11 * 50, 100, 20, COLOR_CIRCLE)
        gfxdraw.filled_circle(screen, 60 + 18 * 50, 100, 20, COLOR_CIRCLE)

        # draw trains
        for train in simulation.trains:
            c = train.path_total

            if train.direction == 1:
                screen.blit(TRAIN_IMAGE, (c, 100))
            else:
                screen.blit(TRAIN_IMAGE_REVERSED, (c, 40))

        # 74 fps
        await asyncio.sleep(1 / 74)

        pygame.display.flip()
