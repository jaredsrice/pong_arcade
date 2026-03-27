# Overview

I developed a Pong-style game using Python and the Arcade library. The game includes two-player paddle controls, ball physics with collision detection, a scoring system, and multiple game states including a menu, serve phase, active gameplay, and game over. The ball speed increases during rallies, and the game uses delta time to ensure consistent movement regardless of frame rate.

I wrote this software with the goal of becoming more familiar with Python and game development fundamentals. Through this project I gained experience working with real-time game loops, handling user input, managing game state, and implementing collision detection. The project also helped reinforce design practices such as organizing code into smaller helper methods, separating responsibilities like drawing and updating, and using scaling to maintain consistent gameplay across different window sizes.

[Software Demo Video](https://youtu.be/2obw77GluSA)

## How to Run

1. Open a terminal and navigate to the project folder

2. Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py 
```

Note: Keep the Fonts folder in the same directory as main.py or the game will not load the custom fonts.

## How to Play

- Player 1: W / S  
- Player 2: ↑ / ↓  
- SPACE: start, serve, and continue  

- First player to 5 points wins! 

## Development Environment

- Visual Studio Code
- Python 3
- Arcade Library
- Git / GitHub

## Useful Websites

- [Python Arcade Library](https://api.arcade.academy/en/stable/example_code/index.html)
- [How to add fonts to Python Arcade](https://www.makeuseof.com/python-arcade-custom-fonts-text-effects/)
- [Second Source for Python Arcade Library](https://arcade-pk.readthedocs.io/en/latest/)
- [Python Math Library](https://docs.python.org/3/library/math.html)

## Future Work

- Fully refactor to object-oriented design.
- Add sound effects for paddles, scoring, and game start. 
- Add a single player mode with levels and a basic AI for the second paddle.  

## AI disclosure

I used ChatGPT as a learning and reference tool throughout this project to help think through design decisions, debug issues, and clarify Python and Arcade library usage. I also used it to better understand concepts such as delta time, collision handling, and structuring a game loop. All final code reflects my own understanding, with AI being primarily used to support learning and problem solving rather than generate complete solutions.