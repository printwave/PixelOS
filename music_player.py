import os
import pygame
import tkinter as tk
from tkinter import filedialog

# Initialize Pygame
pygame.init()

# Set up window
window_width, window_height = 1200, 900
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Media Player")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Function to open file dialog and select media file
def import_media():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    media_file = filedialog.askopenfilename(filetypes=[("Media Files", "*.mp3 *.wav")])
    if media_file:
        return media_file

# Main loop
running = True
current_file_index = 0
media_files = []
progress = 0

# Preload music files
preloaded_sounds = {}

current_music = None  # Variable to store currently playing music

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is clicked within the import button area
            if event.pos[0] >= window_width - 100 and event.pos[1] <= 100:
                new_file = import_media()
                if new_file:
                    media_files.append(new_file)
                    # Preload the new file
                    preloaded_sounds[new_file] = pygame.mixer.Sound(new_file)

            # Check if the mouse is clicked within the next button area
            if window_width - 100 <= event.pos[0] <= window_width and window_height - 100 <= event.pos[1] <= window_height:
                if media_files:  # Check if media_files is not empty
                    current_file_index = (current_file_index + 1) % len(media_files)
                    progress = 0
                    # Stop the current music
                    if current_music:
                        pygame.mixer.music.stop()

            # Check if the mouse is clicked within the previous button area
            if 0 <= event.pos[0] <= 100 and window_height - 100 <= event.pos[1] <= window_height:
                if media_files:  # Check if media_files is not empty
                    current_file_index = (current_file_index - 1) % len(media_files)
                    progress = 0
                    # Stop the current music
                    if current_music:
                        pygame.mixer.music.stop()

    # Draw the window
    window.fill(WHITE)

    # Draw the import button
    pygame.draw.rect(window, GRAY, [window_width - 100, 0, 100, 100])
    import_text = font.render("Import", True, BLACK)
    window.blit(import_text, (window_width - 90, 10))

    # Draw the next button
    pygame.draw.rect(window, GRAY, [window_width - 100, window_height - 100, 100, 100])
    next_text = font.render("Next", True, BLACK)
    window.blit(next_text, (window_width - 90, window_height - 90))

    # Draw the previous button
    pygame.draw.rect(window, GRAY, [0, window_height - 100, 100, 100])
    prev_text = font.render("Prev", True, BLACK)
    window.blit(prev_text, (10, window_height - 90))

    # Draw the progress bar
    progress_width = int(window_width * progress)
    pygame.draw.rect(window, BLUE, [0, window_height - 50, progress_width, 50])

    # Draw the current song name
    if media_files:  # Check if media_files is not empty
        current_file = media_files[current_file_index]
        current_text = font.render(os.path.basename(current_file), True, BLACK)
        window.blit(current_text, (10, 10))

    pygame.display.flip()

    # Play the current song
    if media_files and pygame.mixer.music.get_busy() == 0:  # Check if media_files is not empty
        current_music = current_file  # Update the current music
        preloaded_sounds[current_file].play()
    else:
        if pygame.mixer.music.get_busy():  # Check if music is playing
            progress = pygame.mixer.music.get_pos() / 1000.0 / preloaded_sounds[current_file].get_length()

# Quit Pygame
pygame.quit()
