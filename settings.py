import pygame
import sys
import random
import time
from buttons import *
from text import *
import subprocess

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
icon = pygame.image.load("icon.png")
on = pygame.image.load("off.png")
off = pygame.image.load("on.png")
streamer = pygame.image.load("streamer.png")

# Set up the initial state
streamer_mode = False


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
pygame.display.set_caption("pixelOS-settings")
def run(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True)
        print("Script executed successfully!")
    except subprocess.CalledProcessError as e:
        print("Error executing script:", e)
        return result
def button_img(screen, x, y, image):
    rect = image.get_rect()
    rect.topleft = (x, y)
    screen.blit(image, rect)

    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    if rect.collidepoint(mouse_pos) and clicked:
        set_mode()

def set_mode():
    global streamer_mode
    streamer_mode = not streamer_mode  # Toggle streamer_mode
    return streamer_mode


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.mod & pygame.KMOD_CTRL) and (event.key == pygame.K_s):
                pygame.quit()
                sys.exit()

    screen.fill((30, 30, 255))
    button_img(screen, 0, 0, streamer)

    if streamer_mode:  # Display appropriate image based on streamer_mode
        screen.blit(on, (250, 0))
        time.sleep(0.2)
    else:
        screen.blit(off, (250, 0))
        time.sleep(0.2)

    pygame.display.update()
    clock.tick(30)
