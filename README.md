# simple_tag_ai
temp : ai code
import asyncio
import pygame
import random
import math
import copy

pygame.init()
random.seed()

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1300, 750
INNER_LAYERS = 3
INNER_NEURON_COUNT = 20
AI_COUNT = 25
INPUT_COUNT = 8
OUTPUT_COUNT = 4
TAGGER_SPEED = 5
RUNNER_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Tag Evolution")
clock = pygame.time.Clock()

# --- AI CLASS ---
class NeuralNetwork:
    def __init__(self):
        # Initialize weights randomly
        self.weights = []
        # Input Layer
        layer = []
        for i in range(INNER_NEURON_COUNT):
            layer.append([ [random.uniform(-1, 1) for _ in range(INPUT_COUNT)], random.uniform(-1, 1) ])
        self.weights.append(layer)
        # Hidden Layers
        for _ in range(INNER_LAYERS - 1):
            layer = []
            for i in range(INNER_NEURON_COUNT):
                layer.append([ [random.uniform(-1, 1) for _ in range(INNER_NEURON_COUNT)], random.uniform(-1, 1) ])
            self.weights.append(layer)
        # Output Layer
        layer = []
        for i in range(OUTPUT_COUNT):
            layer.append([ [random.uniform(-1, 1) for _ in range(INNER_NEURON_COUNT)], -1 ])
        self.weights.append(layer)

    def sigmoid(self, x):
        if x >= 0: return 1 / (1 + math.exp(-x))
        return math.exp(x) / (1 + math.exp(x))

    def predict(self, inputs):
        current_inputs = inputs
        for layer_idx, layer in enumerate(self.weights):
            new_outputs = []
            for neuron in layer:
                weights, bias = neuron
                total = sum(i * w for i, w in zip(current_inputs, weights)) + bias
                new_outputs.append(self.sigmoid(total))
            current_inputs = new_outputs
        return current_inputs

    def mutate(self, rate=0.1):
        # Create a copy and slightly tweak weights
        mutated = copy.deepcopy(self)
        for layer in mutated.weights:
            for neuron in layer:
                # Mutate weights
                neuron[0] = [w + random.uniform(-rate, rate) for w in neuron[0]]
                # Mutate bias
                neuron[1] += random.uniform(-rate, rate)
        return mutated

# --- GAME LOGIC ---
def check_collision(pos1, pos2):
    dist = math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
    return dist < 50 # Combined radii

def run_match(tagger_net, runner_net, visual=False):
    # Positions: [x, y, vx, vy]
    t_pos = [WIDTH // 5, HEIGHT // 2, 0, 0]
    r_pos = [(WIDTH // 5) * 4, HEIGHT // 2, 0, 0]
    
    frames = 0
    max_frames = 1000 # Prevent infinite loops
    
    while frames < max_frames:
        # Tagger AI
        t_in = [t_pos[0]/WIDTH, t_pos[1]/HEIGHT, t_pos[2]/TAGGER_SPEED, t_pos[3]/TAGGER_SPEED, 0,0,0,0]
        t_out = tagger_net.predict(t_in)
        action = max(range(4), key=lambda i: t_out[i])
        if action == 0: t_pos[3] -= TAGGER_SPEED
        elif action == 1: t_pos[3] += TAGGER_SPEED
        elif action == 2: t_pos[2] -= TAGGER_SPEED
        else: t_pos[2] += TAGGER_SPEED
        
        # Runner AI
        r_in = [r_pos[0]/WIDTH, r_pos[1]/HEIGHT, r_pos[2]/RUNNER_SPEED, r_pos[3]/RUNNER_SPEED, 0,0,0,0]
        r_out = runner_net.predict(r_in)
        action = max(range(4), key=lambda i: r_out[i])
        if action == 0: r_pos[3] -= RUNNER_SPEED
        elif action == 1: r_pos[3] += RUNNER_SPEED
        elif action == 2: r_pos[2] -= RUNNER_SPEED
        else: r_pos[2] += RUNNER_SPEED

        # Physics
        for p in [t_pos, r_pos]:
            p[2] *= 0.7; p[3] *= 0.7
            p[0] = (p[0] + p[2]) % WIDTH
            p[1] = (p[1] + p[3]) % HEIGHT

        if check_collision(t_pos, r_pos):
            return frames # Return time taken to tag

        if visual:
            pygame.draw.circle(screen, (255,0,0), (int(t_pos[0]), int(t_pos[1])), 25)
            pygame.draw.circle(screen, (0,0,255), (int(r_pos[0]), int(r_pos[1])), 25)
            pygame.display.flip()
            clock.tick(60)

        frames += 1
    return max_frames

# --- EVOLUTION SYSTEM ---
async def main():
    # Initial Population
    taggers = [NeuralNetwork() for _ in range(AI_COUNT)]
    runners = [NeuralNetwork() for _ in range(AI_COUNT)]
    
    hall_of_fame_taggers = []
    hall_of_fame_runners = []

    generation = 1
    while True:
        print(f"--- Generation {generation} ---")
        
        # Tournament: Every tagger vs every runner
        t_scores = [0] * AI_COUNT
        r_scores = [0] * AI_COUNT
        
        for t_idx in range(AI_COUNT):
            for r_idx in range(AI_COUNT):
                time = run_match(taggers[t_idx], runners[r_idx])
                t_scores[t_idx] += time
                r_scores[r_idx] += time

        # Best Tagger = lowest total time
        best_t_idx = t_scores.index(min(t_scores))
        # Best Runner = highest total time
        best_r_idx = r_scores.index(max(r_scores))
        
        champ_t = taggers[best_t_idx]
        champ_r = runners[best_r_idx]
        
        hall_of_fame_taggers.append(champ_t)
        hall_of_fame_runners.append(champ_r)
        
        print(f"Best Tagger Score: {t_scores[best_t_idx]} | Best Runner Score: {r_scores[best_r_idx]}")

        # EVOLVE: Create next generation from champions
        taggers = [champ_t.mutate() for _ in range(AI_COUNT)]
        runners = [champ_r.mutate() for _ in range(AI_COUNT)]
        
        generation += 1
        await asyncio.sleep(0)

asyncio.run(main())
