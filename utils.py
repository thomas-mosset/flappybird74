import pygame

from constants import *
from assets import load_images

images = load_images()

def draw_mountains(screen):
    """Display the mountain image for the game background."""

    screen.blit(images["background_elements"]["mountain_img"], (0, HEIGHT - images["background_elements"]["mountain_img"].get_height()))


def draw_grass(screen):
    """Display the grass image for the game background."""

    screen.blit(images["background_elements"]["grass_img"], (0, HEIGHT - images["background_elements"]["grass_img"].get_height()))