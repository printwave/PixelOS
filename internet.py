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
pygame.display.set_caption("pixelOS-internet")
clock = pygame.time.Clock()
input_box = InputBox(200, 50, 120, 32, 32, "pixelnet.com")
search_bar = InputBox(475, 450, 120, 32, 32)
done = False

# List of predefined websites
websites = ["pixelnet.com"]
search_tags = ["python", "minecraft"]

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
                if search_bar.active:
                    user_input1 = input_box.get_text()
                    if check_input_in_list(user_input1, search_tags):
                        filename = user_input[:-4] + ".py"  # Remove the last 4 characters and add ".py"
                        subprocess.run(["python", filename])  # Execute the Python file


            elif input_box.active:  # Handle keyboard events only when input box is active
                input_box.handle_event(event)
            elif search_bar.active:
                search_bar.handle_event(event)

    input_box.update()
    search_bar.update()

    screen.fill((30, 30, 30))
    Text.draw_text(screen, screen, 0, 50, "Pixelbrowser")  # Assuming this is the correct method call
    Text.draw_text(screen, screen, 525, 400, "Pixelnet")
    input_box.draw(screen)
    search_bar.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

