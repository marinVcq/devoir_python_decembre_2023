import pygame
from sys import exit 
import math
from settings import *

pygame.init()

# Creating the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exorsit: Shell Unleashed")
clock = pygame.time.Clock()

# Load images
background = pygame.transform.scale(pygame.image.load("background/background.png").convert(), (SCREEN_WIDTH,SCREEN_HEIGHT))


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = pygame.math.Vector2(PLAYER_START_X,PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("player/0.png").convert_alpha(),0,PLAYER_SCALE)
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.position)
        self.player_rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED

    def player_rotation(self):
        self.mouse_coordinates = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coordinates[0] - self.hitbox_rect.centerx)
        self.y_change_mouse_player =  (self.mouse_coordinates[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle )
        self.player_rect = self.image.get_rect(center = self.hitbox_rect.center) # up^date player rect center


    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_q]:
            self.velocity_x = -self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed

        if self.velocity_x != 0 and self.velocity_y !=0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)


    def move(self):
        self.position += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.position
        self.player_rect.center = self.hitbox_rect.center
    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()

# Create the player instance
player = Player()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # display to the screen 
    screen.blit(background, (0,0))
    screen.blit(player.image, player.player_rect)
    pygame.draw.rect(screen,"red", player.hitbox_rect, width = 2)
    pygame.draw.rect(screen,"green", player.player_rect, width = 2)

    # Update the screen
    player.update()
    pygame.display.update()
    clock.tick(FPS)
