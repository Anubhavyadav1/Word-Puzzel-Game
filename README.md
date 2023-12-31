# Word-Puzzel-Game

## Word Puzzle Game

### Overview
This Python script implements a simple Word Puzzle game with an AI component. The game generates a random grid of letters, and the player can select letters to form words. The AI component then attempts to find and display additional valid words on the grid.

### Dependencies
pygame: A library for creating games and multimedia applications in Python.
nltk: The Natural Language Toolkit, used for working with human language data.
string: A module providing common string operations.

### Usage
Run the script, and a window will open, displaying the Word Puzzle game. The player can select letters to form words. The AI component finds additional valid words on the grid and displays their paths.

### Main Components

1. Game Initialization and Configuration
Pygame Initialization: Initializes the Pygame library for graphical display.
NLTK Words Dataset: Checks if the NLTK words dataset is available and downloads it if not.
Colors: Defines color constants used in the game.

2. Grid Generation
generate_grid(grid_size, english_letter_ratio): Generates a random grid of letters with a specified size and a given ratio of English letters.

3. Game Logic and Display
Main Loop (main()): Manages the main game loop, including player input, grid display, and AI word search solution.
draw_grid(screen, grid, cell_size, selected_cells): Displays the grid with selected cells highlighted.
draw_word_list(screen, traced_words, screen_width, title_visible, scroll_offset): Displays the list of traced words on the right side of the window.
draw_attempted_path(screen, path, cell_size): Displays the attempted path in red.

4. Word Search AI
get_random_word(grid): Retrieves a random meaningful word from the NLTK words dataset based on the letters available in the grid.
find_english_words_with_paths(grid): Searches for English words and their paths in the grid.
solve_puzzle(grid): Solves the Word puzzle using the AI component.

5. User Interaction
get_grid_size(): Uses Tkinter to prompt the user for the grid size.

### How to Play
Run the script.
Enter the size of the grid when prompted.
Select letters on the grid to form words.
The AI component finds additional words and displays their paths.
The traced words are listed on the right side of the window.


### Notes
Ensure that the required dependencies (pygame, nltk) are installed before running the script.
The script may need an internet connection to download the NLTK words dataset.
The AI component uses NLTK's English words dataset to find valid words on the grid.
