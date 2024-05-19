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
logo = pygame.image.load("pixelOS.png")
setting_img = pygame.image.load("settings.png")

# Set up the initial state
startup = True
first_time = True
home = False
settings = False
result = ""

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
pygame.display.set_caption("pixelOS")

def handle_startup(first_time):
    if first_time:
        display_text_sequence([
            "collecting data",
            "downloading PixelOS",
            "downloading PixelSoundDriver2.0.1",
            "downloading PixelDisplayDriver2.0.1",
            "downloading PixelSystem",
            "downloading PixelMicrophoneDrivers1.9.1",
            "connecting to Pixelnet",
            "downloading PixelNetworkDrivers2.0.2",
            "Almost done!",
            "Finished"
        ], logo, [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9])
    else:
        display_text_sequence([
            "starting up",
            "loading files",
            "finished"
        ], logo, [20, t9, t2])
    return False, True

def display_text_sequence(texts, image, delays):
    for i, text_msg in enumerate(texts):
        screen.fill((30, 30, 255))
        screen.blit(image, (450, 200))
        text.draw_text(screen, 500, 500, text_msg, color)
        pygame.display.flip()
        delay = delays[i] if i < len(delays) else 2
        time.sleep(delay)
def run(script_name):
    global result
    try:
        result = subprocess.run(['python', script_name], check=True)
        print("Script executed successfully!")
    except subprocess.CalledProcessError as e:
        print("Error executing script:", e)
        return result
def button_img(screen, x, y, image, file):
    rect = image.get_rect()
    rect.topleft = (x, y)
    screen.blit(image, rect)

    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    if rect.collidepoint(mouse_pos):
        if clicked:
            run(file)
def get(script_name, var_name):
    try:
        with open(script_name, 'r') as f:
            script_code = f.read()
        # Execute the script code in a controlled environment
        local_vars = {}
        global_vars = {}
        exec(script_code, global_vars, local_vars)
        # Retrieve the value of the variable
        if var_name in local_vars:
            return local_vars[var_name]
        elif var_name in global_vars:
            return global_vars[var_name]
        else:
            print(f"Variable '{var_name}' not found in '{script_name}'.")
            return None
    except Exception as e:
        print(f"Error occurred while getting variable '{var_name}' from '{script_name}': {e}")
        return None
streamer = get("settings.py","streamer_mode" )
with open("settings.txt", "a") as f:
    f.write("streamer mode:")
with open("settings.txt", "a") as f:
    f.write(str(streamer))


# Main loop
while True:
    button_rect = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.mod & pygame.KMOD_CTRL) and (event.key == pygame.K_s):
                pygame.quit()
                sys.exit()


    if first_time and startup:
        first_time, home = handle_startup(first_time)
        startup = False

    if startup and not first_time:
        startup, home = handle_startup(first_time)

    if home:
       screen.fill((30, 30, 30))
       button_img(screen, 0, 0, setting_img, "settings.py")
       pygame.display.flip()
            




    clock.tick(30)
