import pygame
import pygame.locals as pl
from box import InputBox
from text import Text
import subprocess

# Function to check if the input is in the list of websites
def check_input_in_list(user_input, websites):
    user_input = user_input.strip()  # Remove leading and trailing whitespace
    for website in websites:
        if user_input == website.strip():  # Remove leading and trailing whitespace from website
            return True
    return False

pygame.init()
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("pixelOS-pixelnet")
clock = pygame.time.Clock()
input_box = InputBox(120, 45, 120, 32, 32, "pixelnet.com")
done = False

# List of predefined websites
websites = ["pixelnet.com", "youtube.com", "python.org"]

while not done:
    for event in pygame.event.get():
        if event.type == pl.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            input_box.handle_event(event)  # Handle mouse click events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_box.active:
                    user_input = input_box.get_text()
                    if check_input_in_list(user_input, websites):
                        filename = user_input[:-4] + ".py"  # Remove the last 4 characters and add ".py"
                        subprocess.run(["python", filename])  # Execute the Python file
                    else:
                        print(f"{user_input} is not in the list.") # Deactivate input box after processing Enter key press
            elif input_box.active:  # Handle keyboard events only when input box is active
                input_box.handle_event(event)

    input_box.update()

    screen.fill((30, 30, 30))
    Text.draw_text(screen, screen, 0, 50, "PixelNet")  # Assuming this is the correct method call
    input_box.draw(screen)

    pygame.display.flip()
    clock.tick(30)