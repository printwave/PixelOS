import pygame
import time
import threading

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1200, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Timer and Stopwatch")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define fonts
FONT = pygame.font.SysFont(None, 30)

# Global variables
mode = "timer"
running = False
timer_thread = None
stopwatch_thread = None
timer_display = "00:00:00"
stopwatch_display = "00:00:00:000"

# Timer class
class Timer:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.total_seconds = hours * 3600 + minutes * 60 + seconds
        self._stop = False

    def start(self):
        global timer_display
        while self.total_seconds > 0 and running:
            hours = self.total_seconds // 3600
            minutes = (self.total_seconds % 3600) // 60
            seconds = self.total_seconds % 60
            timer_display = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            time.sleep(1)
            self.total_seconds -= 1

        if self.total_seconds == 0:
            pygame.mixer.Sound('beep.wav').play()

    def stop(self):
        self._stop = True

    def restart(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.total_seconds = hours * 3600 + minutes * 60 + seconds
        self._stop = False

# Stopwatch class
class Stopwatch:
    def __init__(self):
        self.start_time = time.time()
        self._stop = False

    def start(self):
        global stopwatch_display
        while running:
            elapsed_time = time.time() - self.start_time
            milliseconds = int(elapsed_time * 1000)
            hours = milliseconds // (3600 * 1000)
            minutes = (milliseconds % (3600 * 1000)) // (60 * 1000)
            seconds = (milliseconds % (60 * 1000)) // 1000
            ms = milliseconds % 1000
            stopwatch_display = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{ms:03d}"
            time.sleep(0.01)

    def stop(self):
        self._stop = True

    def restart(self):
        self.start_time = time.time()
        self._stop = False

# Function to draw text on the screen
def draw_text(text, x, y):
    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    WIN.blit(text_surface, text_rect)

# Function to draw buttons
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(WIN, color, (x, y, width, height))
    draw_text(text, x + width // 2, y + height // 2)

# Function to handle the timer countdown
def handle_timer(timer):
    timer.start()

# Function to handle the stopwatch counting
def handle_stopwatch(stopwatch):
    stopwatch.start()

def main():
    global mode, running, timer_thread, stopwatch_thread

    # Initialize timer and stopwatch
    timer = Timer()
    stopwatch = Stopwatch()

    hours = 0
    minutes = 0
    seconds = 0

    input_boxes = [
        pygame.Rect(120, HEIGHT // 2 - 40, 50, 30),
        pygame.Rect(180, HEIGHT // 2 - 40, 50, 30),
        pygame.Rect(240, HEIGHT // 2 - 40, 50, 30)
    ]

    active_box = None
    user_input = ["0", "0", "0"]
    active_index = None

    # Game loop
    running_game = True
    while running_game:
        WIN.fill(WHITE)

        if mode == "timer":
            draw_text("Timer: ", WIDTH // 2, HEIGHT // 4 - 50)

            # Draw input boxes and user input
            for i, box in enumerate(input_boxes):
                pygame.draw.rect(WIN, GRAY if box != active_box else BLACK, box, 2)
                draw_text(user_input[i], box.x + box.width // 2, box.y + box.height // 2)

            # Draw buttons
            draw_button("Start", WIDTH // 4 - 40, 3 * HEIGHT // 4, 70, 30, GREEN)
            draw_button("Stop", WIDTH // 2 - 35, 3 * HEIGHT // 4, 70, 30, RED)
            draw_button("Restart", 3 * WIDTH // 4 - 30, 3 * HEIGHT // 4, 70, 30, GRAY)
            draw_button("Stopwatch", WIDTH // 2 - 50, HEIGHT - 40, 100, 30, GRAY)

            # Display the timer
            draw_text(timer_display, WIDTH // 2, HEIGHT // 2 - 70)

        elif mode == "stopwatch":
            draw_text("Stopwatch: ", WIDTH // 2, HEIGHT // 4 - 50)
            # Draw buttons
            draw_button("Start", WIDTH // 4 - 40, 3 * HEIGHT // 4, 70, 30, GREEN)
            draw_button("Stop", WIDTH // 2 - 35, 3 * HEIGHT // 4, 70, 30, RED)
            draw_button("Restart", 3 * WIDTH // 4 - 30, 3 * HEIGHT // 4, 70, 30, GRAY)
            draw_button("Timer", WIDTH // 2 - 50, HEIGHT - 40, 100, 30, GRAY)

            # Display the stopwatch
            draw_text(stopwatch_display, WIDTH // 2, HEIGHT // 2 - 70)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if any input box is clicked
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(mouse_x, mouse_y):
                        active_box = box
                        active_index = i
                        break
                else:
                    active_box = None
                    active_index = None

                # Timer mode button actions
                if mode == "timer":
                    if WIDTH // 4 - 40 < mouse_x < WIDTH // 4 + 30 and 3 * HEIGHT // 4 < mouse_y < 3 * HEIGHT // 4 + 30:
                        if not running:
                            running = True
                            hours = int(user_input[0])
                            minutes = int(user_input[1])
                            seconds = int(user_input[2])
                            timer.restart(hours, minutes, seconds)
                            timer_thread = threading.Thread(target=handle_timer, args=(timer,))
                            timer_thread.start()
                    elif WIDTH // 2 - 35 < mouse_x < WIDTH // 2 + 35 and 3 * HEIGHT // 4 < mouse_y < 3 * HEIGHT // 4 + 30:
                        running = False
                        if timer_thread is not None:
                            timer_thread = None
                    elif 3 * WIDTH // 4 - 30 < mouse_x < 3 * WIDTH // 4 + 40 and 3 * HEIGHT // 4 < mouse_y < 3 * HEIGHT // 4 + 30:
                        running = False
                        if timer_thread is not None:
                            timer_thread = None
                        timer.restart(hours, minutes, seconds)
                    elif WIDTH // 2 - 50 < mouse_x < WIDTH // 2 + 50 and HEIGHT - 40 < mouse_y < HEIGHT - 10:
                        running = False
                        mode = "stopwatch"

                # Stopwatch mode button actions
                elif mode == "stopwatch":
                    if WIDTH // 4 - 40 < mouse_x < WIDTH // 4 + 30 and 3 * HEIGHT // 4 < mouse_y < 3 * HEIGHT // 4 + 30:
                        if not running:
                            running = True
                            stopwatch.restart()
                            stopwatch_thread = threading.Thread(target=handle_stopwatch, args=(stopwatch,))
                            stopwatch_thread.start()
                    elif WIDTH // 2 - 35 < mouse_x < WIDTH // 2 + 35 and 3 * HEIGHT // 4 < mouse_y < 3 * HEIGHT // 4 + 30:
                        running = False
                        if stopwatch_thread is not None:
                            stopwatch_thread = None
                    elif 3 * WIDTH // 4 - 30 < mouse_x < 3 * WIDTH // 4 + 40 and 3 * HEIGHT // 4 < mouse_y < 3 * HEIGHT // 4 + 30:
                        running = False
                        if stopwatch_thread is not None:
                            stopwatch_thread = None
                        stopwatch.restart()
                    
                    
                    elif WIDTH // 2 - 50 < mouse_x < WIDTH // 2 + 50 and HEIGHT - 40 < mouse_y < HEIGHT - 10:
                        running = False
                        mode = "timer"

            elif event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_BACKSPACE:
                    user_input[active_index] = user_input[active_index][:-1]
                elif event.unicode.isdigit():
                    user_input[active_index] += event.unicode

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
