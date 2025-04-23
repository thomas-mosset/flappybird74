import pygame

from constants import *

# Bird's creation
def create_pixel_bird():
    """Create the bird image with pixels"""

    # Creates a surface for the bird
    # pygame.SRCALPHA allows to use transparency
    bird_surface = pygame.Surface((12 * PIXEL_SIZE, 12 * PIXEL_SIZE), pygame.SRCALPHA)
    pixels = [
        (5, 1, BROWN), (6, 1, BROWN),
        (4, 2, BROWN), (5, 2, YELLOW), (6, 2, YELLOW), (7, 2, BROWN),
        (3, 3, BROWN), (4, 3, YELLOW), (5, 3, YELLOW), (6, 3, YELLOW), (7, 3, BROWN), (8, 3, DARK_BROWN),
        (3, 4, YELLOW), (4, 4, YELLOW), (5, 4, YELLOW), (6, 4, YELLOW), (7, 4, DARK_BROWN),
        (2, 5, YELLOW), (3, 5, YELLOW), (4, 5, ORANGE), (5, 5, YELLOW), (6, 5, DARK_GRAY), (7, 5, DARK_BROWN),
        (3, 6, ORANGE), (4, 6, ORANGE), (5, 6, DARK_BROWN), (6, 6, DARK_BROWN),
        (4, 7, DARK_BROWN), (5, 7, DARK_BROWN)
    ]
    
    
    # Filling the surface with the bird's pixels
    for x, y, color in pixels:
        pygame.draw.rect(bird_surface, color, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
    
    return bird_surface

# Bird Initialisation
bird_img = create_pixel_bird()

# Bird rect
bird = pygame.Rect(100, 200, 48, 48)