import pygame, asyncio, os
from sys import exit 
import math

class GameState:
    RULES_SCREEN = 0
    CHARACTER_SELECTION = 1
    PLAYING = 2
    GAME_OVER = 3

current_game_state = GameState.CHARACTER_SELECTION

async def start_screen():
    start_font = pygame.font.Font("kongtext.ttf", 20)
    welcome_text = "Bienvenue Aventurier, Dans ce jeu tu dois parcourir les 5 mondes (feu, eau, desert, etc...) et capturer l'esprit qui s'y trouve ! choisis un pouvoir qui te permettra la capture facile d'au moins un et combat les autres habilement"
    welcome_surface = start_font.render(welcome_text, True, (255, 255, 255))
    welcome_rect = welcome_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60))

    start_button_text_surface = start_font.render("Press 'S' to start", True, (255, 255, 255))
    start_button_rect = start_button_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True

        screen.fill((33, 33, 33))
        screen.blit(welcome_surface, welcome_rect)
        screen.blit(start_button_text_surface, start_button_rect)
        pygame.display.flip()
        await asyncio.sleep(0)

async def end_screen(player_won):
    end_font = pygame.font.Font("kongtext.ttf", 40)
    result_text = "You Win!" if player_won else "Game Over"
    result_surface = end_font.render(result_text, True, (255, 255, 255))
    result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    restart_text_surface = end_font.render("Press 'R' to restart", True, (255, 255, 255))
    restart_rect = restart_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True

        screen.fill((33, 33, 33))
        screen.blit(result_surface, result_rect)
        screen.blit(restart_text_surface, restart_rect)
        pygame.display.flip()
        await asyncio.sleep(0)

class Character:
    def __init__(self, name, power, damage, sheet_position, map_position, speed):
        self.name = name
        self.power = power
        self.damage = damage
        self.sheet_position = sheet_position
        self.map_position = map_position
        self.speed = speed

# Store  game color's variable
class Colors:
    WHITE = (255, 255, 255)
    YELLOW = (255, 215, 0)
    DARK_GRAY = (33, 33, 33)

# Store game asset's path variable
class Paths:
    BACKGROUND = "background/background.png"
    CHARACTERS_SPRITE_SHEET = "assets/characters.png"
    MENU_IMAGE = "menu.png"
    BULLET_IMAGE = "bullet/1.png"
    FONT_PATH = "kongtext.ttf"  

CHARACTERS = [
    Character(name="Vulcanus", power="fire", damage=10, sheet_position=(468,288), map_position=(400,300),speed=4),
    Character(name="Aeris", power="wind", damage=15, sheet_position=(312, 288), map_position=(400,300),speed=4),
    Character(name="Voltara", power="thunder", damage=20, sheet_position=(156, 0), map_position=(400,300),speed=4),
    Character(name="Stonewarden", power="earth", damage=25, sheet_position=(0, 0), map_position=(400,300),speed=4),
    Character(name="Nereida", power="water", damage=30, sheet_position=(0, 288), map_position=(400,300),speed=4),
]

ENEMIES = [
    Character(name="Infernus", power="fire", damage=10, sheet_position=(468,288), map_position=(0,0),speed=2),
    Character(name="Galeblade", power="wind", damage=15, sheet_position=(312, 288), map_position=(1600,450),speed=3),
    Character(name="Fulgur", power="thunder", damage=20, sheet_position=(156, 0), map_position=(1600,650),speed=2),
    Character(name="Terravus", power="earth", damage=25, sheet_position=(0, 0), map_position=(1500,750),speed=2),
    Character(name="Tsunewave", power="water", damage=30, sheet_position=(0, 288), map_position=(1800,300),speed=3),
]

DAMAGE_MATRIX = {
    ("fire", "water"): 25,
    ("wind", "fire"): 25,
    ("thunder", "wind"): 25,
    ("earth", "thunder"): 25,
    ("water", "earth"): 25,
}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Define powers and damage matrix
POWERS = ['fire', 'wind', 'thunder', 'earth', 'water']


# Player settings
PLAYER_START_X = 400
PLAYER_START_Y = 300
PLAYER_SCALE = 0.4
PLAYER_SPEED = 4

ENEMY_STOP_DISTANCE = 150
ENEMY_SHOOT_STOP_DISTANCE = 300
ENEMY_SPEED = 3

SHOOT_COOLDOWN = 40

# Projectile settings
PROJECTILE_SCALE = 2.4
PROJECTILE_SPEED = 8

PROJECTILE_LIFETIME = 1200

pygame.init()

# Creating the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exorsit: Shell Unleashed")
clock = pygame.time.Clock()

# Load images
background = pygame.image.load("background/background.png").convert()
sprite_sheet = pygame.image.load("assets/characters.png").convert_alpha()

class UI:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)

    def update(self):
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        enemies_text = self.font.render(f"Enemies Killed: {self.player.enemies_killed}", True, (255, 255, 255))

        # Adjust the position of UI elements as needed
        health_rect = health_text.get_rect(topleft=(10, 10))
        enemies_rect = enemies_text.get_rect(topleft=(10, 50))

        screen.blit(health_text, health_rect)
        screen.blit(enemies_text, enemies_rect)


def draw_character_menu(selected_index):
    # Load the custom font
    menu_font = pygame.font.Font("kongtext.ttf", 22)
    label_font = pygame.font.Font("kongtext.ttf", 24)  # Font for the label

    line_spacing = 55
    label_margin_top = 60

    label_text = label_font.render("Choose Your Character", True, (255, 255, 255))
    label_rect = label_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + label_margin_top))

    # Blit the label onto the screen
    screen.blit(label_text, label_rect)


    menu_text = [menu_font.render(character.name, True, (240, 240, 240)) for character in CHARACTERS]

    for i, text_surface in enumerate(menu_text):
        rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * line_spacing))

        # Increase space between character names
        rect.y += i * 10  

        pygame.draw.rect(screen, (33, 33, 33), rect)

        # Add padding to the selected rectangle
        if i == selected_index:
            padding = 15
            selected_rect = pygame.Rect(rect.x - padding, rect.y - padding, rect.width + 2 * padding, rect.height + 2 * padding)

            pygame.draw.rect(screen, (255, 215, 0), selected_rect, 4)

        screen.blit(text_surface, rect)

    pygame.display.flip()

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet_position=(0, 0), power="fire", damage=10, map_position=(400,300), speed = 4, max_health=100):
        super().__init__()
        self.position = pygame.math.Vector2(map_position)
        self.sprites = self.load_sprites(sheet_position)
        self.image = self.sprites['down'][0]  # Initial frame
        self.rect = self.image.get_rect(center=self.position)
        self.speed = speed
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.shoot = False
        self.shoot_cooldown = 0
        self.direction = "down"
        self.power = power
        self.damage = damage
        self.max_health = max_health
        self.health = max_health
        self.enemies_killed = 0

    def take_damage(self, projectile_power):
        default_damage = 2

        damage_taken = DAMAGE_MATRIX.get((self.power, projectile_power), default_damage)
        self.health -= damage_taken

        # print(f"Player: {self.power}, projectile_power: {projectile_power}")
        # print(f"Player took {damage_taken} damage. Remaining health: {self.health}\n")

        if self.health <= 0:
            current_game_state = GameState.GAME_OVER

    def load_sprites(self, sheet_position):
        sprite_width, sprite_height = 52, 72
        rows, columns = 4, 3
        sprites = {'down': [], 'left': [], 'right': [], 'up': []}

        for row in range(rows):
            for col in range(columns):
                x = sheet_position[0] + col * sprite_width
                y = sheet_position[1] + row * sprite_height
                sprite = sprite_sheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))

                if row == 0:
                    sprites['down'].append(sprite)
                elif row == 1:
                    sprites['left'].append(sprite)
                elif row == 2:
                    sprites['right'].append(sprite)
                elif row == 3:
                    sprites['up'].append(sprite)

        return sprites




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
        if keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

            

        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        # Check if no movement keys are pressed
        if not any((keys[pygame.K_z], keys[pygame.K_s], keys[pygame.K_q], keys[pygame.K_d])):
                self.animation_frame = 0  # Reset animation frame to the first sprite

    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_projectile = self.position
            player_direction_angle = 0  # Default angle (up)

            if self.direction == "down":
                player_direction_angle = 90  # Angle for down
            elif self.direction == "up":
                player_direction_angle = -90  # Angle for right
            elif self.direction == "left":
                player_direction_angle = 180  # Angle for left
            elif self.direction == "right":
                player_direction_angle = 0  # Angle for right

            self.projectile = Projectile(spawn_projectile[0], spawn_projectile[1], self.direction, math.radians(player_direction_angle), power=self.power, shooter = self)
            projectile_group.add(self.projectile)
            all_sprites_group.add(self.projectile)

    def move(self):
        new_position = self.position + pygame.math.Vector2(self.velocity_x, self.velocity_y)

        # Clamp the player's position to stay within the game world boundaries
        new_position.x = max(0, min(new_position.x, background.get_width() - self.rect.width))
        new_position.y = max(0, min(new_position.y, background.get_height() - self.rect.height))

        self.position = new_position

    def update_animation(self):

        if self.velocity_x > 0:
            self.direction = 'right'
        elif self.velocity_x < 0:
            self.direction = 'left'
        elif self.velocity_y < 0:
            self.direction = 'up'
        elif self.velocity_y > 0:
            self.direction = 'down'

        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(self.sprites[self.direction]):
            self.animation_frame = 0

        self.image = self.sprites[self.direction][int(self.animation_frame)]
        
    def update(self):
        self.user_input()
        self.move()
        self.update_animation()
        self.rect.center = self.position
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet_position=(312, 0), power="fire", damage=10, map_position=(400,300), speed = 4, max_health=100):
        super().__init__(enemy_group, all_sprites_group)
        self.position = pygame.math.Vector2(map_position)
        self.sprites = self.load_sprites(sheet_position)
        self.image = self.sprites['down'][0]  # Initial frame
        self.rect = self.image.get_rect(center=self.position)
        self.speed = speed
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.shoot = False
        self.shoot_cooldown = 0
        self.direction = "down"
        self.velocity_x = 0
        self.velocity_y = 0
        self.power = power
        self.damage = damage
        self.max_health = max_health
        self.health = max_health

    def draw_health_bar(self, screen, offset_x, offset_y):
        # Calculate the position of the health bar above the enemy
        health_bar_x = self.rect.topleft[0] - offset_x
        health_bar_y = self.rect.topleft[1] - offset_y - 10  # Adjust the vertical offset as needed

        # Calculate the width of the health bar based on the current health
        health_bar_width = int((self.health / self.max_health) * self.rect.width)

        # Draw the health bar background
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, self.rect.width, 5))

        # Draw the filled part of the health bar based on current health
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width, 5))

    def take_damage(self, projectile_power):
        default_damage = 20

        damage_taken = DAMAGE_MATRIX.get((self.power, projectile_power), default_damage)
        self.health -= damage_taken

        # print(f"Player: {self.power}, projectile_power: {projectile_power}")
        # print(f"Player took {damage_taken} damage. Remaining health: {self.health}\n")

        if self.health <= 0:
            player.enemies_killed += 1
            self.kill()

    def hunt_player(self, player):
        player_vector = pygame.math.Vector2(player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)

        # Calculate the vector pointing from the enemy to the player
        direction_to_player = player_vector - enemy_vector

        # Get the distance to the player in pixels
        distance_to_player = direction_to_player.length()

        # print("Distance to player:", distance_to_player) 

        if distance_to_player < ENEMY_STOP_DISTANCE:
            # Normalize the vector to get a unit vector
            direction_to_player.normalize_ip()
            # Calculate the angle between the enemy and the player
            angle = math.atan2(direction_to_player.y, direction_to_player.x)
            self.is_shooting(angle)

        if distance_to_player > ENEMY_STOP_DISTANCE:
            # Normalize the vector to get a unit vector
            direction_to_player.normalize_ip()

            # Calculate the angle between the enemy and the player
            angle = math.atan2(direction_to_player.y, direction_to_player.x)

            # Set the enemy's velocity based on the normalized vector
            self.velocity_x = direction_to_player.x * self.speed
            self.velocity_y = direction_to_player.y * self.speed

            # Start shooting at the player with the calculated angle
            
        else:
            # Stop moving towards the player
            self.velocity_x = 0
            self.velocity_y = 0
        
                # Stop hunting if the distance to the player is greater than 400 pixels
        if distance_to_player > 400:
            self.velocity_x = 0
            self.velocity_y = 0

        # print("Enemy position:", self.position)  
        # print("Player position:", player.position)  

    def load_sprites(self, sheet_position):
        sprite_width, sprite_height = 52, 72
        rows, columns = 4, 3
        sprites = {'down': [], 'left': [], 'right': [], 'up': []}

        for row in range(rows):
            for col in range(columns):
                x = sheet_position[0] + col * sprite_width
                y = sheet_position[1] + row * sprite_height
                sprite = sprite_sheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))

                if row == 0:
                    sprites['down'].append(sprite)
                elif row == 1:
                    sprites['left'].append(sprite)
                elif row == 2:
                    sprites['right'].append(sprite)
                elif row == 3:
                    sprites['up'].append(sprite)

        return sprites

    def is_shooting(self, angle):
        # calculate the distance to player
        player_vector = pygame.math.Vector2(player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        direction_to_player = player_vector - enemy_vector
        distance_to_player = direction_to_player.length()

        if distance_to_player <= ENEMY_SHOOT_STOP_DISTANCE and self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_projectile = self.position
            self.projectile = Projectile(spawn_projectile[0], spawn_projectile[1], self.direction, angle, power=self.power, shooter=self)
            projectile_group.add(self.projectile)
            all_sprites_group.add(self.projectile)

    def move(self):

        new_position = self.position + pygame.math.Vector2(self.velocity_x, self.velocity_y)

        # Clamp the enemy's position to stay within the game world boundaries
        new_position.x = max(0, min(new_position.x, background.get_width() - self.rect.width))
        new_position.y = max(0, min(new_position.y, background.get_height() - self.rect.height))

        self.position = new_position

    def update_animation(self):

        if self.velocity_x > 0:
            self.direction = 'right'
        elif self.velocity_x < 0:
            self.direction = 'left'
        elif self.velocity_y < 0:
            self.direction = 'up'
        elif self.velocity_y > 0:
            self.direction = 'down'

        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(self.sprites[self.direction]):
            self.animation_frame = 0

        self.image = self.sprites[self.direction][int(self.animation_frame)]

        if self.velocity_x == 0 and self.velocity_y ==0:
            self.animation_frame = 0  # Reset animation frame to the first sprite
        
    def update(self):
        self.hunt_player(player)
        self.move()
        self.update_animation()
        self.rect.center = self.position
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def custom_draw(self, player):
        offset_x = player.rect.centerx - SCREEN_WIDTH // 2
        offset_y = player.rect.centery - SCREEN_HEIGHT // 2

        # Ensure the camera does not go beyond the map boundaries
        offset_x = max(0, min(offset_x, background.get_width() - SCREEN_WIDTH))
        offset_y = max(0, min(offset_y, background.get_height() - SCREEN_HEIGHT))

        screen.blit(background, (-offset_x, -offset_y))

        for sprite in all_sprites_group:
            offset_pos = sprite.rect.topleft[0] - offset_x, sprite.rect.topleft[1] - offset_y
            screen.blit(sprite.image, offset_pos)

            if isinstance(sprite, Enemy):
                sprite.draw_health_bar(screen, offset_x, offset_y)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, player_direction, angle=0, power="fire", shooter="null"):
        super().__init__()

        self.direction = player_direction
        self.angle = angle
        self.x = x
        self.y = y
        self.speed = PROJECTILE_SPEED
        self.projectile_lifetime = PROJECTILE_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
        self.power = power
        self.shooter = shooter

        self.load_image()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.image = pygame.transform.scale(self.image, (24, 24))

    def load_image(self):
        power_mapping = {
            "fire": "fire.png",
            "water": "water.png",
            "wind": "wind.png",
            "earth": "earth.png",
            "thunder": "thunder.png",
        }

        power_image_path = os.path.join("bullet", power_mapping.get(self.power, "1.png"))
        self.image = pygame.image.load(power_image_path).convert_alpha()

    def handle_collisions(self, player, enemies):
        if self.shooter != player and self.rect.colliderect(player.rect):
            player.take_damage(projectile_power=self.power)
            self.kill()

        enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in enemy_hits:
            if self.shooter != enemy:
                enemy.take_damage(projectile_power=self.power)
                self.kill()

    def projectile_movement(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.projectile_lifetime:
            self.kill()

    def update(self):
        self.projectile_movement()
        self.handle_collisions(player, enemies)


all_sprites_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemies = [Enemy(map_position=enemy.map_position, sheet_position=enemy.sheet_position, power=enemy.power, damage=enemy.damage, speed=enemy.speed) for enemy in ENEMIES]
# Create the player instance with a different character
camera = Camera()
# Create enemy instances using the ENEMIES list
enemy_group.add(*enemies)
all_sprites_group.add(*enemies)
selected_character = ""

async def character_selection_menu():
    selected_index = 0
    menu_image = pygame.image.load("menu.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(CHARACTERS)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(CHARACTERS)
                elif event.key == pygame.K_RETURN:
                    return CHARACTERS[selected_index]

        screen.fill((33, 33, 33))
        x_centered = (screen.get_width() - menu_image.get_width()) // 2
        screen.blit(menu_image, (x_centered, 0))

        draw_character_menu(selected_index)

        pygame.display.flip()
        await asyncio.sleep(0)

async def main():
    global all_sprites_group, projectile_group, enemy_group, selected_character, player, current_game_state

    while True:
        pygame.event.pump()  # Process events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if current_game_state == GameState.CHARACTER_SELECTION:
            start_game = await start_screen()
            if start_game:
                selected_character = await character_selection_menu()
                player = Player(
                    sheet_position=selected_character.sheet_position,
                    power=selected_character.power,
                    damage=selected_character.damage,
                    speed=selected_character.speed
                )
                all_sprites_group.add(player)
                ui = UI(player)
                current_game_state = GameState.PLAYING

        elif current_game_state == GameState.PLAYING:
            camera.custom_draw(player)

            all_sprites_group.update()
            ui.update()

            # Check for win or lose conditions
            if len(enemy_group) == 0:
                current_game_state = GameState.GAME_OVER
                player_won = True
            elif player.health <= 0:
                current_game_state = GameState.GAME_OVER
                player_won = False

        elif current_game_state == GameState.GAME_OVER:
            restart = await end_screen(player_won)
            if restart:
                # Reset game state for a new game
                current_game_state = GameState.CHARACTER_SELECTION
                player.kill()
                all_sprites_group.empty()
                projectile_group.empty()
                enemy_group.empty()
                ui = UI(player)

        # Update the screen
        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)
asyncio.run(main())

