"""
Привет из 2024 !
python -m pygbag platformerhabrahabr.py
"""
# Импортируем библиотеку pygame
import pygame
#Объявляем переменные(я их не показываю , птомучто их много)
async def main():
    print("Starting the game...")
    loadLevel()
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
    bg_path = os.path.join(os.path.dirname(__file__), "background", BACKGROUND_IMAGE)
    bg = image.load(bg_path)
    bg = transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
    menu = Menu(screen)
    # далее много информации и создание уровня

# конце
level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group() # Все передвигающиеся объекты
platforms = [] # то, во что мы будем врезаться или опираться



if __name__ == "__main__":
    asyncio.run(main())

