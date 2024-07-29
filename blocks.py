import pygame
from pygame import *
import os
import pyganim
from pygame import transform

WALL_WIDTH = 32
WALL_HEIGHT = 32
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 32
TELEPORT_WIDTH = 32
TELEPORT_HEIGHT = 64
PLATFORM_COLOR = "#000000"

if os.environ.get('WEB_ENV'):
    BASE_DIR = '/'  # для веб-версии
else:
    BASE_DIR = os.path.dirname(__file__)  # для локальной версии

ICON_DIR = os.path.join(BASE_DIR, 'blocks')  # Путь к каталогу с файлами блоков

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load(os.path.join(ICON_DIR, "platform.png"))
        self.image = transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load(os.path.join(ICON_DIR, "dieBlock.png"))

class Spring(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load(os.path.join(ICON_DIR, "spring.png"))
        self.image = transform.scale(self.image, (WALL_WIDTH, WALL_HEIGHT))
        self.rect = Rect(x, y, WALL_WIDTH, WALL_HEIGHT)
        self.boost_power = 30  # Сила подброса

    def boost(self, player):
        player.yvel = -self.boost_power

class Wall(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load(os.path.join(ICON_DIR, "wall.png"))
        self.image = transform.scale(self.image, (WALL_WIDTH, WALL_HEIGHT))
        self.rect = Rect(x, y, WALL_WIDTH, WALL_HEIGHT)

class BlockTree(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load(os.path.join(ICON_DIR, "block_tree.png"))
        self.image = transform.scale(self.image, (32, 32))
        self.rect = Rect(x, y, 32, 32)

class InvisibleDeadlyBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image.set_alpha(0)
        self.rect = Rect(x, y, 32, 32)

class InvisibleBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image.set_alpha(0)
        self.rect = Rect(x, y, 32, 32)

class LavaBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load(os.path.join(ICON_DIR, "lava_block.png"))
        self.image = transform.scale(self.image, (32, 32))
        self.rect = Rect(x, y, 32, 32)

class CloudBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load(os.path.join(ICON_DIR, "Cloud_block.png"))
        self.image = transform.scale(self.image, (96, 64))
        self.rect = Rect(x, y, 96, 64)

class CloudSpringBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load(os.path.join(ICON_DIR, "Cloud_block_2.png"))
        self.image = transform.scale(self.image, (96, 64))
        self.rect = Rect(x, y, 96, 64)
        self.boost_power = 35

    def boost(self, player):
        player.yvel = -self.boost_power

class BlockTeleport(sprite.Sprite):
    def __init__(self, x, y, teleport_id):
        sprite.Sprite.__init__(self)
        self.destination = None
        self.teleport_id = teleport_id
        self.image = image.load(os.path.join(ICON_DIR, "portal.png"))
        self.image = transform.scale(self.image, (TELEPORT_WIDTH, TELEPORT_HEIGHT))
        self.rect = Rect(x, y, TELEPORT_WIDTH, TELEPORT_HEIGHT)

    def set_destination(self, dest):
        self.destination = dest

    def teleport(self, player):
        if self.destination:
            print(f"Телепортация игрока с {player.rect.x}, {player.rect.y} на {self.destination.rect.x}, {self.destination.rect.y}")
            player.rect.x = self.destination.rect.x
            player.rect.y = self.destination.rect.y
            player.checkpoint = self.destination
        else:
            print("Ошибка: назначение телепорта не установлено")

class Letter(pygame.sprite.Sprite):
    def __init__(self, x, y, letter_number):
        pygame.sprite.Sprite.__init__(self)
        self.letter_number = letter_number
        self.info_image = self.get_number_image()
        original_image = pygame.image.load(os.path.join(ICON_DIR, "letter.jpg"))
        self.image = pygame.transform.scale(original_image, (52, 52))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False

    def get_number_image(self):
        image_path = os.path.join(ICON_DIR, f"{self.letter_number}_number.jpg")
        try:
            original_image = pygame.image.load(image_path)
            return pygame.transform.scale(original_image, (256, 256))
        except FileNotFoundError:
            print(f"Предупреждение: Файл изображения номера {self.letter_number} не найден. Использую заполнитель.")
            placeholder = pygame.Surface((256, 256))
            placeholder.fill((200, 200, 200))
            return placeholder

    def update(self):
        if self.collected:
            self.image = pygame.Surface((1, 1))
            self.image.set_alpha(0)