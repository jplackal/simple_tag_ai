import asyncio
import pygame
import random
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
tagger_vel = (0,0)
runner_vel = (0,0)
tagger_speed = 5
runner_speed = 5
output_count = 4
def create_ai():
    for i in range(0, ai_count):
        networks_tagger.append([])
        networks_tagger[i].append([])
        for i2 in range(0, inner_nueron_count):
            networks_tagger[i][0].append([])
            networks_tagger[i][0][i2].append([])
            for i3 in range(0, input_count):
                networks_tagger[i][0][i2][0].append(random.uniform(-1,1))
            networks_tagger[i][0][i2].append(random.uniform(-1,1))
        for i2 in range(0, inner_layers-1):
            networks_tagger[i].append([])
            for i3 in range(0, inner_nueron_count):
                networks_tagger[i][i2+1].append([])
                networks_tagger[i][i2+1][i3].append([])
                for i4 in range(0,inner_nueron_count):
                    networks_tagger[i][i2+1][i3][0].append(random.uniform(-1,1))
                networks_tagger[i][i2+1][i3].append(random.uniform(-1,1))
        networks_tagger[i].append([])
        for i2 in range(0, output_count):
            networks_tagger[i][inner_layers].append([])
            networks_tagger[i][inner_layers][i2].append([])
            for i3 in range(0, inner_nueron_count):
                networks_tagger[i][inner_layers][i2][0].append(random.uniform(-1,1))              

            networks_tagger[i][inner_layers][i2].append(-1)
    for i in range(0, ai_count):
        networks_runner.append([])
        networks_runner[i].append([])
        for i2 in range(0, inner_nueron_count):
            networks_runner[i][0].append([])
            networks_runner[i][0][i2].append([])
            for i3 in range(0, input_count):
                networks_runner[i][0][i2][0].append(random.uniform(-1,1))
            networks_runner[i][0][i2].append(random.uniform(-1,1))
        for i2 in range(0, inner_layers-1):
            networks_runner[i].append([])
            for i3 in range(0, inner_nueron_count):
                networks_runner[i][i2+1].append([])
                networks_runner[i][i2+1][i3].append([])
                for i4 in range(0,inner_nueron_count):
                    networks_runner[i][i2+1][i3][0].append(random.uniform(-1,1))
                networks_runner[i][i2+1][i3].append(random.uniform(-1,1))
        networks_runner[i].append([])
        for i2 in range(0, output_count):
            networks_runner[i][inner_layers].append([])
            networks_runner[i][inner_layers][i2].append([])
            for i3 in range(0, inner_nueron_count):
                networks_runner[i][inner_layers][i2][0].append(random.uniform(-1,1))              

            networks_runner[i][inner_layers][i2].append(-1)

    print(networks_tagger)
    print(networks_runner)
create_ai()
async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())