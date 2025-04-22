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

