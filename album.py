import pygame
import os
import time

# Initialize Pygame
pygame.init()

# Set the width and height of the window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

# Number of pictures to fit in one row and one column
NUM_ROWS = 3
NUM_COLS = 3

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Photo Album")

# Function to load and display images
def display_images(images, scroll_offset):
    screen.fill((255, 255, 255))  # Fill the screen with white color

    # Calculate the width and height of each image cell
    cell_width = WINDOW_WIDTH // NUM_COLS
    cell_height = WINDOW_HEIGHT // NUM_ROWS

    # Display each image in a grid
    for i, image_path in enumerate(images):
        row = i // NUM_COLS
        col = i % NUM_COLS

        # Calculate the position of the image cell
        cell_x = col * cell_width
        cell_y = row * cell_height - scroll_offset

        # Check if the image cell is within the visible portion of the window
        if cell_y + cell_height > 0 and cell_y < WINDOW_HEIGHT:
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (cell_width, cell_height))
                screen.blit(image, (cell_x, cell_y))
            except pygame.error as e:
                print(f"Error loading image: {e}")

    pygame.display.flip()

# Function to get all image files in the current directory
def get_image_files():
    image_files = [file for file in os.listdir() if file.lower().startswith('picture') and file.lower().endswith('.png')]
    image_files.sort(key=lambda x: int(x.split('picture')[1].split('.png')[0]))
    return image_files

# Main loop
running = True
scroll_offset = 0
scroll_delay = 0.1  # Delay in seconds
last_scroll_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_time = time.time()
            if event.button == 4 and current_time - last_scroll_time > scroll_delay:  # Scroll up
                scroll_offset += WINDOW_HEIGHT // (NUM_ROWS * 2)
                last_scroll_time = current_time
            elif event.button == 5 and current_time - last_scroll_time > scroll_delay:  # Scroll down
                scroll_offset -= WINDOW_HEIGHT // (NUM_ROWS * 2)
                last_scroll_time = current_time

    # Cap scroll offset to limit scrolling beyond image boundaries
    max_scroll_offset = max(0, len(get_image_files()) * (WINDOW_HEIGHT // NUM_ROWS) - WINDOW_HEIGHT)
    scroll_offset = max(0, min(scroll_offset, max_scroll_offset))

    # Get all image files in the current directory
    image_files = get_image_files()

    # Determine the index of the first visible image
    first_visible_index = scroll_offset // (WINDOW_HEIGHT // NUM_ROWS)

    # Display images
    display_images(image_files[first_visible_index:], scroll_offset)

pygame.quit()
