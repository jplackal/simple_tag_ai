
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
pygame.display.set_caption("AI Tag")
clock = pygame.time.Clock()

inner_layers = 3
inner_nueron_count = 20
ai_count = 25
input_count = 8
tagger_speed = 5
runner_speed = 5
output_count = 4
friction = 0.9

tagger_hall_of_fame = []
runner_hall_of_fame = []

max_time = 15
fps = 60

# In percentage
mutate_chance = 10
mutate_amount = 0.1

collision_dist = 30
collision_dist **= 2

best_r = 0
best_t = 0
max_frames = max_time * fps

time = 0
gen = 0


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
        if x >= 0:
            return 1 / (1 + math.exp(-x))
        return math.exp(x) / (1 + math.exp(x))

    def calculate(self, inputs):
        new = []

        for i in range(0, inner_nueron_count):
            total_w = sum(
                inputs[i2] * self.network[0][i][0][i2]
                for i2 in range(len(inputs))
            )

            total_w += self.network[0][i][1]
            total_w = self.sigmoid(total_w)
            new.append(total_w)

        inputs = new

        for i in range(0, inner_layers-1):
            new = []

            for i3 in range(0, inner_nueron_count):
                total_w = sum(
                    inputs[i2] * self.network[i+1][i3][0][i2]
                    for i2 in range(len(inputs))
                )

                total_w += self.network[i+1][i3][1]
                total_w = self.sigmoid(total_w)
                new.append(total_w)

            inputs = new

        new = []

        for i in range(0, output_count):
            total_w = sum(
                inputs[i2] * self.network[-1][i][0][i2]
                for i2 in range(len(inputs))
            )

            total_w += self.network[-1][i][1]
            total_w = self.sigmoid(total_w)
            new.append(total_w)

        return new

    def mutate_self(self):
        for i in range(0, len(self.network)):
            for i2 in range(0, len(self.network[i])):
                for i3 in range(0, len(self.network[i][i2][0])):
                    if random.randint(0, 100) <= mutate_chance:
                        self.network[i][i2][0][i3] += random.uniform(
                            -mutate_amount, mutate_amount
                        )

                if random.randint(0, 100) <= mutate_chance:
                    self.network[i][i2][1] += random.uniform(
                        -mutate_amount, mutate_amount
                    )


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
            self.vx -= self.speed

        self.vx *= friction
        self.vy *= friction

        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT

    def simulate_step(self, other):
        inputs = self.input_data(other)
        outputs = self.brain.calculate(inputs)
        direction = outputs.index(max(outputs))
        return direction

    def reset_pos(self):
        self.y = HEIGHT/2
        self.vx = 0
        self.vy = 0

        if self.type == "tagger":
            self.x = WIDTH/5
        else:
            self.x = WIDTH/5*4

    def draw_self(self):
        color = (255, 0, 0) if self.type == "tagger" else (0, 100, 255)
        pygame.draw.circle(
            screen,
            color,
            (int(self.x), int(self.y)),
            int(collision_dist**0.5)
        )


def add_to_hall_of_fame(tagger, runner):
    tagger_hall_of_fame.append(copy.deepcopy(tagger))
    runner_hall_of_fame.append(copy.deepcopy(runner))


def mutate_all():
    global taggers, runners

    taggers = [
        copy.deepcopy(tagger_hall_of_fame[-1])
        for i in range(0, ai_count-1)
    ]

    runners = [
        copy.deepcopy(runner_hall_of_fame[-1])
        for i in range(0, ai_count-1)
    ]

    for tagger in taggers:
        tagger.brain.mutate_self()

    for runner in runners:
        runner.brain.mutate_self()

    taggers.append(copy.deepcopy(tagger_hall_of_fame[-1]))
    runners.append(copy.deepcopy(runner_hall_of_fame[-1]))


def check_collision(tagger, runner):
    dist = (
        ((runner.x - tagger.x + WIDTH / 2) % WIDTH - WIDTH / 2)**2
        + ((runner.y - tagger.y + HEIGHT / 2) % HEIGHT - HEIGHT / 2)**2
    )

    return dist <= collision_dist


def run_match(tagger, runner):
    time = 0
    tagged = "no"

    tagger.reset_pos()
    runner.reset_pos()

    while time < max_frames and tagged == "no":
        t_direction = tagger.simulate_step(runner)
        r_direction = runner.simulate_step(tagger)

        tagger.apply_vel(t_direction)
        runner.apply_vel(r_direction)

        if check_collision(tagger, runner):
            tagged = "yes"

        time += 1

    return time


# This function runs in the background thread.
def simulate():
    times_t = []

    for i in range(0, ai_count):
        total_time = sum(
            run_match(taggers[i], runner_hall_of_fame[i2])
            for i2 in range(0, len(runner_hall_of_fame))
        )

        times_t.append(total_time)

    times_r = []

    for i in range(0, ai_count):
        total_time = sum(
            run_match(tagger_hall_of_fame[i2], runners[i])
            for i2 in range(0, len(tagger_hall_of_fame))
        )

        times_r.append(total_time)

    best_r = times_r.index(max(times_r))
    best_t = times_t.index(min(times_t))

    add_to_hall_of_fame(taggers[best_t], runners[best_r])
    mutate_all()

    return min(times_t), max(times_r)


def showcase_setup():
    global tagger, runner

    tagger = copy.deepcopy(tagger_hall_of_fame[-1])
    runner = copy.deepcopy(runner_hall_of_fame[-1])

    tagger.reset_pos()
    runner.reset_pos()


def showcase_step():
    global time

    t_direction = tagger.simulate_step(runner)
    r_direction = runner.simulate_step(tagger)

    tagger.apply_vel(t_direction)
    runner.apply_vel(r_direction)

    if check_collision(tagger, runner):
        time = max_frames

    tagger.draw_self()
    runner.draw_self()


# BACKGROUND TRAINING:
# This function starts training without blocking Pygame.
def start_training():
    return asyncio.create_task(asyncio.to_thread(simulate))


async def main():
    global time, gen

    running = True

    # Create the first showcase from the initial random agents.
    showcase_setup()

    # Start the first generation in the background.
    training_task = start_training()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # BACKGROUND TRAINING:
        # Check whether the training thread has finished.
        if training_task.done():
            tagger_score, runner_score = training_task.result()

            gen += 1
            print("Generation:", gen)
            print("Best tagger score:", tagger_score)
            print("Best runner score:", runner_score)

            # Load the newly selected champions.
            showcase_setup()
            time = 0

            training_task = None

        # If training is not happening, play the showcase.
        if training_task is None:
            if time >= max_frames:
                # Start training the next generation.
                training_task = start_training()
            else:
                time += 1
                showcase_step()

        else:
            # Keep the showcase moving while training happens.
            if time < max_frames:
                time += 1
                showcase_step()
            else:
                tagger.draw_self()
                runner.draw_self()

        pygame.display.flip()
        clock.tick(fps)
        await asyncio.sleep(0)

    pygame.quit()


# Create the initial population and Hall of Fame entries.
setup()
add_to_hall_of_fame(taggers[0], runners[0])

# Start the program.
asyncio.run(main())
