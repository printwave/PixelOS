import pygame

class Text:
    def __init__(self):
        pygame.init()

    def draw_text(self, screen, x, y, text, color=(255, 255, 255)):
        font = pygame.font.Font(None, 36)  # You can adjust the font and size here
        text_surface = font.render(str(text), True, color)  # Convert text to str
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)
