import pygame
import random

from constants import *
from assets import load_images
from bird import bird_img

images = load_images()

# ======================
# Class Button
# ======================
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


# ======================
# Class Pipe
# ======================
class Pipe:
    def __init__(self, x):
        self.size = random.choice(list(images["pipes"].keys())) # get a random size trough the dictionary's keys
        self.image = images["pipes"][self.size] # get the image corresponding to the key
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

# ======================
# Class Coin
# ======================
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
            1: images["coins"][1],
            2: images["coins"][2],
            3: images["coins"][3],
            4: images["coins"][4],
            5: images["coins"][5]
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

    def animate_flip(self, screen):
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


# ======================
# Class Cloud
# ======================
class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 400) # cloud starts outisde the right screen, at a random position
        self.y = random.randint(5, 80) # cloud is random height level
        self.speed = random.uniform(0.5, 1.5) # each cloud will have a random speed
        self.scale = random.uniform(0.2, 0.9) # each cloud will have a different size
        self.image = pygame.transform.scale(images["background_elements"]["cloud_img"], ( # resize the cloud while keeping its scale
            int(images["background_elements"]["cloud_img"].get_width() * self.scale),
            int(images["background_elements"]["cloud_img"].get_height() * self.scale)
        ))
    
    def move(self):
        self.x -= self.speed # diminish the x cloud's position based on its speed, so it's moving to the left
        if self.x < -self.image.get_width(): # if it's completely outside the left screen...
            self.x = WIDTH + random.randint(100, 500) # ... we put it back outside the right screen
            self.y = random.randint(5, 80) # ... and we give it a new random height
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))