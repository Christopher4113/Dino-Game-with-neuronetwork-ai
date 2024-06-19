# Dino Game AI

This project uses NEAT (NeuroEvolution of Augmenting Topologies) to train an AI to play a Dino game.

## Features

- Train an AI to play the Dino game.
- Use NEAT for neural network evolution.
- Visualize the AI's learning process.

## Prerequisites

- Python installed on your system.
- Required Python packages listed in `requirements.txt`.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/YourUsername/Dino-Game-with-neuronetwork-ai.git
    cd Dino-Game-with-neuronetwork-ai
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    On Windows:
    ```bash
    venv\Scripts\activate
    ```

    On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Start the application:**

    ```bash
    python main.py
    ```

2. **Observe the AI playing the Dino game and learning over time.**

3. **Close the game window to stop the execution.**

## Configuration

The NEAT configuration is specified in the `config_feedforward.txt` file. You can adjust the parameters as needed to fine-tune the performance of the neural networks.

## Code Explanation

### Project Setup

The project uses Pygame for the game environment and NEAT for evolving the neural networks. The main script initializes the game, sets up the NEAT algorithm, and runs the training loop.

### Dependencies

- **pygame**: For creating the Dino game environment.
- **neat-python**: For implementing the NEAT algorithm.

### File Structure

```plaintext
project_directory/
│
├── Assets/
│   ├── Dino/
│   │   ├── DinoRun1.png
│   │   ├── DinoRun2.png
│   │   ├── DinoJump.png
│   │   ├── DinoDuck1.png
│   │   ├── DinoDuck2.png
│   ├── Cactus/
│   │   ├── SmallCactus1.png
│   │   ├── SmallCactus2.png
│   │   ├── SmallCactus3.png
│   │   ├── LargeCactus1.png
│   │   ├── LargeCactus2.png
│   │   ├── LargeCactus3.png
│   ├── Bird/
│   │   ├── Bird1.png
│   │   ├── Bird2.png
│   ├── Other/
│       ├── Cloud.png
│       ├── Track.png
│
├── main.py
├── config_feedforward.txt
├── requirements.txt
└── README.md
