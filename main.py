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
tagger_vel = (0,0)
runner_vel = (0,0)
tagger_speed = 5
runner_speed = 5
output_count = 4
inputs = [1,1,1,1,1,1,1,1]
new = []
tagger_vals = [[WIDTH // 2, HEIGHT // 2, 0, 0]]
def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    exp_x = math.exp(x)
    return exp_x / (1 + exp_x)


def calculate_tagger(ai):
    global new, inputs, networks_tagger
    new = []
    for i in range(0, inner_nueron_count):
        total_w = 0
        for i2 in range(input_count):
            total_w += inputs[i2]*networks_tagger[ai][0][i][0][i2]
        total_w += networks_tagger[ai][0][i][1]
        total_w = sigmoid(total_w)
        new.append(total_w)
    inputs = new.copy()
    new = []
    for i in range(0, inner_layers-1):
        for i2 in range(0, inner_nueron_count):
            total_w = 0
            for i3 in range(0, inner_nueron_count):
                total_w += inputs[i3]*networks_tagger[ai][i+1][i2][0][i3]
            total_w += networks_tagger[ai][i+1][i2][1]
            total_w = sigmoid(total_w)
            new.append(total_w)    
        inputs = new.copy()
        new = []
    for i in range(0, output_count):
        total_w = 0
        for i2 in range(inner_nueron_count):
            total_w += inputs[i2]*networks_tagger[ai][inner_layers][i][0][i2]
        total_w += networks_tagger[ai][inner_layers][i][1]
        total_w = sigmoid(total_w)
        new.append(total_w)
    inputs = new.copy()
    new = []

def iterate_tagger(ai):
    global inputs
    inputs = [
        tagger_vals[ai][0] / WIDTH,
        tagger_vals[ai][1] / HEIGHT,
        tagger_vals[ai][2] / tagger_speed,
        tagger_vals[ai][3] / tagger_speed,
        0, 0, 0, 0
    ]
    calculate_tagger(ai)
    action = max(range(4), key=lambda i: inputs[i])
    if action == 0:
        tagger_vals[ai][1] -= tagger_speed  # up
    elif action == 1:
        tagger_vals[ai][1] += tagger_speed  # down
    elif action == 2:
        tagger_vals[ai][0] -= tagger_speed  # left
    else:
        tagger_vals[ai][0] += tagger_speed  # right
    tagger_vals[ai][2] *= 0.9
    tagger_vals[ai][3] *= 0.9
    tagger_vals[ai][0] += tagger_vals[ai][2]
    tagger_vals[ai][1] += tagger_vals[ai][3]
    
def draw():
    for i in range(len(tagger_vals)):
        pygame.draw.circle(screen, (255, 255, 255), (int(tagger_vals[i][0]), int(tagger_vals[i][1])), 25)

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
        screen.fill((0, 0, 0))
        iterate_tagger(0)
        draw()
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())