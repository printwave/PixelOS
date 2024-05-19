import pygame
import cv2

# Initialize Pygame
pygame.init()

# Set the width and height of the window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Camera Viewer")

# Initialize the camera
camera = cv2.VideoCapture(1)  # change the number to match the camera. Use 0 for default.

# Function to take a picture and save it
def take_picture(file_name):
    ret, frame = camera.read()  # Read a frame from the camera
    cv2.imwrite(file_name, frame)  # Save the frame as an image
class Text:
    def __init__(self):
        pygame.init()

    def draw_text(self, x, y, text, color=(255, 255, 255)):
        font = pygame.font.Font(None, 36)  # You can adjust the font and size here
        text_surface = font.render(str(text), True, color)  # Convert text to str
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

# Main loop
running = True
picture_count = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Press space to take a picture
                picture_name = f"picture{picture_count}.png"
                take_picture(picture_name)
                picture_count += 1

    # Read a frame from the camera
    ret, frame = camera.read()

    # Mirror flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert the frame from OpenCV's BGR format to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize the frame to fit the Pygame window
    frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Convert the frame to Pygame surface
    frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")

    # Display the frame on the Pygame window
    screen.blit(frame_surface, (0, 0))
    Text.draw_text(screen, 450, 750, "press space to take picture", (0, 0, 0))
    pygame.display.flip()

# Release the camera and close Pygame
camera.release()
pygame.quit()
