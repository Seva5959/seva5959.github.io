#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import *
from blocks import *
from monsters import *
import asyncio
import random
#Объявляем переменные

playerX = 110
playerY = 44
BACKGROUND_IMAGE = "background.jpg"
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"
FILE_DIR = os.path.dirname(__file__)

if os.environ.get('WEB_ENV'):
    ICON_DIR = '/'  # для веб-версии
else:
    ICON_DIR = os.path.dirname(__file__)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.collected_images = []
        self.image_size = (240, 240)
        # Загрузка изображений
        self.menu_button = pygame.image.load(os.path.join(ICON_DIR, "menu", "menu_button.png"))
        self.menu_button = pygame.transform.scale(self.menu_button, (100, 75))  # Увеличили в 2 раза
        self.menu_button_rect = self.menu_button.get_rect(topright=(WIN_WIDTH - 20, 20))

        self.board = pygame.image.load(os.path.join(ICON_DIR, "menu", "board.png"))
        self.board = pygame.transform.scale(self.board, (WIN_WIDTH - 100, WIN_HEIGHT - 100))
        self.board_rect = self.board.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))

        self.exit_button = pygame.image.load(os.path.join(ICON_DIR, "menu", "exit_button.png"))
        self.exit_button = pygame.transform.scale(self.exit_button, (80, 60))  # Увеличили в 3 раза
        self.exit_button_rect = self.exit_button.get_rect(
            topright=(self.board_rect.right - 20, self.board_rect.top + 20))

    def toggle(self):
        self.active = not self.active

    def add_image(self, image):
        self.collected_images.append(image)

    def draw(self):
        if not self.active:
            self.screen.blit(self.menu_button, self.menu_button_rect)
        else:
            self.screen.blit(self.board, self.board_rect)
            self.screen.blit(self.exit_button, self.exit_button_rect)

            # Отображение собранных изображений
            for i, img in enumerate(self.collected_images[:4]):  # Ограничиваем до 4 изображений
                row = i // 2
                col = i % 2

                # Увеличиваем изображение
                img = pygame.transform.scale(img, self.image_size)

                # Вычисляем позицию для каждого изображения
                x = self.board_rect.left + 50 + col * (self.board_rect.width // 2 - 40)
                y = self.board_rect.top + 40 + row * (self.board_rect.height // 2 - 40)

                img_rect = img.get_rect(topleft=(x, y))
                self.screen.blit(img, img_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button_rect.collidepoint(event.pos) and not self.active:
                self.toggle()
            elif self.exit_button_rect.collidepoint(event.pos) and self.active:
                self.toggle()
#кнопки
class VirtualButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.pressed = False
        self.just_pressed = False

    def update(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed and not self.pressed:
                self.just_pressed = True
            else:
                self.just_pressed = False
            self.pressed = pressed
        else:
            self.pressed = False
            self.just_pressed = False



class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        if isinstance(target, pygame.Rect):
            return target.move(self.state.topleft)
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


# В основном файле (main.py или подобном)
def loadLevel():
    global playerX, playerY

    levelFile = open(os.path.join(ICON_DIR, 'levels', '1.txt'))
    line = " "
    commands = []
    while line[0] != "/":
        line = levelFile.readline()
        if line[0] == "[":
            while line[0] != "]":
                line = levelFile.readline()
                if line[0] != "]":
                    endLine = line.find("|")
                    level.append(line[0: endLine])

        if line[0] != "":
            commands = line.split()
            if len(commands) > 1:
                if commands[0] == "player":
                    playerX = int(commands[1])
                    playerY = int(commands[2])

    levelFile.close()

async def main():
    print("Starting the game...")
    loadLevel()
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
    bg_path = os.path.join(ICON_DIR, "background", BACKGROUND_IMAGE)
    bg = image.load(bg_path)
    bg = transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
    menu = Menu(screen)

    virtual_buttons = pygame.sprite.Group()
    button_size = 80
    button_margin = 10
    screen_width, screen_height = DISPLAY

    left_button = VirtualButton(button_margin, screen_height - button_size - button_margin, button_size, button_size,
                                os.path.join(ICON_DIR,"blocks", "left_buttons.png"))
    right_button = VirtualButton(button_size + button_margin * 2, screen_height - button_size - button_margin,
                                 button_size, button_size,
                                 os.path.join(ICON_DIR,"blocks", "right_buttons.png"))
    up_button = VirtualButton(screen_width - button_size - button_margin,
                              screen_height - button_size * 2 - button_margin * 2, button_size, button_size,
                              os.path.join(ICON_DIR,"blocks", "up_buttons.png"))

    virtual_buttons = pygame.sprite.Group(left_button, right_button, up_button)


    letter_count = 0  # Счетчик для нумерации писем

    left = right = False  # по умолчанию - стоим
    up = False
    running = False

    hero = Player(playerX, playerY, menu)  # создаем героя по (x,y) координатам
    entities.add(hero)

    timer = pygame.time.Clock()
    x = y = 0  # координаты

    teleport = None
    destination = None
    teleport = None
    destination = None
    x = y = 0  # Инициализируем x и y
    PLATFORM_WIDTH = 32
    PLATFORM_HEIGHT = 32
    teleports = {}  # Словарь для хранения всех телепортов
    destinations = {}  # Словарь для хранения всех назначений
    for row_index, row in enumerate(level):
        for col_index, col in enumerate(row):
            # Вычисляем x и y для каждого элемента
            x = col_index * WALL_WIDTH  # используем WALL_WIDTH для позиционирования по горизонтали
            y = row_index * WALL_HEIGHT  # используем WALL_HEIGHT для позиционирования по вертикали

            if col == "=":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == "S":
                spring = blocks.Spring(x, y)
                entities.add(spring)
                platforms.append(spring)
            elif col == "+":
                tree = BlockTree(x, y)
                entities.add(tree)
                platforms.append(tree)
            elif col == "-":
                wall = Wall(x, y)
                entities.add(wall)
                platforms.append(wall)
            elif col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            elif col == "N":
                cloud_spring = CloudSpringBlock(x, y)
                entities.add(cloud_spring)
                platforms.append(cloud_spring)
            elif col == "?":
                cloud = CloudBlock(x, y)
                entities.add(cloud)
                platforms.append(cloud)
            elif col == "/":
                lava = LavaBlock(x, y)
                entities.add(lava)
                platforms.append(lava)
            elif col == "L":
                letter_count = len([e for e in entities if isinstance(e, Letter)])
                letter_number = ["first", "second", "third", "fourth"][letter_count]
                letter = Letter(x, y, letter_number)
                entities.add(letter)
                platforms.append(letter)
            elif col == "^":
                deadly_block = blocks.InvisibleDeadlyBlock(x, y)
                entities.add(deadly_block)
                platforms.append(deadly_block)
            elif col == "!":
                invisible_block = blocks.InvisibleBlock(x, y)
                entities.add(invisible_block)
                platforms.append(invisible_block)
            elif col == "M":
                mn = Monster(x, y, left=1, up=0)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
            elif col in ["T", "G", "D"]:
                teleport = blocks.BlockTeleport(x, y, col)
                entities.add(teleport)
                platforms.append(teleport)
                animatedEntities.add(teleport)
                teleports[col] = teleport

            elif col in ["J", "E", "A"]:  # Назначения телепортов (добавлен "A")
                destination = blocks.Platform(x, y)
                entities.add(destination)
                platforms.append(destination)
                destinations[col] = destination

            # Устанавливаем назначения для телепортов
            if "T" in teleports and "J" in destinations:
                teleports["T"].set_destination(destinations["J"])


            if "G" in teleports and "E" in destinations:
                teleports["G"].set_destination(destinations["E"])


            if "D" in teleports and "A" in destinations:
                teleports["D"].set_destination(destinations["A"])


            x += PLATFORM_WIDTH  # Увеличиваем x на полную ширину платформы

            y += PLATFORM_HEIGHT  # Увеличиваем y на полную высоту платформы
        x = 0  # на каждой новой строчке начинаем с нуля
    if "T" in teleports and "J" in destinations:
        teleports["T"].set_destination(destinations["J"])

    if "G" in teleports and "E" in destinations:
        teleports["G"].set_destination(destinations["E"])

    if "D" in teleports and "A" in destinations:
        teleports["D"].set_destination(destinations["A"])
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    clock = pygame.time.Clock()
    FPS = 60


    show_number = False
    current_number = None
    number_display_time = 0
    number_image = None
    collected_letters = set()
    while not hero.winner:  # Основной цикл программы
        clock.tick(FPS)
        delta_time = clock.tick(60) / 1000.0
        await asyncio.sleep(0)
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

            menu.handle_event(e)

        if not menu.active:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            virtual_buttons.update(mouse_pos, mouse_pressed)

            VIRTUAL_BUTTON_SPEED_FACTOR = 0.5

            left = pygame.key.get_pressed()[pygame.K_LEFT] or (left_button.pressed * VIRTUAL_BUTTON_SPEED_FACTOR)
            right = pygame.key.get_pressed()[pygame.K_RIGHT] or (right_button.pressed * VIRTUAL_BUTTON_SPEED_FACTOR)
            up = pygame.key.get_pressed()[pygame.K_UP] or up_button.just_pressed

            if not hero.winner and hero.alive():
                collision_result = hero.update(left, right, up, running, platforms)
                if isinstance(collision_result, str) and collision_result.startswith("show_number_"):
                    letter_number = collision_result.split("_")[2]
                    if letter_number not in collected_letters:
                        collected_letters.add(letter_number)
                        show_number = True
                        current_number = letter_number
                        number_display_time = pygame.time.get_ticks()
                        for letter in [p for p in platforms if
                                       isinstance(p, blocks.Letter) and p.letter_number == current_number]:
                            number_image = letter.get_number_image()
                            break
            else:
                # Сброс состояния кнопок, если герой умер или игра окончена
                left = right = up = False

            movement_x = (right - left) * MOVE_SPEED * delta_time
            hero.rect.x += movement_x

            animatedEntities.update()  # показываем анимацию
            monsters.update(platforms)  # передвигаем всех монстров
            camera.update(hero)  # центризируем камеру относительно персонажа

        screen.blit(bg, (0, 0))

        if not menu.active:
            # Обновляем все спрайты
            for e in entities:
                screen.blit(e.image, camera.apply(e))
                if isinstance(e, Letter):
                    e.update()

            if show_number and number_image:
                screen.blit(number_image, (WIN_WIDTH // 2 - 128, WIN_HEIGHT // 2 - 128))
                if pygame.time.get_ticks() - number_display_time > 7000:  # Показываем число 7 секунды
                    show_number = False
                    number_image = None

            virtual_buttons.draw(screen)

        menu.draw()
        pygame.display.update()  # обновление и вывод всех изменений на экран




level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group() # Все передвигающиеся объекты
platforms = [] # то, во что мы будем врезаться или опираться



if __name__ == "__main__":
    asyncio.run(main())
