import pygame
import random
import string
import tkinter as tk
from tkinter import simpledialog
import nltk
from nltk.corpus import words as nltk_words
import pygame.time
from collections import deque
import ssl 


# Check if NLTK words dataset is present, if not, download it
try:
    nltk_words.words()
except LookupError:
    print("Downloading NLTK words dataset...")
    
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('words')



# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialize PyGame
pygame.init()

# Function to generate a random grid of letters
def generate_grid(grid_size, english_letter_ratio):
    english_letters = string.ascii_uppercase
    total_cells = grid_size * grid_size
    english_letter_cells = int(total_cells * english_letter_ratio)

    # Generate a grid with random letters
    grid = [
        [random.choice(english_letters) if random.random() < english_letter_ratio else random.choice(string.ascii_uppercase) 
         for _ in range(grid_size)] for _ in range(grid_size)
    ]

    return grid

# Function to draw the grid on the screen
def draw_grid(screen, grid, cell_size, selected_cells):
    highlight_color = (0, 255, 0, 128)  # Green with 50% transparency

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            x, y, width, height = col * cell_size, row * cell_size, cell_size, cell_size
            rect = pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
            font = pygame.font.Font(None, min(36, cell_size - 10))  # Adjusted font size
            text = font.render(grid[row][col], True, BLACK)
            screen.blit(text, (x + width // 4, y + height // 4))

    if selected_cells:
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        for row, col in selected_cells:
            x, y, width, height = col * cell_size, row * cell_size, cell_size, cell_size
            pygame.draw.rect(overlay, highlight_color, (x, y, width, height), 0)
        screen.blit(overlay, (0, 0))

    pygame.display.flip()

# Function to display traced words with a right-aligned title
def draw_word_list(screen, traced_words, screen_width, title_visible, scroll_offset):
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 40)
    margin = 20
    
    # Convert traced_words set to a list
    traced_words_list = list(traced_words)

    # Render the title once at the beginning of the game
    title_text = title_font.render("Completed Words", True, BLACK)
    title_width, title_height = title_text.get_size()

    # Position the title on the right side
    title_x = screen_width - title_width

    # Blit the pre-rendered title surface instead of re-rendering every frame
    screen.blit(title_text, (title_x, 0))

    # Calculate visible word count
    total_visible_words = min(10, len(traced_words_list))
    visible_word_count = min(total_visible_words, len(traced_words_list) - scroll_offset)

    # Display only a portion of the traced words based on scroll_offset
    for i in range(scroll_offset, scroll_offset + visible_word_count):
        if 0 <= i < len(traced_words_list):
            word = traced_words_list[i]
            text = font.render(word, True, BLACK)
            x = screen_width - title_width
            y = (i) * (text.get_height() + margin) + title_height  # Adjusted vertical position below the title
            screen.blit(text, (x, y))

# Function to get a random meaningful word
def get_random_word(grid):
    word_list = nltk_words.words()
    meaningful_words = [word.lower() for word in word_list if 4 <= len(word) <= 8]

    valid_words = []

    for word in meaningful_words:
        word_letters = set(word)
        board_letters = set(letter.upper() for row in grid for letter in row)
        if word_letters.issubset(board_letters):
            valid_words.append(word.upper())

    return random.choice(valid_words) if valid_words else None

# Function to get the grid size from the user using tkinter
def get_grid_size():
    root = tk.Tk()
    root.withdraw()
    size = simpledialog.askinteger("Grid size", "Enter size of map: ")
    return size

def draw_attempted_path(screen, path, cell_size):
    path_color = (255, 0, 0)  # Red color for attempted paths

    for row, col in path:
        x, y, width, height = col * cell_size, row * cell_size, cell_size, cell_size
        pygame.draw.rect(screen, path_color, (x, y, width, height), 0)

    pygame.display.flip()

# Function to find English words and their paths in the grid
def find_english_words_with_paths(grid):
    words_with_paths = {}
    grid_size = len(grid)

    # Load the NLTK English words
    english_words = set(nltk_words.words())

    # Function to check if the given coordinates are within the grid
    def is_valid_coord(row, col):
        return 0 <= row < grid_size and 0 <= col < grid_size

    # Function to search for words starting from a given position
    def search_from_position(row, col, direction):
        path = []
        word = ""
        while is_valid_coord(row, col):
            path.append((row, col))
            word += grid[row][col]
            row, col = row + direction[0], col + direction[1]
        return word, path

    # Iterate over all positions in the grid
    for row in range(grid_size):
        for col in range(grid_size):
            # Search horizontally
            word, path = search_from_position(row, col, (0, 1))
            if word.lower() in english_words:
                words_with_paths[word] = path

            # Search vertically
            word, path = search_from_position(row, col, (1, 0))
            if word.lower() in english_words:
                words_with_paths[word] = path

            # Search diagonally (up-right)
            word, path = search_from_position(row, col, (-1, 1))
            if word.lower() in english_words:
                words_with_paths[word] = path

            # Search diagonally (down-right)
            word, path = search_from_position(row, col, (1, 1))
            if word.lower() in english_words:
                words_with_paths[word] = path

    return words_with_paths

# Function to solve the word search puzzle
def solve_puzzle(grid):
    return find_english_words_with_paths(grid)

def main():
    # Get the grid size from the user
    grid_size = get_grid_size()
    english_word_percentage = 0.2

    # Constants
    cell_size = max(20, min(800 // grid_size, 800 // grid_size))
    width, height = grid_size * cell_size, grid_size * cell_size

    # Create a window
    screen = pygame.display.set_mode((width + 600, height))
    pygame.display.set_caption("Word Search Puzzle AI")

    # Generate a random grid
    grid = generate_grid(grid_size, english_word_percentage)

    # Main game loop
    running = True
    title_visible = True

    selected_cells = set()
    completed_words = set()

    # Traced words list
    traced_words = set()

    # Initialize current_word
    current_word = get_random_word(grid)

    # Enable double buffering
    # Create a window with VSync enabled
    pygame.display.set_mode((width + 600, height), pygame.HWSURFACE)

    # Set up clock for controlling frame rate
    clock = pygame.time.Clock()

    scroll_offset = 0  # Initial scroll offset

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // cell_size
                col = x // cell_size
                clicked_cell = (row, col)

                if clicked_cell in selected_cells:
                    # Deselect the cell if it's already selected
                    selected_cells.remove(clicked_cell)
                else:
                    if 0 <= row < grid_size and 0 <= col < grid_size:
                        selected_cells.add(clicked_cell)

                        # Check if the selected cells form a complete word
                        word = ''.join([grid[row][col] for row, col in selected_cells if 0 <= row < grid_size and 0 <= col < grid_size])
                        if word == current_word:
                            traced_words.add(word)
                            selected_cells.clear()
                            current_word = get_random_word(grid)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Scroll up
                scroll_offset = max(0, scroll_offset - 1)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Scroll down
                scroll_offset = min(len(traced_words) - 1, scroll_offset + 1)
        
        # Draw the grid
        screen.fill(WHITE)
        # Draw the traced words list on the right-hand side
        draw_word_list(screen, traced_words, width + 400, title_visible, scroll_offset)
        draw_grid(screen, grid, cell_size, selected_cells)

        ai_solution = solve_puzzle(grid)
        for word, path in ai_solution.items():
            if word not in traced_words:
                traced_words.add(word)
                completed_words.add(word)
                draw_attempted_path(screen, path, cell_size)

        pygame.display.flip()

        clock.tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    # Main function here
    main()
