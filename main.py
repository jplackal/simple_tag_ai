import asyncio
import pygame
import random
import math
import copy
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
friction = 0.9
tagger_hall_of_fame = []
runner_hall_of_fame = []
max_time = 15
fps = 60
max_frames = max_time * fps
def setup():
    global taggers, runners
    taggers = [agent("tagger") for i in range(ai_count)]
    runners = [agent("runner") for i in range(ai_count)]
class nueral_network:
    def __init__(self):
        self.network = []
        layer = []
        for i in range(0, inner_nueron_count):
            nueron = [[]]
            nueron.append(random.uniform(-1, 0))
            for i in range(0, input_count):
                nueron[0].append(random.uniform(-1, 1))
            layer.append(nueron)
        self.network.append(layer)
        for i in range(0, inner_layers-1):
            layer = []
            for i in range(0, inner_nueron_count):
                nueron = [[]]
                nueron.append(random.uniform(-1, 0))
                for i in range(0, inner_nueron_count):
                    nueron[0].append(random.uniform(-1, 1))
                layer.append(nueron)
            self.network.append(layer)
        layer = []
        for i in range(0, output_count):
            nueron = [[]]
            nueron.append(random.uniform(-1, 0))
            for i in range(0, inner_nueron_count):
                nueron[0].append(random.uniform(-1, 1))
            layer.append(nueron)
        self.network.append(layer)

    def sigmoid(self, x):
        if x >= 0: return 1 / (1 + math.exp(-x))
        return math.exp(x) / (1 + math.exp(x))
    def calculate(self, inputs):
        new = []
        for i in range(0, inner_nueron_count):
            total_w = sum(inputs[i2] * self.network[0][i][0][i2] for i2 in range(len(inputs)))
            total_w += self.network[0][i][1]
            total_w = self.sigmoid(total_w)
            new.append(total_w)
        inputs = new
        for i in range(0, inner_layers-1):
            new = []
            for i3 in range(0, inner_nueron_count):
                total_w = sum(inputs[i2] * self.network[i+1][i3][0][i2] for i2 in range(len(inputs)))
                total_w += self.network[i+1][i3][1]
                total_w = self.sigmoid(total_w)
                new.append(total_w)
            inputs = new
        new = []
        for i in range(0, output_count):
            total_w = sum(inputs[i2] * self.network[-1][i][0][i2] for i2 in range(len(inputs)))
            total_w += self.network[-1][i][1]
            total_w = self.sigmoid(total_w)
            new.append(total_w)
        return new
    
class agent:
    def __init__(self, role):
        self.y = HEIGHT/2
        self.vx = 0
        self.vy = 0
        self.type = role
        if self.type == "tagger":
            self.speed = tagger_speed
            self.x = WIDTH/5
        else:
            self.speed = runner_speed
            self.x = WIDTH/5*4
        self.brain = nueral_network()
    def input_data(self, other):
        return [
            self.x / WIDTH,
            self.y / HEIGHT,
            self.vx / self.speed,
            self.vy / self.speed,
            ((other.x - self.x + WIDTH / 2) % WIDTH - WIDTH / 2) / WIDTH,
            ((other.y - self.y + HEIGHT / 2) % HEIGHT - HEIGHT / 2) / HEIGHT,
            other.vx / other.speed,
            other.vy / other.speed
        ]
    def apply_vel(self, direction):
        if direction == 0:
            self.vy += self.speed
        elif direction == 1:
            self.vx += self.speed
        elif direction == 2:
            self.vy -= self.speed
        elif direction == 3:
            self.vx-= self.speed
        self.vx *= friction
        self.vy *= friction
        self.x += self.vx
        self.y += self.vy
        self.x %= WIDTH+1
        self.y %= HEIGHT+1

    def simulate_step(self, other):
        inputs = self.input_data(other)
        outputs = self.brain.calculate(inputs)
        direction = outputs.index(max(outputs))
        self.apply_vel(direction)
setup()
time = 0
def reset():
    global time
    print("reset")
    time = 0
    simulate()
def simulate():
    for i in range(0, max_frames):
        print("frame")
def showcase_step():
    print("does one step of showcase")
def check_reset():
    if time >= max_frames:
        reset()
    else:
        time += 1
        showcase_step(
        )
gen = 0
reset()
async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(fps)
        await asyncio.sleep(0)
asyncio.run(main())