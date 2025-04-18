# import pygame
import pygame
import random
import time

# initialization of pygame
pygame.init()
music_on = True
game_over_played = False

# fonts
font_21 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 21)
font_26 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 26)
font_30 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 30)
font_40 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 40)
font_50 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 50)
font_80 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 80)
font_100 = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 100)

# menus titles
title_main_menu_text = font_50.render("MENU", True, (255, 255, 255))
title_main_menu_rect = title_main_menu_text.get_rect(center=(640, 150))

title_params_menu_text = font_40.render("PARAMS", True, (255, 255, 255))
title_params_menu_rect = title_params_menu_text.get_rect(center=(640, 150))

title_controls_menu_text = font_30.render("CONTROLS", True, (255, 255, 255))
title_controls_menu_rect = title_controls_menu_text.get_rect(center=(640, 150))

title_music_menu_text = font_40.render("MUSIC", True, (255, 255, 255))
title_music_menu_rect = title_music_menu_text.get_rect(center=(640, 150))

title_pause_menu_text = font_40.render("PAUSE", True, (255, 255, 255))
title_pause_menu_rect = title_pause_menu_text.get_rect(center=(640, 150))

title_game_over_menu_text = font_30.render("GAME OVER", True, (255, 255, 255))
title_game_over_menu_rect = title_game_over_menu_text.get_rect(center=(640, 150))

number_version_main_menu_text = font_26.render("v.2", True, (0, 0, 0))
number_version_main_menu_rect = number_version_main_menu_text.get_rect(center=(640, 630))

jump_title_controls_menu_text = font_26.render("Jump", True, (116, 160, 80)) # green
jump_title_controls_menu_rect = jump_title_controls_menu_text.get_rect(center=(640, 290))

jump_keys_controls_menu_text = font_26.render("up & space", True, (0, 0, 0))
jump_keys_controls_menu_rect = jump_keys_controls_menu_text.get_rect(center=(640, 330))

pause_title_controls_menu_text = font_26.render("Pause", True, (116, 160, 80)) # green
pause_title_controls_menu_rect = pause_title_controls_menu_text.get_rect(center=(640, 410))

pause_keys_controls_menu_text = font_26.render("escape", True, (0, 0, 0))
pause_keys_controls_menu_rect = pause_keys_controls_menu_text.get_rect(center=(640, 450))

music_on_text = font_26.render("ON", True, (116, 160, 80) if music_on else (0, 0, 0))
music_on_rect = music_on_text.get_rect(center=(570, 430))

music_off_text = font_26.render("OFF", True, (116, 160, 80) if not music_on else (0, 0, 0))
music_off_rect = music_off_text.get_rect(center=(710, 430))

# screens
countdown_screen = pygame.image.load("assets/screens/countdown_screen.png")
base_menu_screen = pygame.image.load("assets/screens/base_menu_screen.png")
base_game_over_screen = pygame.image.load("assets/screens/base_game_over_screen.png")

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

game_started = False
game_over = False
game_paused = False

# Menus management
main_menu = True
params_menu = False
music_menu = False
controls_menu = False

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
pygame.display.set_caption("Flappy Bird")

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


# reset game's values to initial state (use case : the player has already played once but has come back to the main menu - so their data and the game's state doesn't stay as their previous gameplay.)
def reset_game():
    global bird, BIRD_VERTICAL_SPEED, score, pipes, coins, coin_timer, start_time
    global game_over, game_paused, game_over_played, clouds

    # Reset bird position & speed
    bird.x = 150
    bird.y = HEIGHT // 2
    BIRD_VERTICAL_SPEED = 0

    # Reset score & timer
    score = 0
    start_time = pygame.time.get_ticks() # start the timer again
    coin_timer = 0

    # Reset gameplay elements
    pipes = [Pipe(WIDTH + i * PIPE_DISTANCE) for i in range(3)]
    coins = []

    # Reset clouds
    clouds = [Cloud() for _ in range(4)]

    # Reset game state flags
    game_over = False
    game_paused = False
    game_over_played = False


def start_game():
    global game_started, elapsed_time, last_time_update
    
    reset_game() # Reset the game
    countdown() # Launch the beginning countdown

    # Restart music if the option if activated
    if music_on and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    elapsed_time = 0
    last_time_update = pygame.time.get_ticks()

    game_started = True  # game starts after the countdown


def quit_game():
    global game_started
    global running
    game_started = False
    running = False

def resume_game():
    global game_paused
    game_paused = False

def go_to_params_menu():
    global params_menu, main_menu
    params_menu = True
    main_menu = False

def go_back(current_menu_name, previous_menu_name):
    globals()[current_menu_name] = False
    globals()[previous_menu_name] = True

def go_to_music_menu():
    global params_menu, music_menu
    params_menu = False
    music_menu = True

def go_to_controls_menu():
    global params_menu, controls_menu
    params_menu = False
    controls_menu = True

def go_back_to_main_menu():
    global main_menu, game_started, game_paused
    game_started = False
    main_menu = True
    game_paused = False


# screens / menus assets
## Load btn images
menu_btn = pygame.image.load("assets/screens/screens_elements/menu_button.png").convert_alpha()
menu_params_btn = pygame.image.load("assets/screens/screens_elements/menu_params.png").convert_alpha()
params_menu_headphone_btn = pygame.image.load("assets/screens/screens_elements/params_headphone.png").convert_alpha()
params_menu_gamestick_btn = pygame.image.load("assets/screens/screens_elements/params_gamestick.png").convert_alpha()
music_menu_img = pygame.image.load("assets/screens/screens_elements/params_music_note.png").convert_alpha()

## resize btn images
resized_menu_btn = pygame.transform.scale(menu_btn, (200, 80))
resized_menu_params_btn = pygame.transform.scale(menu_params_btn, (135, 135))
resized_params_menu_headphone_btn = pygame.transform.scale(params_menu_headphone_btn, (125, 125))
resized_params_menu_gamestick_btn = pygame.transform.scale(params_menu_gamestick_btn, (125, 125))
resized_music_menu_img = pygame.transform.scale(music_menu_img, (100, 100))

# Create btns
start_menu_btn = Button(resized_menu_btn, (640, 300), "START", font_26, start_game)
params_menu_btn = Button(resized_menu_params_btn, (640, 425), "", font_26, go_to_params_menu)
quit_menu_btn = Button(resized_menu_btn, (640, 550), "QUIT", font_26, quit_game)
headphone_btn = Button(resized_params_menu_headphone_btn, (640, 300), "", font_26, go_to_music_menu)
gamestick_btn = Button(resized_params_menu_gamestick_btn, (640, 435), "", font_26, go_to_controls_menu)
resume_game_btn = Button(resized_menu_btn, (640, 345), "RESUME", font_21, resume_game)
back_to_menu_btn = Button(resized_menu_btn, (640, 470), "MENU", font_21, go_back_to_main_menu)
play_game_over_btn = Button(resized_menu_btn, (520, 545), "PLAY", font_21, start_game)
back_to_menu_game_over_btn = Button(resized_menu_btn, (760, 545), "MENU", font_21, go_back_to_main_menu)

# it's just an img not a btn so we use get_rect()
resized_music_menu_img_rect = resized_music_menu_img.get_rect(center=(640, 330))

# reusable go back btn 
def create_back_button(current_menu, previous_menu):
    return Button(
        resized_menu_btn,
        (640, 550),
        "BACK",
        font_26,
        lambda: go_back(current_menu, previous_menu)
    )

# Create the clouds
clouds = [Cloud() for _ in range(4)]

# Create the pipes
pipes = [Pipe(WIDTH + i * PIPE_DISTANCE) for i in range(3)] # Create 3 pipes initially, spaced by PIPE_DISTANCE, off screen to the right


# Calculate timer
elapsed_time = 0
last_time_update = None  # we wait the begining of the game to initialize it

# main loop
while running:
    # Timer only runs when game is active (not paused or over)
    if not game_paused and not game_over and game_started:
        current_time = pygame.time.get_ticks()
        delta = (current_time - last_time_update) / 1000.0  # Convert to seconds
        elapsed_time += delta
        last_time_update = current_time
    elif game_started and (game_paused or game_over):
        # if the game is on pause or over, we do not update elapsed_time
        # we stock it for the time where the player will resume the game
        last_time_update = pygame.time.get_ticks()

    if not game_started:
        if main_menu:
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

        elif params_menu:
            # PARAMS MENU
            screen.blit(base_menu_screen, (0, 0))
            screen.blit(title_params_menu_text, title_params_menu_rect) 
            screen.blit(number_version_main_menu_text, number_version_main_menu_rect)

            # create_back_button("current_menu", "previous_menu")
            back_btn = create_back_button("params_menu", "main_menu")

            headphone_btn.draw(screen)
            gamestick_btn.draw(screen)
            back_btn.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    running = False
                headphone_btn.handle_event(event)
                gamestick_btn.handle_event(event)
                back_btn.handle_event(event)

            pygame.display.flip()
            clock.tick(60)
            continue  # we skip the loop as long as the game has not begun

        elif controls_menu:
            # CONTROLS MENU
            screen.blit(base_menu_screen, (0, 0))
            screen.blit(title_controls_menu_text, title_controls_menu_rect)
            screen.blit(jump_title_controls_menu_text, jump_title_controls_menu_rect)
            screen.blit(jump_keys_controls_menu_text, jump_keys_controls_menu_rect)
            screen.blit(pause_title_controls_menu_text, pause_title_controls_menu_rect)
            screen.blit(pause_keys_controls_menu_text, pause_keys_controls_menu_rect)
            screen.blit(number_version_main_menu_text, number_version_main_menu_rect)
            
            # create_back_button("current_menu", "previous_menu")
            back_btn = create_back_button("controls_menu", "params_menu")
            # draw it on screen
            back_btn.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    running = False
                back_btn.handle_event(event)

            pygame.display.flip()
            clock.tick(60)
            continue  # we skip the loop as long as the game has not begun


        elif music_menu:
            music_on_text = font_26.render("ON", True, (116, 160, 80) if music_on else (0, 0, 0))
            music_off_text = font_26.render("OFF", True, (116, 160, 80) if not music_on else (0, 0, 0))

            # MUSIC MENU
            screen.blit(base_menu_screen, (0, 0))
            screen.blit(title_music_menu_text, title_music_menu_rect)
            screen.blit(resized_music_menu_img, resized_music_menu_img_rect)

            screen.blit(music_on_text, music_on_rect)
            screen.blit(music_off_text, music_off_rect)

            screen.blit(number_version_main_menu_text, number_version_main_menu_rect)
            
            # create_back_button("current_menu", "previous_menu")
            back_btn = create_back_button("music_menu", "params_menu")
            # draw it on screen
            back_btn.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN: # check it click event
                    if music_on_rect.collidepoint(event.pos):
                        music_on = True
                        pygame.mixer.music.set_volume(0.5)  # activate music

                        if not pygame.mixer.music.get_busy():  # if the music is not played
                            pygame.mixer.music.play(-1) # we start the music

                    elif music_off_rect.collidepoint(event.pos):
                        music_on = False
                        pygame.mixer.music.set_volume(0.0)  # turn off music
                back_btn.handle_event(event)

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
        headphone_btn.handle_event(event)
        gamestick_btn.handle_event(event)

        # if a key from the keyboard is pressed
        if event.type == pygame.KEYDOWN:
            # if the key is equal to the space key or the up key
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # the bird jumps
                BIRD_VERTICAL_SPEED = JUMP_STRENGTH

            # if ESC key is pressed then we pause the game
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused


    if not game_paused:
        # gravity is applied to the bird
        BIRD_VERTICAL_SPEED += GRAVITY
        # update the bird's position
        bird.y += BIRD_VERTICAL_SPEED

        # Limit the bird's position to the top of the screen (bird can't go above the screen)
        if bird.y < 0:
            bird.y = 0
            BIRD_VERTICAL_SPEED = 0
        
        # If bird is out of the bottom of the screen, player has lost
        if bird.y + bird.height >= HEIGHT:
            bird.y = HEIGHT - bird.height  # so the bird doesn't "go down" the screen
            game_over = True

        # If the last pipe has moved far enough to the left, a new one is created on the right
        if pipes[-1].x < WIDTH - PIPE_DISTANCE:
            pipes.append(Pipe(WIDTH))

        # Only keep the pipes that are still visible on screen
        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        for pipe in pipes:
            # if one of the pipes collide with the bird, we stop the game
            if pipe.collides_with(bird):
                game_over = True


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
        # Display timer

        # Force elapsed_time to be an int
        elapsed_seconds = int(elapsed_time)

        # convert it to minutes and seconds
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60

        # display it
        timer_text = font_26.render(f"Time: {minutes:02}m {seconds:02}s", True, BLACK)
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
        # PAUSE MENU
        screen.blit(base_menu_screen, (0, 0))
        screen.blit(title_pause_menu_text, title_pause_menu_rect) 
        screen.blit(number_version_main_menu_text, number_version_main_menu_rect)

        resume_game_btn.draw(screen)
        resume_game_btn.handle_event(event)

        back_to_menu_btn.draw(screen)
        back_to_menu_btn.handle_event(event)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            resume_game_btn.handle_event(event)
            back_to_menu_btn.handle_event(event)


    if game_over:
        # GAME OVER MENU
        if not game_over_played:
            pygame.mixer.music.stop() # stop the game's music loop
            game_over_sound.play() # play the game over sound
            game_over_played = True

        screen.blit(base_game_over_screen, (0, 0))
        screen.blit(title_game_over_menu_text, title_game_over_menu_rect)
        screen.blit(number_version_main_menu_text, number_version_main_menu_rect)

        score_text = font_26.render(f"Score: {score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(700, 310))
        screen.blit(score_text, score_rect)

        # Force elapsed_time to be an int
        elapsed_seconds = int(elapsed_time)

        # convert it to minutes and seconds
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60

        # display it
        timer_text = font_26.render(f"Time: {minutes:02}m{seconds:02}s", True, BLACK)
        timer_rect = timer_text.get_rect(center=(700, 440))
        screen.blit(timer_text, timer_rect)

        play_game_over_btn.draw(screen)
        play_game_over_btn.handle_event(event)

        back_to_menu_game_over_btn.draw(screen)
        back_to_menu_game_over_btn.handle_event(event)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            play_game_over_btn.handle_event(event)
            back_to_menu_game_over_btn.handle_event(event)


    # refresh the screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)