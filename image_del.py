import pygame
import os

# Global variable to keep track of deleted pictures
trash_amount = 1

# Button class
class Button:
    def __init__(self, x, y, text, text_color=(0, 0, 0), bg_color=None, rounded_corners=False):
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.rounded_corners = rounded_corners
        self.font = pygame.font.Font(None, 36)  # Default font and size 36
        
        # Render the text and calculate the size
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=(x, y))
        
        # Calculate the size of the button based on the text size
        padding = 10
        self.rect = self.text_rect.inflate(padding*2, padding*2)

    def draw(self, screen):
        if self.bg_color:
            if self.rounded_corners:
                pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)
            else:
                pygame.draw.rect(screen, self.bg_color, self.rect)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)  # White border if bg_color is None

        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def set_text(self, text):
        self.text = text
        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def get_text(self):
        return self.text

# Function to delete all files starting with "picture_"
def delete_all_pictures():
    global trash_amount
    for file in os.listdir():
        if file.lower().startswith("picture") and file.lower().endswith(".png"):
            try:
                file_number = int(file.lower().split("picture")[1].split(".png")[0])
                if 1 <= file_number <= 20:  # Adjusted to include numbers 10 and up
                    os.remove(file)
                    trash_amount += 1
                    print(f"Deleted {file}")
            except ValueError:
                print("error code 1: unable to use bruh")

# Function to delete a specific picture by its number
# Function to delete pictures from picture1.png to picture100.png
def delete_pictures(amount):
    global trash_amount
    for i in range(1, amount):
        file_name = f"picture{i}.png"
        if os.path.exists(file_name):
            os.remove(file_name)
            trash_amount += 1
            print(f"Deleted {file_name}")


# Initialize Pygame
pygame.init()

# Set the width and height of the window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

input_font = pygame.font.Font(None, 32)
text_input = ""
input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 16, 200, 32)
active = False
bruh = 1000000

# Colors
LIGHT_BLUE = (173, 216, 230)  # Light blue
WHITE = (255, 255, 255)

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Delete Pictures")

# Function to draw text on the screen
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)

# Main loop
def main():
    clock = pygame.time.Clock()

    delete_all_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50, "Delete All", (0, 0, 0), LIGHT_BLUE)

    # Text input variable

    running = True
    clock = pygame.time.Clock()

    delete_all_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50, "Delete All", (0, 0, 0), LIGHT_BLUE)

    running = True
    while running:
        # Draw background gradient
        for y in range(WINDOW_HEIGHT):
            color = (255 - int(255 * y / WINDOW_HEIGHT), 255 - int(255 * y / WINDOW_HEIGHT), 255)
            pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if delete_all_button.is_clicked(event):
                    delete_pictures(bruh)

        # Render delete all button
        delete_all_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
