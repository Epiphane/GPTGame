import pygame
import random

# Game settings
WINDOW_SIZE = (400, 400)
PUZZLE_SIZE = 4
TILE_SIZE = WINDOW_SIZE[0] // PUZZLE_SIZE

# Shape definitions
SHAPES = [
    "square",
    "rectangle",
    "circle",
    "diamond"
]

# Color palette
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0)   # Yellow
]

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Puzzle Game")

# Create the puzzle grid
def create_puzzle(size):
    puzzle = [[None] * size for _ in range(size)]
    available_tiles = []

    # Generate available tiles
    for shape in SHAPES:
        for color in COLORS:
            available_tiles.append({"shape": shape, "color": color})

    # Randomly populate the puzzle grid
    for row in range(size):
        for col in range(size):
            if row == size - 1 and col == size - 1:
                continue  # Skip the last tile (empty tile)
            tile = random.choice(available_tiles)
            puzzle[row][col] = tile
            available_tiles.remove(tile)

    return puzzle

# Draw the puzzle grid on the window
def draw_puzzle(puzzle):
    window.fill((0, 0, 0))  # Black background
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile = puzzle[row][col]
            if tile:
                shape = tile["shape"]
                color = tile["color"]
                if shape == "square":
                    pygame.draw.rect(window, color, (x, y, TILE_SIZE, TILE_SIZE))
                elif shape == "rectangle":
                    pygame.draw.rect(window, color, (x, y, TILE_SIZE, TILE_SIZE // 2))
                elif shape == "circle":
                    pygame.draw.circle(window, color, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 2)
                elif shape == "diamond":
                    pygame.draw.polygon(window, color, [
                        (x + TILE_SIZE // 2, y),
                        (x + TILE_SIZE, y + TILE_SIZE // 2),
                        (x + TILE_SIZE // 2, y + TILE_SIZE),
                        (x, y + TILE_SIZE // 2)
                    ])
    pygame.display.flip()

# Check if the puzzle is solved
def is_solved(puzzle):
    # Check if every row has only one shape type
    for row in range(len(puzzle) - 1):
        row_tiles = [tile for tile in puzzle[row] if tile is not None]
        if len(set(tile["shape"] for tile in row_tiles)) != 1:
            return False

    # Check if every column has only one color
    for col in range(len(puzzle[0])):
        if not puzzle[-1][col]:  # Ignore the empty tile column
            continue
        color = puzzle[-1][col]["color"]
        if any(puzzle[row][col] and puzzle[row][col]["color"] != color for row in range(len(puzzle) - 1)):
            return False

    return True




# Play the puzzle game
def play_puzzle():
    puzzle = create_puzzle(PUZZLE_SIZE)
    empty_row = PUZZLE_SIZE - 1
    empty_col = PUZZLE_SIZE - 1

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // TILE_SIZE
                    row = mouse_y // TILE_SIZE
                    if (
                        (col == empty_col and abs(row - empty_row) == 1)
                        or (row == empty_row and abs(col - empty_col) == 1)
                    ):
                        puzzle[row][col], puzzle[empty_row][empty_col] = puzzle[empty_row][empty_col], puzzle[row][col]
                        empty_row, empty_col = row, col

        draw_puzzle(puzzle)

        if is_solved(puzzle):
            font = pygame.font.Font(None, 48)
            text = font.render("Congratulations!", True, (255, 255, 255))  # White text color
            text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            window.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        clock.tick(60)

# Run the puzzle game
play_puzzle()

# Quit Pygame
pygame.quit()
