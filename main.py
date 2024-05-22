import pygame
import sys
import random
import time
from text import *
from image_del import trash_amount
import subprocess

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
media_img = pygame.image.load("media.png")
wifi_img = pygame.image.load("wifi.png")
timer_img = pygame.image.load("timer.png")
internet_img = pygame.image.load("internet.png")

# Set up the initial state
shutdown = False
startup = False
first_time = False
home = False
settings = False
result = ""
trash = trash_amount
h = True

if h == False:
    startup = True
    first_time = True
    home = False
elif h == True:
    home = True
    startup = False
    first_time = False

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
def check_data():
    try:
        with open("pixelOS_data.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split(" : ")
                if key.strip() == "esp32wfiduyusizea" and value.strip() == "password5":
                    return True
            return False
    except FileNotFoundError:
        print("File not found.")
    except ValueError:
        print("Invalid format in file.")

# Check data


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
    except subprocess.CalledProcessError as e:
        return result

def button_img(screen, x, y, image, file):
    rect = image.get_rect()
    rect.topleft = (x, y)
    screen.blit(image, rect)
    return rect, file

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

# Initialize buttons list
buttons = []
if check_data():
    print("The specified data was found in the file.")
    run("esp32.py")

# Main loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.mod & pygame.KMOD_CTRL) and (event.key == pygame.K_q) and not shutdown:
                shutdown = True

    if first_time and startup:
        first_time, home = handle_startup(first_time)
        startup = False

    if home:
        home = False
        screen.fill((30, 30, 30))
        rect_x = 0
        rect_y = 900 - 75  # Adjusted to bottom of the screen
        rect_width = 1200  # Explicitly setting the width
        rect_height = 75  # Explicitly setting the height
        pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))
        buttons = [
            button_img(screen, 0, 0, setting_img, "settings.py"),
            button_img(screen, 300, 0, camra_img, "camra.py"),
            button_img(screen, 600, 0, album_img, "album.py"),
            button_img(screen, 900, 0, media_img, "music_player.py"),
            button_img(screen, 1100, 800 ,wifi_img, "wifi.py"),
            button_img(screen, 0, 300, timer_img, "clock.py"),
            button_img(screen, 300, 300, internet_img, "internet.py")
        ]
        if trash < 50 and trash > 0:
            buttons.append(button_img(screen, 600, 0, imgdel, "image_del.py"))
        elif trash > 50 and trash < 100:
            buttons.append(button_img(screen, 600, 0, imgdelhalf, "image_del.py"))
        elif trash > 100:
            buttons.append(button_img(screen, 600, 0, imgdelfull, "image_del.py"))
        pygame.display.flip()

        
    if shutdown:
        run("shutdown.py")
        time.sleep(1)
        shutdown = False

    for button_rect, script_name in buttons:
        if button_rect.collidepoint(mouse_pos) and clicked:
            run(script_name)

    clock.tick(30)
