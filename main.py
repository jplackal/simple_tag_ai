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
font = pygame.font.SysFont("Arial", 36)

# Neural network settings
inner_layers = 2
inner_nueron_count = 10
ai_count = 25
input_count = 8
output_count = 4

# Agent settings
tagger_speed = 1
runner_speed = 1
friction = 0.85

# Training settings
max_time = 5
fps = 60
max_frames = max_time * fps

mutate_chance = 10
mutate_amount = 0.15

max_hall_of_fame = 5

collision_dist = 30 ** 2

# Maximum possible toroidal distance
max_distance = math.hypot(WIDTH / 2, HEIGHT / 2)

tagger_hall_of_fame = []
runner_hall_of_fame = []

time = 0
gen = 0
progress = 0


def setup():
    global taggers, runners

    taggers = [agent("tagger") for i in range(ai_count)]
    runners = [agent("runner") for i in range(ai_count)]


class nueral_network:

    def __init__(self):
        self.network = []

        layer = []

        for i in range(inner_nueron_count):
            nueron = [[]]
            nueron.append(random.uniform(-1, 0))

            for i2 in range(input_count):
                nueron[0].append(random.uniform(-1, 1))

            layer.append(nueron)

        self.network.append(layer)

        for i in range(inner_layers - 1):
            layer = []

            for i2 in range(inner_nueron_count):
                nueron = [[]]
                nueron.append(random.uniform(-1, 0))

                for i3 in range(inner_nueron_count):
                    nueron[0].append(random.uniform(-1, 1))

                layer.append(nueron)

            self.network.append(layer)

        layer = []

        for i in range(output_count):
            nueron = [[]]
            nueron.append(random.uniform(-1, 0))

            for i2 in range(inner_nueron_count):
                nueron[0].append(random.uniform(-1, 1))

            layer.append(nueron)

        self.network.append(layer)

    def sigmoid(self, x):
        if x >= 0:
            return 1 / (1 + math.exp(-x))

        return math.exp(x) / (1 + math.exp(x))

    def calculate(self, inputs):

        new = []

        for i in range(inner_nueron_count):

            total_w = sum(
                inputs[i2] * self.network[0][i][0][i2]
                for i2 in range(len(inputs))
            )

            total_w += self.network[0][i][1]

            total_w = self.sigmoid(total_w)

            new.append(total_w)

        inputs = new

        for i in range(inner_layers - 1):

            new = []

            for i2 in range(inner_nueron_count):

                total_w = sum(
                    inputs[i3] * self.network[i + 1][i2][0][i3]
                    for i3 in range(len(inputs))
                )

                total_w += self.network[i + 1][i2][1]

                total_w = self.sigmoid(total_w)

                new.append(total_w)

            inputs = new

        new = []

        for i in range(output_count):

            total_w = sum(
                inputs[i2] * self.network[-1][i][0][i2]
                for i2 in range(len(inputs))
            )

            total_w += self.network[-1][i][1]

            total_w = self.sigmoid(total_w)

            new.append(total_w)

        return new

    def mutate_self(self):

        for i in range(len(self.network)):

            for i2 in range(len(self.network[i])):

                for i3 in range(len(self.network[i][i2][0])):

                    if random.random() < mutate_chance / 100:

                        self.network[i][i2][0][i3] += random.uniform(
                            -mutate_amount,
                            mutate_amount
                        )

                if random.random() < mutate_chance / 100:

                    self.network[i][i2][1] += random.uniform(
                        -mutate_amount,
                        mutate_amount
                    )


class agent:

    def __init__(self, role):

        self.y = HEIGHT / 2
        self.vx = 0
        self.vy = 0
        self.type = role

        if self.type == "tagger":
            self.speed = tagger_speed
            self.x = WIDTH / 5
        else:
            self.speed = runner_speed
            self.x = WIDTH / 5 * 4

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

        self.y = HEIGHT / 2
        self.vx = 0
        self.vy = 0

        if self.type == "tagger":
            self.x = WIDTH / 5
        else:
            self.x = WIDTH / 5 * 4

    def draw_self(self):

        color = (255, 0, 0) if self.type == "tagger" else (0, 100, 255)

        pygame.draw.circle(
            screen,
            color,
            (int(self.x), int(self.y)),
            int(collision_dist ** 0.5)
        )


def find_dist(tagger, runner):

    dx = (runner.x - tagger.x + WIDTH / 2) % WIDTH - WIDTH / 2
    dy = (runner.y - tagger.y + HEIGHT / 2) % HEIGHT - HEIGHT / 2

    return math.sqrt(dx ** 2 + dy ** 2)


def check_collision(tagger, runner):

    return find_dist(tagger, runner) ** 2 <= collision_dist


# Both agents receive the same score.
# The tagger wants to MINIMIZE it.
# The runner wants to MAXIMIZE it.
async def run_match(tagger, runner):

    time = 0
    total_dist = 0

    tagger.reset_pos()
    runner.reset_pos()

    tagged = False

    while time < max_frames and not tagged:

        t_direction = tagger.simulate_step(runner)
        r_direction = runner.simulate_step(tagger)

        tagger.apply_vel(t_direction)
        runner.apply_vel(r_direction)

        current_dist = find_dist(tagger, runner)
        total_dist += current_dist

        time += 1

        if check_collision(tagger, runner):
            tagged = True

        # Give the browser time to process events
        if time % 30 == 0:
            await asyncio.sleep(0)

    average_dist = total_dist / time
    final_dist = find_dist(tagger, runner)

    average_dist_score = average_dist / max_distance
    final_dist_score = final_dist / max_distance

    score = (
        time * 50
        + average_dist_score * 25
        + final_dist_score * 25
    )

    return score


def add_to_hall_of_fame(tagger, runner):

    tagger_hall_of_fame.append(copy.deepcopy(tagger))
    runner_hall_of_fame.append(copy.deepcopy(runner))

    if len(tagger_hall_of_fame) > max_hall_of_fame:

        tagger_hall_of_fame.pop(0)
        runner_hall_of_fame.pop(0)


def mutate_all():

    global taggers, runners

    taggers = [
        copy.deepcopy(tagger_hall_of_fame[-1])
        for i in range(ai_count - 1)
    ]

    runners = [
        copy.deepcopy(runner_hall_of_fame[-1])
        for i in range(ai_count - 1)
    ]

    for tagger in taggers:
        tagger.brain.mutate_self()

    for runner in runners:
        runner.brain.mutate_self()

    # Preserve one unchanged champion
    taggers.append(copy.deepcopy(tagger_hall_of_fame[-1]))
    runners.append(copy.deepcopy(runner_hall_of_fame[-1]))


async def simulate():

    global progress

    progress = 0

    total_evaluations = ai_count * 2

    times_t = []

    # Evaluate taggers
    for i in range(ai_count):

        total_time = 0

        for i2 in range(len(runner_hall_of_fame)):

            score = await run_match(
                taggers[i],
                runner_hall_of_fame[i2]
            )

            total_time += score

        times_t.append(total_time)

        progress = (i + 1) / total_evaluations * 100

    times_r = []

    # Evaluate runners
    for i in range(ai_count):

        total_time = 0

        for i2 in range(len(tagger_hall_of_fame)):

            score = await run_match(
                tagger_hall_of_fame[i2],
                runners[i]
            )

            total_time += score

        times_r.append(total_time)

        progress = (ai_count + i + 1) / total_evaluations * 100

    best_t = times_t.index(min(times_t))
    best_r = times_r.index(max(times_r))

    add_to_hall_of_fame(
        taggers[best_t],
        runners[best_r]
    )

    mutate_all()

    return min(times_t), max(times_r)
def showcase_setup():

    global tagger, runner

    tagger = copy.deepcopy(tagger_hall_of_fame[-1])
    runner = copy.deepcopy(runner_hall_of_fame[-1])

    tagger.reset_pos()
    runner.reset_pos()


def showcase_step():

    t_direction = tagger.simulate_step(runner)
    r_direction = runner.simulate_step(tagger)

    tagger.apply_vel(t_direction)
    runner.apply_vel(r_direction)

    if check_collision(tagger, runner):

        tagger.reset_pos()
        runner.reset_pos()

    tagger.draw_self()
    runner.draw_self()

def start_training():
    return asyncio.create_task(simulate())


def draw_loading_bar(progress):

    bar_width = 300
    bar_height = 20

    bar_x = WIDTH // 2 - bar_width // 2
    bar_y = HEIGHT - 60

    pygame.draw.rect(
        screen,
        (70, 70, 70),
        (bar_x, bar_y, bar_width, bar_height)
    )

    filled_width = int(bar_width * progress / 100)

    pygame.draw.rect(
        screen,
        (0, 220, 100),
        (bar_x, bar_y, filled_width, bar_height)
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (bar_x, bar_y, bar_width, bar_height),
        2
    )

    text = font.render(
        f"Training: {progress:.1f}%",
        True,
        (255, 255, 255)
    )

    screen.blit(text, (bar_x, bar_y - 40))


async def main():

    global time, gen, progress

    running = True

    showcase_setup()

    training_task = None

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Check if background training finished
        if training_task is not None and training_task.done():

            try:
                tagger_score, runner_score = training_task.result()

            except Exception:
                import traceback
                traceback.print_exc()
                raise

            gen += 1

            print("Generation:", gen)
            print("Best tagger score:", tagger_score)
            print("Best runner score:", runner_score)

            showcase_setup()

            time = 0

            training_task = None

        # Showcase or start another generation
        if training_task is None:

            if time >= max_frames:

                training_task = start_training()

            else:

                time += 1
                showcase_step()

        else:

            if time < max_frames:

                time += 1
                showcase_step()

            else:

                tagger.draw_self()
                runner.draw_self()

        text = font.render(
            f"Generation: {gen}",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (20, 20))

        if time >= max_frames and training_task is not None:
            draw_loading_bar(progress)

        pygame.display.flip()

        clock.tick(fps)

        await asyncio.sleep(0)

    pygame.quit()


# Initialize
setup()

add_to_hall_of_fame(taggers[0], runners[0])

asyncio.run(main())