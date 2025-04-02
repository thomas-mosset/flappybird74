# import pygame
import pygame

# initialization of pygame
pygame.init()

# game's constants
WIDTH = 1280
HEIGHT = 720

# game's variables
clock = pygame.time.Clock()
running = True

# game's colors
WHITE = (255, 255, 255)

# screen creation
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird 74")


while running:
    # fill the screen with a color
    screen.fill("#1C9AD2")

    # events management
    for event in pygame.event.get():
        # pygame .QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    # Render game here


    # refresh the screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)

pygame.quit()