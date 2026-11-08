import asyncio
import pygame
import random
import math
pygame.init()
random.seed()
WIDTH = 1300
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ai tag")
clock = pygame.time.Clock()
inner_layers = 3
inner_nueron_count = 20
ai_count = 25
input_count = 8
networks_tagger = []
networks_runner = []
tagger_speed = 5
runner_speed = 5
output_count = 4
async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())