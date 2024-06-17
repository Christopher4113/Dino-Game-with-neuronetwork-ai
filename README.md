Dino Game AI
This project uses NEAT (NeuroEvolution of Augmenting Topologies) to train an AI to play a Dino game.

Setup
Create a Virtual Environment
Create a virtual environment to manage project dependencies.

bash
Copy code
python -m venv venv
Activate the Virtual Environment
On Windows:

bash
Copy code
venv\Scripts\activate
On macOS and Linux:

bash
Copy code
source venv/bin/activate
Install Dependencies
Install the required dependencies using pip.

bash
Copy code
pip install -r requirements.txt
Running the Project
To run the project, execute the following command:

bash
Copy code
python main.py
File Structure
css
Copy code
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
Configuration
The NEAT configuration is specified in the config_feedforward.txt file. You can adjust the parameters as needed to fine-tune the performance of the neural networks.

Controls
The game is controlled by the AI. You can close the game window to stop the execution.
