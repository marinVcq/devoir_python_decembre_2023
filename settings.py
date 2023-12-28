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
    Character(name="Infernus", power="fire", damage=10, sheet_position=(468,288), map_position=(0,0),speed=3),
    Character(name="Galeblade", power="wind", damage=15, sheet_position=(312, 288), map_position=(1600,450),speed=4),
    Character(name="Fulgur", power="thunder", damage=20, sheet_position=(156, 0), map_position=(1600,650),speed=2),
    Character(name="Terravus", power="earth", damage=25, sheet_position=(0, 0), map_position=(1500,750),speed=3),
    Character(name="Tsunewave", power="water", damage=30, sheet_position=(0, 288), map_position=(1800,300),speed=3),
]

# Define damage multipliers
DAMAGE_MATRIX = {
    'fire': {'wind': 2, 'water': 0.5, 'thunder': 1, 'earth': 0.3},
    'wind': {'thunder': 2, 'earth': 0.5, 'water': 1, 'fire': 0.3},
    'thunder': {'earth': 2, 'water': 0.5, 'fire': 1, 'wind': 0.3},
    'earth': {'water': 2, 'fire': 0.5, 'wind': 1, 'thunder': 0.3},
    'water': {'fire': 2, 'wind': 0.5, 'thunder': 1, 'earth': 0.3},
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
PROJECTILE_SCALE = 1.4
PROJECTILE_SPEED = 8

PROJECTILE_LIFETIME = 1200