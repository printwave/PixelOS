import pygame
import sys
import random
import time
from text import *
from image_del import trash_amount

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
icon = pygame.image.load("icon.png")
logo = pygame.image.load("pixelOS.png")
setting_img = pygame.image.load("settings.png")
camra_img = pygame.image.load("camra.png")
imgdel = pygame.image.load("imgdel.png")
imgdelhalf = pygame.image.load("imgdelhalf.png")
imgdelfull = pygame.image.load("imgdelfull.png")
album_img = pygame.image.load("album.png")
shutdown_img = pygame.image.load("shutdown.png")

# Set up the initial state
shutdown = True
startup = False
first_time = False
home = False
settings = False
result = ""
trash = trash_amount

# Set random values
t1 = random.randrange(1, 11)
t2 = random.randrange(1, 11)
t3 = random.randrange(1, 11)
t4 = random.randrange(1, 11)
t5 = random.randrange(1, 11)
t6 = random.randrange(1, 11)
t7 = random.randrange(1, 11)
t8 = random.randrange(1, 11)
t9 = random.randrange(1, 11)
t0 = random.randrange(1, 11)

# Set color and text variables
color = (255, 255, 255)
text = Text()

# Window settings
pygame.display.set_icon(icon)
pygame.display.set_caption("pixelOS-shutdown")

# Function to draw button and handle click
def button_img(screen, x, y, image):
    rect = image.get_rect()
    rect.topleft = (x, y)
    screen.blit(image, rect)
    return rect

# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if shutdown:
        shutdown = False
        screen.fill((30, 30, 175))
        text.draw_text(screen, 500, 450, "Shutting down")
        pygame.display.update()
        time.sleep(1)  # Reduced time to 1 second for faster testing
        screen.fill((0, 0, 0))
        button_rect = button_img(screen, 450, 300, shutdown_img)
        pygame.display.update()

    # Check if button is clicked
    if button_rect and button_rect.collidepoint(mouse_pos) and clicked:
        pygame.quit()
        sys.exit()

    clock.tick(30)
