<h1 align="center">Classic Game Suite 🎮</h1>

A collection of classic games built with Python and Pygame, featuring a unified interface with a main menu, theme switching, and a leaderboard system. Games include Snake, Tic-Tac-Toe, Hangman, Minesweeper, and Number Guessing. 🕹️

# Screenshots 📸

![1](https://github.com/user-attachments/assets/9cd05d66-c679-4390-8bc9-66092251d644)
![2](https://github.com/user-attachments/assets/3114af88-31c7-4bd7-bb18-9623cd7d679f)
![3](https://github.com/user-attachments/assets/02c67d96-af1a-4a31-990a-d1e6968e9567)
![4](https://github.com/user-attachments/assets/eaa96492-3223-4b91-a348-62350a3a6f43)
![5](https://github.com/user-attachments/assets/d634ee9a-18c7-473d-8236-e250735648d3)
![6](https://github.com/user-attachments/assets/b7905260-6a20-4581-967d-acdee401954c)
![7](https://github.com/user-attachments/assets/05eedf71-9b52-43f0-b29d-710a25129cdf)

# Requirements 🛠️

1. Programming Language: Python 3.x 🐍

2. Libraries Used:
i. Pygame (pip install pygame) for rendering graphics and handling input. 🎨
ii. Standard Python libraries: asyncio, random, math, collections.defaultdict.

# Features ✨

1. Games Included:

i.Snake 🐍: Navigate a snake to eat food and grow without hitting walls or yourself.

ii. Tic-Tac-Toe ❌⭕: Play against an AI opponent to align three symbols (X or O).

iii. Hangman 🧍: Guess letters to complete a hidden word within a limited number of lives.

iv. Minesweeper 💣: Reveal cells to avoid hidden mines and clear the board.

v. Number Guessing 🔢: Guess a number between 1 and 100 within 10 attempts.

2. Theme Toggle 🌗: Switch between dark and light themes using the 'T' key.

3. Player Name Input ✍️: Enter a name before starting a game for leaderboard tracking.

4. Responsive Controls 🎲: Keyboard and mouse inputs tailored for each game.

# Installation 🚀

Clone the repository:git clone https://github.com/ArshiBansal/classic-game-suite.git

Navigate to the project directory:cd classic-game-suite

Install dependencies:pip install pygame

Run the game:python main.py

# How to Play 🎯

i. Launch the Game: Run the script to start the main menu. 🚪

ii. Main Menu:

Use UP/DOWN arrows to navigate game options. ⬆️⬇️

Press ENTER to select a game and enter your name. ✅

Press T to toggle between dark and light themes. 🌑🌕

Select "Quit" to exit. 🚪

iii. Game Controls:

Snake: Arrow keys to move, ESC to return to menu, R to restart after game over. 🐍

Tic-Tac-Toe: Click to place X, AI places O, ESC to menu, R to restart. ❌⭕

Hangman: Type letters to guess, ESC to menu, R to restart. 🧍

Minesweeper: Left-click to reveal, right-click to flag, ESC to menu, R to restart. 💣

Number Guessing: Type numbers, ENTER to submit, ESC to menu, R to restart. 🔢

iv. Scoring:

Snake: +10 per food. 🍎

Tic-Tac-Toe: +50 for win, +10 for draw. 🏅

Hangman: +5 per guess, +10 per remaining life on win. 📝

Minesweeper: +10 per revealed cell, +5 per flag, +100 for win. 💥

Number Guessing: +5 per guess, +(10 - attempts + 1) * 10 for win. 🔍

# Compatibility 🌐

The game is compatible with Pyodide for browser execution, with no local file I/O or network calls. 🌍

Tested on Python 3.8+ and Pygame 2.x. ✅

# Acknowledgments 🙌

Built with Pygame. 🎮

Inspired by classic arcade and puzzle games. 🕹️

