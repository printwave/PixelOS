import pygame
import sys
import os

pygame.init()

screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("pixelOS-wifi")

# Path for storing connection status in the same folder
data_file_path = os.path.join(os.path.dirname(__file__), "pixelOS_data.txt")

# Function to save connection status
def save_connection_status(network, password):
    lines = []
    if os.path.exists(data_file_path):
        with open(data_file_path, "r") as f:
            lines = f.readlines()
        # Check if the network already exists
        for line in lines:
            if line.startswith(network + " : "):
                return  # If the network already exists, do nothing
    with open(data_file_path, "a") as f:
        f.write(f"{network} : {password}\n")

# Function to load connection status
def load_connection_status():
    if os.path.exists(data_file_path):
        with open(data_file_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            network, password = line.strip().split(" : ")
            if network in network_passwords and network_passwords[network] == password:
                return network
    return None

# Button class
class Button:
    def __init__(self, x, y, text, text_color=(0, 0, 0), bg_color=None, rounded_corners=False):
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.rounded_corners = rounded_corners
        self.font = pygame.font.Font(None, 36)
        
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=(x, y))
        
        padding = 10
        self.rect = self.text_rect.inflate(padding*2, padding*2)

    def draw(self, screen):
        if self.bg_color:
            if self.rounded_corners:
                pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)
            else:
                pygame.draw.rect(screen, self.bg_color, self.rect)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Text:
    def __init__(self):
        pygame.init()

    def draw_text(self, screen, x, y, text, color=(255, 255, 255)):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(str(text), True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Define the network passwords
network_passwords = {
    "MyWifi0987": "password1",
    "MyWifi9827": "password2",
    "MyWifi0567": "password3",
    "MyWifi-guest": "password4",
    "esp32wfiduyusizea": "password5",
    "Walmart-guest": "password6",
    "Target-guest": "password7",
    "Xfinity": "password8"
}

text_drawer = Text()

networks = [
    "MyWifi0987",
    "MyWifi9827",
    "MyWifi0567",
    "MyWifi-guest",
    "esp32wfiduyusizea",
    "Walmart-guest",
    "Target-guest",
    "Xfinity"
]

buttons = []
input_boxes = []
button_x = 300
button_y_start = 150
button_y_gap = 50

for i, network in enumerate(networks):
    button_y = button_y_start + i * button_y_gap
    buttons.append(Button(button_x, button_y, "Connect", text_color=(0, 0, 0), bg_color=(200, 200, 200), rounded_corners=True))
    input_boxes.append(InputBox(button_x + 150, button_y - 15, 200, 40))

current_input_box = None
connected_network = None

connected_network = load_connection_status()
wifi = bool(connected_network)
connected_password = network_passwords[connected_network] if connected_network else None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_input_box:
            password = current_input_box.handle_event(event)
            if password is not None:
                network_index = input_boxes.index(current_input_box)
                if password == network_passwords[networks[network_index]]:
                    wifi = True
                    connected_network = networks[network_index]
                    connected_password = password
                    save_connection_status(connected_network, password)
                else:
                    wifi = False
                current_input_box.active = False
                current_input_box = None
        else:
            for i, button in enumerate(buttons):
                if button.is_clicked(event):
                    current_input_box = input_boxes[i]
                    current_input_box.active = True
                    break

    screen.fill((30, 30, 125))
    
    text_drawer.draw_text(screen, 0, 0, "WIFI")
    if wifi and connected_network:
        text_drawer.draw_text(screen, 0, 50, f"Connected to {connected_network}")
    else:
        text_drawer.draw_text(screen, 0, 50, "Disconnected")
    
    text_drawer.draw_text(screen, 0, 100, "Networks")
    for i, network in enumerate(networks):
        text_drawer.draw_text(screen, 0, button_y_start + i * button_y_gap, network)
        buttons[i].draw(screen)
        if input_boxes[i].active:
            input_boxes[i].draw(screen)
    
    pygame.display.update()
