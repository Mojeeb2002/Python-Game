# Number Guesser Game

A modern, GUI-based number guessing game built with Python and PyQt5. The game features a sleek dark theme interface and includes score tracking with PostgreSQL database integration.

## Features

- 🎮 Modern GUI interface with dark theme
- 🎯 Multiple difficulty levels:
  - Easy: Unlimited tries
  - Medium: 10 tries
  - Hard: 5 tries
  - Custom: Set your own range and tries
- 💾 Score tracking with PostgreSQL database
- ⌨️ Keyboard support (Enter key for submitting guesses)
- 🏆 High score system

## Prerequisites

- Python 3.6 or higher
- PostgreSQL database
- uv (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Mojeeb2002/Python-Game.git
cd number-guesser
```

2. Install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create a virtual environment and install dependencies using uv:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

4. Set up the database:
   - Create a PostgreSQL database named `number_guesser`
   - Create a `.env` file in the project root with your database credentials:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/number_guesser
   ```

## How to Play

1. Run the game:

```bash
python gui.py
```

2. Select a difficulty level from the dropdown menu
3. Click "Start Game" to begin
4. Enter your guess in the input field
   - Press Enter or click "Submit Guess" to submit your guess
5. Follow the hints (Too high/Too low) to find the number
6. If you win, enter your username to save your score
7. Click "Start Game" to play again

## Game Rules

- The game generates a random number between 1 and the selected range
- You need to guess this number
- After each guess, you'll get a hint if your guess is too high or too low
- The number of tries depends on the selected difficulty level
- Your score is calculated based on how quickly you guess the number
- Only winning scores are saved to the database

## Score System

- Base score: 1000 points
- Points deduction: 100 points per try
- Minimum score: 0 points

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
