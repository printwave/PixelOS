import pygame, sys, time
from box import *
pygame.init()
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("pixelOS-internet")
clock = pygame.time.Clock()
input_box = InputBox(100, 100, 140, 32)
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pl.QUIT:
            done = True
        input_box.handle_event(event)

    input_box.update()

    screen.fill((30, 30, 30))
    input_box.draw(screen)

    pygame.display.flip()
    clock.tick(30)

    
pygame.quit()