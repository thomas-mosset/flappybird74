# import pygame
import pygame
import random
import time
import math

# initialization of pygame
pygame.init()

# fonts
font_26 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 26)
font_50 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 50)
font_80 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 80)
font_100 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 100)

# musics
pygame.mixer.music.load("assets/musics/POL-magical-sun-short.wav")
pygame.mixer.music.set_volume(0.5) # volume goes from 0.0 to 1.0
pygame.mixer.music.play(-1) # -1 = infinite loop

# sounds
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")
game_over_sound.set_volume(0.5)

coin_touched_sound = pygame.mixer.Sound("assets/sounds/coin_touched.mp3")
coin_touched_sound.set_volume(0.2)

# initialization of the timer (in milliseconds)
start_time = pygame.time.get_ticks()

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
COIN_SPAWN_TIME = 180 # a coin every 3 sec (60 FPS * 3)
COIN_SPEED = 2 # speed of moving coins

# game's variables
clock = pygame.time.Clock()
running = True

coins = []
coin_timer = 0 # to calculate the spawn time of a coin
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
coin_COLOR = (248, 191, 23)

# game's images / icons
timer_img = pygame.image.load("assets/icons/timer.png")
timer_img = pygame.transform.scale(timer_img, (30, 30))  # Resize it

trophy_img = pygame.image.load("assets/icons/trophy.png")
trophy_img = pygame.transform.scale(trophy_img, (30, 30))

grass_img = pygame.image.load("assets/background_elements/grass.bmp")
mountain_img = pygame.image.load("assets/background_elements/mountain.bmp")
cloud_img = pygame.image.load("assets/background_elements/cloud.bmp")

blue_coin_1_img = pygame.image.load("assets/icons/1-coin-blue.bmp")
yellow_coin_2_img = pygame.image.load("assets/icons/2-coin-yellow.bmp")
orange_coin_3_img = pygame.image.load("assets/icons/3-coin-orange.bmp")
pink_coin_4_img = pygame.image.load("assets/icons/4-coin-pink.bmp")
star_coin_5_img = pygame.image.load("assets/icons/5-coin-star.bmp")


# dictionary to group coin img
coin_images = {
    1: blue_coin_1_img,
    2: yellow_coin_2_img,
    3: orange_coin_3_img,
    4: pink_coin_4_img,
    5: star_coin_5_img
}

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


class Coin:
    # create a unique coin with a random posiiotn and a random value
    def __init__(self):
        self.x = WIDTH + random.randint(50, 200)  # Spawn off-screen
        self.y = random.randint(100, HEIGHT - 200)
        self.radius = 25 # initial size of the coin
        self.value = random.randint(1, 5) # random points value between 1 and 5
        self.active = True # to deal with its deleting
        self.touched = False
        self.scored = False

        # for the animation
        self.number_of_flips = 3
        self.flip_progress = 0  # from 0 to 1
        self.flip_speed = 0.2  # adjust for faster or slower flip
        
        # assign values to icons
        self.image = {
            1: blue_coin_1_img,
            2: yellow_coin_2_img,
            3: orange_coin_3_img,
            4: pink_coin_4_img,
            5: star_coin_5_img
        }[self.value]

        # Resize the coin
        self.image = pygame.transform.scale(self.image, (40, 40))

    def move(self):
        # move the coin from the right to the left
        self.x -= COIN_SPEED
        if self.x < -self.radius: # Remove the coin if it goes off-screen
            self.active = False
    
    def draw(self, screen):
        # display the coin on screen
        if self.active:
            image_copy = self.image.copy()
            screen.blit(image_copy, (self.x, self.y))

    def animate_flip(self):
        if not self.touched:
            return

        self.flip_progress += self.flip_speed

        if self.flip_progress >= self.number_of_flips:
            self.flip_progress = self.number_of_flips  # limit to its maximum
            if self.active:
                self.active = False  # end of animation

        # simulate the 3D flip
        angle = self.flip_progress * 360  / self.number_of_flips # 360° rotation

        # Apply rotation
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.radius, self.y + self.radius))

        # Show coin with its rotation
        screen.blit(rotated_image, rotated_rect.topleft)


class Cloud:
    def __init__(self):
        self.image = cloud_img
        self.x = WIDTH + random.randint(0, 400) # cloud starts outisde the right screen, at a random position
        self.y = random.randint(5, 80) # cloud is random height level
        self.speed = random.uniform(0.5, 1.5) # each cloud will have a random speed
        self.scale = random.uniform(0.2, 0.9) # each cloud will have a different size
        self.image = pygame.transform.scale(cloud_img, ( # resize the cloud while keeping its scale
            int(cloud_img.get_width() * self.scale),
            int(cloud_img.get_height() * self.scale)
        ))
    
    def move(self):
        self.x -= self.speed # diminish the x cloud's position based on its speed, so it's moving to the left
        if self.x < -self.image.get_width(): # if it's completely outside the left screen...
            self.x = WIDTH + random.randint(100, 500) # ... we put it back outside the right screen
            self.y = random.randint(5, 80) # ... and we give it a new random height
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# check if the bird touches a coin
def check_coin_collision():
    global score
    for coin in coins:
        if coin.active:
            distance = ((bird.x - coin.x) ** 2 + (bird.y - coin.y) ** 2) ** 0.5
            # collision detected
            if distance < coin.radius + 20 and not coin.touched:
                coin.touched = True
                coin.scored = True
                score += coin.value
                coin_touched_sound.play()


def draw_mountains():
    screen.blit(mountain_img, (0, HEIGHT - mountain_img.get_height()))


def draw_grass():
    screen.blit(grass_img, (0, HEIGHT - grass_img.get_height()))


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

    for i in range(3, 0, -1):
        screen.fill(SKY_BLUE)
        text = font_100.render(str(i), True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(1) # wait 1 sec between each number display
    
    # Display "GO!"
    screen.fill(SKY_BLUE)
    text = font_100.render("GO!", True, BLACK)
    go_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, go_rect)
    pygame.display.flip()
    time.sleep(1) # wait 1 sec before displaying "GO!"

    game_started = True  # Start the game after countdown

# Start countdown before entering main loop
countdown()

# Create the clouds
clouds = [Cloud() for _ in range(4)]

# main loop
while running:
    # fill the screen with a color
    screen.fill(SKY_BLUE) # blue sky
    draw_mountains()
    draw_grass()

    for cloud in clouds:
        cloud.move()
        cloud.draw(screen)

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



        # coins spawn management
        coin_timer += 1
        if coin_timer >= COIN_SPAWN_TIME:
            new_coin = Coin()  # Create a new coin

            # Check if the new coin spawns too close to any existing coin
            if not any(abs(new_coin.x - coin.x) < 40 and abs(new_coin.y - coin.y) < 40 for coin in coins):
                coins.append(new_coin)  # Only add the coin if it's far enough from existing coins

            coin_timer = 0  # Reset the coin timer

        # check fo collision with coins
        check_coin_collision()

        # Display and update coins
        for coin in coins:
            if coin.active:
                coin.move()
                if coin.touched:
                    coin.animate_flip()
                else:
                    coin.draw(screen)
            else:
                coins.remove(coin) # Remove inactive coins

        # Timer
        # Calculate timer
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 # Convert milliseconds to seconds

        # Display timer
        timer_text = font_26.render(f"Time: {elapsed_time}s", True, BLACK)
        screen.blit(timer_text, (55, 19)) # Position at the top
        screen.blit(timer_img, (20, 15))

        # Display score
        score_text = font_26.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (55, 55)) # Position at the top but slightly lower than the timer
        screen.blit(trophy_img, (20, 50))


        # Bird on screen
        screen.blit(bird_img, (bird.x, bird.y))


       
    # if game is paused / Pause screen
    if game_paused:
        game_paused_text = font_80.render("PAUSE", True, (255, 0, 0))
        pause_rect = game_paused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_paused_text, pause_rect)


    # refresh the screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)


# Ending screen
pygame.mixer.music.stop() # stop the game's music loop
game_over_sound.play() # play the game over sound

screen.fill((0, 0, 0)) # black background

# .get_rect() allows to get a rectangle around the text
#  then we just have to center it 

game_over_text = font_100.render("GAME OVER", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
screen.blit(game_over_text, game_over_rect)

score_text = font_50.render(f"Score: {score}", True, (255, 255, 255))
score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(score_text, score_rect)

time_text = font_50.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
screen.blit(time_text, time_rect)


pygame.display.flip()

# Wait 3 secondes before closing
time.sleep(3)

pygame.quit()