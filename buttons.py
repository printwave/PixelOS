import pygame
import sys

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

