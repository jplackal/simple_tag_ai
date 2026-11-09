# simple_tag_ai
# AI Tag

An artificial intelligence simulation built with Python and Pygame. Two populations of AI agents compete in a game of tag: taggers try to catch runners, while runners try to avoid being caught.

The agents use neural networks to make decisions. Over generations, their networks mutate and the best-performing agents are preserved in a Hall of Fame.

## 🎮 Play the Game

- **Play in your browser:** [PLAY AI TAG ON ITCH.IO](https://jplackal.itch.io/a-simple-ai)
- **Source code:** [VIEW THE SOURCE CODE](https://github.com/jplackal/simple_tag_ai/blob/main/main.py)

## How to Run

### Requirements

- Python 3
- Pygame

### Installation

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Install Pygame:

   ```bash
   pip install pygame
   ```

4. Run the main Python file:

   ```bash
   python3 main.py
   ```

If you are using Windows, you may need to use `python main.py` instead.

## How to Play

The simulation has two types of AI:

- **Taggers:** Try to catch the runners.
- **Runners:** Try to stay away from the taggers for as long as possible.

The simulation trains the AI populations over multiple generations. You can watch the best agents compete in the showcase.

## How It Works

### 1. Neural Networks

Every AI agent has its own neural network.

The network receives information about the agent and its opponent, including:

- Its own position.
- Its own velocity.
- The relative position of its opponent.
- The opponent's velocity.

These values are passed through hidden layers of neurons. Each neuron uses weights and a bias to calculate its output.

The network produces four outputs, representing four possible movement directions:

1. Down
2. Right
3. Up
4. Left

The direction with the highest output is selected.

### 2. Training and Evaluation

Each generation contains a population of taggers and runners.

Each candidate is tested against agents from the opposing population's Hall of Fame.

The simulation records a fitness score based on:

- How long the match lasts.
- The average distance between the agents.
- The final distance between the agents.

The tagger with the lowest total score is selected because taggers want to catch runners quickly.

The runner with the highest total score is selected because runners want to survive and maintain distance.

### 3. Evolution and Mutation

After evaluating a generation:

1. The best tagger and runner are selected.
2. Copies of these agents are saved in the Hall of Fame.
3. Most of