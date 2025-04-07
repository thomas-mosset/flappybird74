# import pygame
import pygame
import random
import time

# initialization of pygame
pygame.init()

# musics
pygame.mixer.music.load("assets/musics/POL-magical-sun-short.wav")
pygame.mixer.music.set_volume(0.5) # volume goes from 0.0 to 1.0
pygame.mixer.music.play(-1) # -1 = infinite loop

# sounds
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")
game_over_sound.set_volume(0.5)

# initialization of the timer (in milliseconds)
start_time = pygame.time.get_ticks()

# game's images / icons
timer_img = pygame.image.load("icon/timer.png")
timer_img = pygame.transform.scale(timer_img, (30, 30))  # Resize it

trophy_img = pygame.image.load("icon/trophy.png")
trophy_img = pygame.transform.scale(trophy_img, (30, 30))


# game's constants
WIDTH = 1280
HEIGHT = 720
PIXEL_SIZE = 4 # size an enlarged pixel
TREE_WIDTH = 80
TREE_MIN_HEIGHT = 200
TREE_MAX_HEIGHT = 620
TREE_GAP = 235
TREE_SPEED = 2
GRAVITY = 1 # makes the bird fall down
JUMP_STRENGTH = -12 # bird's jump strenght
BIRD_VERTICAL_SPEED = 0
BUBBLE_SPAWN_TIME = 180 # a bubble every 3 sec (60 FPS * 3)
BUBBLE_SPEED = 2 # speed of moving bubbles

# game's variables
clock = pygame.time.Clock()
running = True

bubbles = []
bubble_timer = 0 # to calculate the spawn time of a bubble
score = 0
game_started = False  # New variable for countdown
game_paused = False

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
BUBBLE_COLOR = (248, 191, 23)

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


class Bubble:
    # create a unique bubble with a random posiiotn and a random value
    def __init__(self):
        self.x = WIDTH + random.randint(50, 200)  # Spawn off-screen
        self.y = random.randint(100, HEIGHT - 200)
        self.radius = 25 # initial size of the bubble
        self.value = random.randint(1, 5) # random points value between 1 and 5
        self.active = True # to deal with its deleting
        self.alpha = 255  # Fully opaque

    def move(self):
        # move the bubble from the right to the left
        self.x -= BUBBLE_SPEED
        if self.x < -self.radius: # Remove the bubble if it goes off-screen
            self.active = False
    
    def draw(self, screen):
        # display the bubble on screen
        if self.active:
            bubble_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(bubble_surface, (BUBBLE_COLOR[0], BUBBLE_COLOR[1], BUBBLE_COLOR[2], self.alpha),(self.radius, self.radius), self.radius)
            screen.blit(bubble_surface, (self.x - self.radius, self.y - self.radius))
            font = pygame.font.Font(None, 30)
            text = font.render(str(self.value), True, (BLACK))
            text.set_alpha(self.alpha)  # Apply transparency to text
            screen.blit(text, (self.x -5, self.y - 9)) # center the text withing the bubble

    def shrink(self):
        """Fade-out effect before disappearing."""
        if self.alpha > 0:
            self.alpha -= 15  # Reduce transparency
            self.radius -= 1
        else:
            self.active = False  # Remove when fully transparent

# check if the bird touches a bubble
def check_bubble_collision():
    global score
    for bubble in bubbles:
        if bubble.active:
            distance = ((bird.x - bubble.x) ** 2 + (bird.y - bubble.y) ** 2) ** 0.5
            # collision detected
            if distance < bubble.radius + 20: 
                score += bubble.value
                bubble.value = 0  # Remove points from the bubble
                bubble.shrink()  # Start fading effect


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

def point_in_triangle(px, py, ax, ay, bx, by, cx, cy):
    detT = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
    alpha = ((by - cy) * (px - cx) + (cx - bx) * (py - cy)) / detT
    beta = ((cy - ay) * (px - cx) + (ax - cx) * (py - cy)) / detT
    gamma = 1 - alpha - beta
    return (0 <= alpha <= 1) and (0 <= beta <= 1) and (0 <= gamma <= 1)


def countdown():
    global game_started
    font = pygame.font.Font(None, 100)
    
    for i in range(3, 0, -1):
        screen.fill(SKY_BLUE)
        text = font.render(str(i), True, BLACK)
        screen.blit(text, (WIDTH // 2 - 30, HEIGHT // 2 - 50))
        pygame.display.flip()
        time.sleep(1) # wait 1 sec between each number display
    
    # Display "GO!"
    screen.fill(SKY_BLUE)
    text = font.render("GO!", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
    pygame.display.flip()
    time.sleep(1) # wait 1 sec before displaying "GO!"

    game_started = True  # Start the game after countdown

# Start countdown before entering main loop
countdown()

# main loop
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

    # events management
    for event in pygame.event.get():
        # pygame .QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        # if a key from the keyboard is pressed
        if event.type == pygame.KEYDOWN:

            # if the key is equal to the space key or the up key
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # the bird jumps
                BIRD_VERTICAL_SPEED = JUMP_STRENGTH

            # if ESC key is pressed then we pause the game
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused
                
                # music on pause
                if game_paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()


        # if bird is out of the bottom of the screen, reload the game (player has lost)
        if bird.y + bird.height >= HEIGHT:
            running = False # stop the game



    if not game_paused:
        # gravity is applied to the bird
        BIRD_VERTICAL_SPEED += GRAVITY
        # update the bird's position
        bird.y += BIRD_VERTICAL_SPEED

        # Limit the bird's position...
        # ... to the bottom
        if bird.y < 0:
            bird.y = 0
            BIRD_VERTICAL_SPEED = 0
        
        # ... to the top
        if bird.y > HEIGHT - 50 - bird.height:
            bird.y > HEIGHT - 50 - bird.height
            BIRD_VERTICAL_SPEED = 0


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
            
            # definition of rectangles collision for the trees
            trunk_rect_collision = pygame.Rect(trees[i][0] + TREE_WIDTH//3, trees[i][1] - 40, TREE_WIDTH//3, 40)

            # check if collision between the bird and the tree's trunk
            if bird.colliderect(trunk_rect_collision) :
                running = False # stop the game


            # Collision detection with leaves
            ax, ay = trees[i][0], trees[i][1] - 40
            bx, by = trees[i][0] + TREE_WIDTH//2, trees[i][1] - 40 - trees[i][2]
            cx, cy = trees[i][0] + TREE_WIDTH, trees[i][1] - 40

            for corner in [(bird.x, bird.y), (bird.x + bird.width, bird.y),
                        (bird.x, bird.y + bird.height), (bird.x + bird.width, bird.y + bird.height)]:
                if point_in_triangle(corner[0], corner[1], ax, ay, bx, by, cx, cy):
                    running = False  # Collision with leaves



        # bubbles spawn management
        bubble_timer += 1
        if bubble_timer >= BUBBLE_SPAWN_TIME:
            bubbles.append(Bubble()) # create a new bubble
            bubble_timer = 0 # reset the bubble timer

        # check fo collision with bubbles
        check_bubble_collision()

        # Display and update bubbles
        for bubble in bubbles:
            if bubble.active:
                bubble.move()
                bubble.draw(screen)
            else:
                bubbles.remove(bubble) # Remove inactive bubbles


        # Info displayed on screen (timer + score)
        font = pygame.font.Font(None, 36)

        # Timer
        # Calculate timer
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 # Convert milliseconds to seconds

        # Display timer
        timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
        screen.blit(timer_text, (55, 19)) # Position at the top
        screen.blit(timer_img, (20, 15))

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (55, 55)) # Position at the top but slightly lower than the timer
        screen.blit(trophy_img, (20, 50))


        # Bird on screen
        screen.blit(bird_img, (bird.x, bird.y))


       
    # if game is paused / Pause screen
    if game_paused:
        game_paused_font = pygame.font.Font(None, 80)
        game_paused_text = game_paused_font.render("PAUSE", True, (255, 0, 0))
        screen.blit(game_paused_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))


    # refresh the screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)


# Ending screen

pygame.mixer.music.stop() # stop the game's music loop
game_over_sound.play() # play the game over sound

eding_font_big = pygame.font.Font(None, 100)
eding_font_small = pygame.font.Font(None, 50)

screen.fill((0, 0, 0)) # black background
game_over_text = eding_font_big.render("GAME OVER", True, (255, 0, 0))
score_text = eding_font_small.render(f"Score: {score}", True, (255, 255, 255))
time_text = eding_font_small.render(f"Time: {elapsed_time}s", True, (255, 255, 255))

screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
screen.blit(time_text, (WIDTH // 2 - 100, HEIGHT // 2 + 60))

pygame.display.flip()

# Wait 3 secondes before closing
time.sleep(3)

pygame.quit()