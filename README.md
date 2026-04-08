# Maple's Adventure

A fun, endless runner game built with Pygame where you control Maple, a pug on an exciting adventure! Jump over obstacles, avoid trees, and try to achieve the highest score possible.

## Features

- **Endless Gameplay**: Keep running and jumping as long as you can!
- **Progressive Difficulty**: Speed increases every 5 points for added challenge
- **High Score Tracking**: Your best score is saved locally
- **Smooth Animations**: Character animations for running and jumping
- **Scrolling Background**: Dynamic background that moves with the action
- **Simple Controls**: Easy to pick up and play

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/PugDash.git
   cd PugDash
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Navigate to the src directory:

   ```bash
   cd src
   ```

2. Run the game:
   ```bash
   python main.py
   ```

The game window will open, and you'll see the main menu with options to Start, access the Store (coming soon), or Quit.

## Controls

- **SPACEBAR**: Jump
- **Mouse Click**: Select menu options

## Gameplay

- Control Maple as she runs automatically through the landscape
- Press SPACE to jump over trees and other obstacles
- Avoid collisions - hitting an obstacle ends the game
- Score points for each obstacle you successfully pass
- Speed increases every 5 points, making it progressively harder
- Try to beat your high score!

## Game Files

- `main.py`: Entry point and main menu
- `game.py`: Core game logic and rendering
- `player.py`: Player character class with animations
- `ground.py`: Ground rendering
- `obstacles.py`: Obstacle generation and collision
- `spriteSheet.py`: Sprite sheet handling
- `gameInfo.json`: Stores high score and unlocked characters

## Requirements

- pygame

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
