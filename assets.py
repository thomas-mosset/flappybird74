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
