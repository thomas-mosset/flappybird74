# import pygame
import pygame
import random

# initialization of pygame
pygame.init()

# game's constants
WIDTH = 1280
HEIGHT = 720
PIXEL_SIZE = 4 # size an enlarged pixel
TREE_WIDTH = 80
TREE_MIN_HEIGHT = 200
TREE_MAX_HEIGHT = 620
TREE_GAP = 235
TREE_SPEED = 2

# game's variables
clock = pygame.time.Clock()
running = True

# game's colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (100, 50, 0)
ORANGE = (255, 165, 0)
DARK_GRAY = (50, 50, 50)
GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 200, 200)
SKY_BLUE = (135, 206, 235)
GREEN_GRASS = (88, 158, 41)
DARK_GREEN = (51, 92, 36)

# screen creation
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird 74")

# Bird's creation
def create_pixel_bird():
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
    
    for x, y, color in pixels:
        pygame.draw.rect(bird_surface, color, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
    
    return bird_surface

bird_img = create_pixel_bird()
bird = pygame.Rect(100, 200, 48, 48)

def draw_mountains():
    # draw.polygon allows to draw triangles
    pygame.draw.polygon(screen, DARK_GRAY, [(50, 500), (200, 300), (350, 500)])  # Big mountain
    pygame.draw.polygon(screen, LIGHT_GRAY, [(170, 335), (200, 300), (230, 335)])  # Snow on big mountain
    pygame.draw.polygon(screen, GRAY, [(200, 520), (300, 400), (400, 520)])  # Small mountain
    pygame.draw.polygon(screen, LIGHT_GRAY, [(280, 420), (300, 400), (320, 420)])  # Snow on small mountain

def draw_cloud(x, y):
    cloud_pixels = [
        (3, 0), (4, 0), (5, 0), (6, 0),
        (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),
        (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3),
        (3, 4), (4, 4), (5, 4), (6, 4),
    ]

    for px, py in cloud_pixels:
        pygame.draw.rect(screen, WHITE, ((x + px * (PIXEL_SIZE * 2.5), y + py * (PIXEL_SIZE * 2.5), (PIXEL_SIZE * 2.5), (PIXEL_SIZE * 2.5))))


def draw_grass():
    pygame.draw.rect(screen, GREEN_GRASS, (0, HEIGHT - 230, WIDTH, 500))


def draw_tree(x, base_y, height):
    trunk_height = 40 # trunk's height is fixed
    leafs_height = height # tree's leafs' height is random (determined between TREE_MIN_HEIGHT and TREE_MAX_HEIGHT)

    # tree trunk
    # x + TREE_WIDTH//3 -> horizontal centered position
    # base_y - trunk_height -> vertical position, in grass
    # TREE_WIDTH//3 -> trunk width
    pygame.draw.rect(screen, BROWN, (x + TREE_WIDTH//3, base_y - trunk_height, TREE_WIDTH//3, trunk_height))

    # tree leafs
    pygame.draw.polygon(screen, DARK_GREEN, [
        (x, base_y - trunk_height), # Lower left corner
        (x + TREE_WIDTH//2, base_y - trunk_height - leafs_height), # top lof the triangle
        (x + TREE_WIDTH, base_y - trunk_height) # Lower right corner
    ])  

# WIDTH + i * TREE_GAP -> trees are placed outside the screen and appears progressively
# HEIGHT -> they're placed on the grass
# random.randint(TREE_MIN_HEIGHT, TREE_MAX_HEIGHT) -> height of leafs is random 
trees = [(WIDTH + i * TREE_GAP, HEIGHT, random.randint(TREE_MIN_HEIGHT, TREE_MAX_HEIGHT)) for i in range(6)]


while running:
    # fill the screen with a color
    screen.fill(SKY_BLUE) # blue sky
    draw_grass() # grass / ground
    draw_mountains() # mountains
    # different clouds -> draw_cloud(X axis, Y axis)
    draw_cloud(20, 80)
    draw_cloud(360, 200)
    draw_cloud(500, 100)
    draw_cloud(200, 180)
    draw_cloud(630, 380)
    draw_cloud(850, 320)
    draw_cloud(950, 105)

    # trees on screen (display + movement)
    for i in range(len(trees)):
        # move trees to left
        # the tree's X (horizontal) position decreases every TREE_SPEED pixels per image
        trees[i] = (trees[i][0] - TREE_SPEED, trees[i][1], trees[i][2])

        # Every tree is re-drawn at its new position
        draw_tree(trees[i][0], trees[i][1], trees[i][2])

        # if the tree is totally out of the screen on the left, it's then repositionned à the right (WIDTH)
        # and its height is randomly reset
        if trees[i][0] < -TREE_WIDTH:
            trees[i] = (WIDTH, HEIGHT - 30, random.randint(TREE_MIN_HEIGHT, TREE_MAX_HEIGHT))

    # Bird on screen
    screen.blit(bird_img, (bird.x, bird.y))

    # events management
    for event in pygame.event.get():
        # pygame .QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    # refresh the screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)

pygame.quit()