# import pygame
import pygame
import random
import time

# initialization of pygame
pygame.init()

# fonts
font_26 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 26)
font_50 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 50)
font_80 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 80)
font_100 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 100)

# menus titles
title_main_menu_text = font_50.render("MENU", True, (255, 255, 255))
title_main_menu_rect = title_main_menu_text.get_rect(center=(640, 150))

number_version_main_menu_text = font_26.render("v.2", True, (0, 0, 0))
number_version_main_menu_rect = number_version_main_menu_text.get_rect(center=(640, 630))

# screens
countdown_screen = pygame.image.load("assets/screens/countdown_screen.png")
base_menu_screen = pygame.image.load("assets/screens/base_menu_screen.png")

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
GRAVITY = 1 # makes the bird fall down
JUMP_STRENGTH = -12 # bird's jump strenght
BIRD_VERTICAL_SPEED = 0
COIN_SPAWN_TIME = 180 # a coin every 3 sec (60 FPS * 3)
COIN_SPEED = 2 # speed of moving coins
PIPE_HEIGHT = 720
PIPE_SPEED = 2
PIPE_DISTANCE = 300

# game's variables
clock = pygame.time.Clock()
running = True

coins = []
coin_timer = 0 # to calculate the spawn time of a coin
score = 0

game_started =False
game_over = False
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

# game's images / icons
timer_img = pygame.image.load("assets/icons/timer.bmp")
timer_img = pygame.transform.scale(timer_img, (30, 30))  # Resize it

trophy_img = pygame.image.load("assets/icons/trophy.bmp")
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

xs_pipe_img = pygame.image.load("assets/pipes/xs_pipe.bmp")
s_pipe_img = pygame.image.load("assets/pipes/s_pipe.bmp")
m_pipe_img = pygame.image.load("assets/pipes/m_pipe.bmp")
l_pipe_img = pygame.image.load("assets/pipes/l_pipe.bmp")
xl_pipe_img = pygame.image.load("assets/pipes/xl_pipe.bmp")

# dictionary to group pipes img
pipe_images = {
    "xs": xs_pipe_img,
    "s": s_pipe_img,
    "m": m_pipe_img,
    "l": l_pipe_img,
    "xl": xl_pipe_img
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


# Active pipes list
pipes = []


class Button:
    def __init__(self, image, pos, text, font, callback):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.text_surf = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.callback = callback

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surf, self.text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# Pipe's collision
class Pipe:
    def __init__(self, x):
        self.size = random.choice(list(pipe_images.keys())) # get a random size trough the dictionary's keys
        self.image = pipe_images[self.size] # get the image corresponding to the key
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x # initial position on the X axis on the pipe's creation
        self.y = HEIGHT - self.height # position the image on the bottom of the screen
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) # rectangle collision
        self.mask = pygame.mask.from_surface(self.image)  # creation of the pixel-perfect collision mask that respects transparency. This gives an accurate collision with the actual shape of the pipe (not just its rectangle).

    def move(self):
        self.x -= PIPE_SPEED # move the pipe from right to left
        self.rect.x = self.x # update the pipe collision position

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y)) # display on screen the pipe at its current position

    def collides_with(self, bird_rect):
        offset = (int(bird_rect.x - self.x), int(bird_rect.y - self.y)) # relative position between the pipe and the bird
        bird_mask = pygame.mask.from_surface(bird_img)
        return self.mask.overlap(bird_mask, offset) is not None # mask.overlap -> checks if there is an overlap between the bird and pipe masks


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


def countdown():
    global game_started

    for i in range(3, 0, -1):
        screen.blit(countdown_screen, (0, 0))
        text = font_100.render(str(i), True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(1) # wait 1 sec between each number display
    
    # Display "GO!"
    screen.blit(countdown_screen, (0, 0))
    text = font_100.render("GO!", True, BLACK)
    go_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, go_rect)
    pygame.display.flip()
    time.sleep(1) # wait 1 sec before displaying "GO!"

    screen.fill(SKY_BLUE)
    game_started = True  # Start the game after countdown


def start_game():
    countdown() # Launch the beginning countdown
    global game_started
    game_started = True  # game starts after the countdown


def quit_game():
    global game_started
    global running
    game_started = False
    running = False

def go_to_params_menu():
    print("def go_to_params_menu")

# screens assets
## Load btn images
menu_btn = pygame.image.load("assets/screens/screens_elements/menu_button.png").convert_alpha()
menu_params_btn = pygame.image.load("assets/screens/screens_elements/menu_params.png").convert_alpha()

## resize btn images
resized_menu_btn = pygame.transform.scale(menu_btn, (200, 80))
resized_menu_params_bt = pygame.transform.scale(menu_params_btn, (135, 135))

# Create btns
start_menu_btn = Button(resized_menu_btn, (640, 300), "START", font_26, start_game)
params_menu_btn = Button(resized_menu_params_bt, (640, 425), "", font_26, go_to_params_menu)
quit_menu_btn = Button(resized_menu_btn, (640, 550), "QUIT", font_26, quit_game)

# Create the clouds
clouds = [Cloud() for _ in range(4)]

# Create the pipes
pipes = [Pipe(WIDTH + i * PIPE_DISTANCE) for i in range(3)] # Create 3 pipes initially, spaced by PIPE_DISTANCE, off screen to the right

# main loop
while running:

    if not game_started:
        # MAIN MENU
        screen.blit(base_menu_screen, (0, 0))
        screen.blit(title_main_menu_text, title_main_menu_rect) 
        screen.blit(number_version_main_menu_text, number_version_main_menu_rect)

        start_menu_btn.draw(screen)
        params_menu_btn.draw(screen)
        quit_menu_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                running = False
            start_menu_btn.handle_event(event)
            params_menu_btn.handle_event(event)
            quit_menu_btn.handle_event(event)

        pygame.display.flip()
        clock.tick(60)
        continue  # we skip the loop as long as the game has not begun

    # fill the screen with a color
    screen.fill(SKY_BLUE) # blue sky
    draw_mountains()
    draw_grass()



    for cloud in clouds:
        cloud.move()
        cloud.draw(screen)

    for pipe in pipes:
        pipe.move()
        pipe.draw(screen)

    # events management
    for event in pygame.event.get():
        # pygame .QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False
        
        # menus management
        start_menu_btn.handle_event(event)
        params_menu_btn.handle_event(event)
        quit_menu_btn.handle_event(event)

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
            game_over = True
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


        # If the last pipe has moved far enough to the left, a new one is created on the right
        if pipes[-1].x < WIDTH - PIPE_DISTANCE:
            pipes.append(Pipe(WIDTH))

        # Only keep the pipes that are still visible on screen
        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        for pipe in pipes:
            # if one of the pipes collide with the bird, we stop the game
            if pipe.collides_with(bird):
                game_over = True
                running = False


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
        screen.blit(timer_text, (60, 19)) # Position at the top
        screen.blit(timer_img, (20, 15))

        # Display score
        score_text = font_26.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (65, 55)) # Position at the top but slightly lower than the timer
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