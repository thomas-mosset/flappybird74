import pygame
import os

# Always start from the flappy.py script folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_buttons():
    """Loads and resizes all buttons needed by the game."""
    assets = {}
    base_path = os.path.join(BASE_DIR, "assets", "screens", "screens_elements")

    # Buttons
    assets["menu_btn"] = pygame.image.load(os.path.join(base_path, "menu_button.png")).convert_alpha()
    
    assets["menu_params_btn"] = pygame.image.load(os.path.join(base_path, "menu_params.png")).convert_alpha()

    assets["params_menu_headphone_btn"] = pygame.image.load(os.path.join(base_path, "params_headphone.png")).convert_alpha()
    
    assets["params_menu_gamestick_btn"] = pygame.image.load(os.path.join(base_path, "params_gamestick.png")).convert_alpha()

    assets["music_menu_img"] = pygame.image.load(os.path.join(base_path,"params_music_note.png")).convert_alpha()

    # Resize Buttons
    assets["resized_menu_btn"] = pygame.transform.scale(assets["menu_btn"], (200, 80))
    assets["resized_menu_params_btn"] = pygame.transform.scale(assets["menu_params_btn"], (135, 135))
    assets["resized_params_menu_headphone_btn"] = pygame.transform.scale(assets["params_menu_headphone_btn"], (125, 125))
    assets["resized_params_menu_gamestick_btn"] = pygame.transform.scale(assets["params_menu_gamestick_btn"], (125, 125))
    assets["resized_music_menu_img"] = pygame.transform.scale(assets["music_menu_img"], (100, 100))

    return assets


def load_sounds_and_music():
    """Loads all sounds needed by the game."""
    sounds_and_music = {}

    # musics
    pygame.mixer.music.load("assets/musics/POL-magical-sun-short.wav")
    pygame.mixer.music.set_volume(0.5) # volume goes from 0.0 to 1.0
    pygame.mixer.music.play(-1) # -1 = infinite loop

    # sounds
    sounds_and_music["game_over_sound"] = pygame.mixer.Sound("assets/sounds/game_over.mp3")

    sounds_and_music["coin_touched_sound"] = pygame.mixer.Sound("assets/sounds/coin_touched.mp3")

    # define sounds volume
    sounds_and_music["game_over_sound"].set_volume(0.5)
    sounds_and_music["coin_touched_sound"].set_volume(0.2)

    return sounds_and_music



def load_fonts():
    """Loads all fonts needed by the game."""
    fonts = {}

    fonts["font_21"] = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 21)
    fonts["font_26"] = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 26)
    fonts["font_30"] = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 30)
    fonts["font_40"] = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 40)
    fonts["font_50"] = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 50)
    fonts["font_80"] = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 80)
    fonts["font_100"] = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 100)

    return fonts


def load_images():
    """Loads all images needed by the game."""

    # Load icons
    timer_img = pygame.image.load("assets/icons/timer.bmp")
    timer_img = pygame.transform.scale(timer_img, (30, 30))  # Resize it

    trophy_img = pygame.image.load("assets/icons/trophy.bmp")
    trophy_img = pygame.transform.scale(trophy_img, (30, 30))

    # Load coins
    coin_images = {
        1: pygame.image.load("assets/icons/1-coin-blue.bmp"),
        2: pygame.image.load("assets/icons/2-coin-yellow.bmp"),
        3: pygame.image.load("assets/icons/3-coin-orange.bmp"),
        4: pygame.image.load("assets/icons/4-coin-pink.bmp"),
        5: pygame.image.load("assets/icons/5-coin-star.bmp")
    }

    # Load pipes
    pipe_images = {
        "xs": pygame.image.load("assets/pipes/xs_pipe.bmp"),
        "s": pygame.image.load("assets/pipes/s_pipe.bmp"),
        "m": pygame.image.load("assets/pipes/m_pipe.bmp"),
        "l": pygame.image.load("assets/pipes/l_pipe.bmp"),
        "xl": pygame.image.load("assets/pipes/xl_pipe.bmp")
    }

    # Load background elements
    background_elements = {
        "grass_img": pygame.image.load("assets/background_elements/grass.bmp"),
        "mountain_img": pygame.image.load("assets/background_elements/mountain.bmp"),
        "cloud_img": pygame.image.load("assets/background_elements/cloud.bmp"),
    }

    # Load screens
    screens = {
        "countdown_screen": pygame.image.load("assets/screens/countdown_screen.png"),
        "base_menu_screen": pygame.image.load("assets/screens/base_menu_screen.png"),
        "base_game_over_screen": pygame.image.load("assets/screens/base_game_over_screen.png"),
    }

    return {
        "icons": {
            "timer_img": timer_img,
            "trophy_img": trophy_img
        },
        "coins": coin_images,
        "pipes": pipe_images,
        "background_elements": background_elements,
        "screens": screens
    }

