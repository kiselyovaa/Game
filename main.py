import pygame
import sys
import random

pygame.init()

# ИГРОВЫЕ НАЙСТРОЙКИ
# Очки
points = 0
points_color = (255, 255, 255)
points_place = (610, 472)

# Этапы
lvl2_value = 50
win_value = 100

game_speed = 4
game_speed_lvl2 = 6

GRAVITY = 0.6  # Гравитация

# ГЛАВНОЕ ОКНО
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 522
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sweet Life")

# ИГРОВЫЕ ПЕРЕМЕННЫЕ
# Для анимации
walk_index = 0  # индекс спрайта
walk_delay = 10  # задержка спрайта
walk_counter = 0  # счетчик фреймов

running = True
pause = True
lose = False
win = False


# Картинки и спрайты
def get_image(filename, size):
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img


start_img = get_image("img/start.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
win_img = get_image("img/win.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
lose_img = get_image("img/lose.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

background_img = get_image("img/background.png", (4096, SCREEN_HEIGHT))
background_x = 0

platform_img = get_image("img/platform.png", (100, 30))
lava_img = get_image("img/lava.png", (69, 23))
lava_img2 = get_image("img/lava2.png", (69, 23))
candy_img = get_image("img/candy.png", (70, 50))

player_walk1 = pygame.image.load("img/player1.png").convert_alpha()
player_walk2 = pygame.image.load("img/player2.png").convert_alpha()
player_size = [  # <---- фиксируем размеры изображения (3, 4)
    [pygame.transform.scale(player_walk1, (24, 41)), pygame.transform.scale(player_walk2, (24, 41))],  # 0 | 1 hp
    [pygame.transform.scale(player_walk1, (47, 82)), pygame.transform.scale(player_walk2, (47, 82))],  # 1 | 2 hp
    [pygame.transform.scale(player_walk1, (71, 123)), pygame.transform.scale(player_walk2, (71, 123))]  # 2 | 3 hp
]


# Классы на основе которых будут создаваться объекты
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 3  # <---- число жизней (3)
        self.invul = False  # <---- неуязвимость (3)
        self.invul_cd = 50  # <---- таймер неуязвимости (3)
        self.image = player_size[self.hp - 1][0]
        self.rect = self.image.get_rect()  # hitbox
        self.rect.centerx = SCREEN_WIDTH // 4
        self.rect.bottom = SCREEN_HEIGHT - 120
        self.y_speed = 0
        self.jump_speed = -15
        self.max_speed = 10
        self.jumping = False

    def animation(self):
        """Анимация уменьшения и увеличения игрока"""
        self.image = player_size[self.hp - 1][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 4
        self.rect.bottom = SCREEN_HEIGHT - 120

    def update(self):
        global walk_index, walk_counter

        if walk_counter % walk_delay == 0:
            if walk_index == 0:
                self.image = player_size[self.hp - 1][0]
                walk_index = 1
            elif walk_index == 1:
                self.image = player_size[self.hp - 1][1]
                walk_index = 0
        walk_counter = (walk_counter + 1) % (walk_delay * 2)

        self.y_speed += GRAVITY
        self.rect.y += self.y_speed

        if self.rect.bottom >= SCREEN_HEIGHT - 120:
            self.rect.bottom = SCREEN_HEIGHT - 120
            self.y_speed = 0
            self.jumping = False


class GameObject(pygame.sprite.Sprite):  # <---- Конфета (4)
    def __init__(self, x, y, img):
        super().__init__()
        self.image = img
        self.rect = img.get_rect(topleft=(x, y))


# СОЗДАНИЕ ОБЪЕКТОВ
clock = pygame.time.Clock()
points_text = pygame.font.Font(None, 36)

# Игрок
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Лава
lava = GameObject(
    x=SCREEN_WIDTH,
    y=SCREEN_HEIGHT - 135,
    img=lava_img
)
lava2 = GameObject(
    x=SCREEN_WIDTH,
    y=SCREEN_HEIGHT - 135,
    img=lava_img2
)
lava_group = pygame.sprite.Group()
lava_group.add(lava)

# Платформы
platform = GameObject(
    x=SCREEN_WIDTH + random.randint(100, 200),
    y=random.randint(200, 350),
    img=platform_img
)
platform_group = pygame.sprite.Group()
platform_group.add(platform)

# Конфеты (4)
candy = GameObject(
    x=SCREEN_WIDTH + random.randint(200, 800),
    y=random.randint(200, 350),
    img=candy_img
)
if pygame.sprite.spritecollide(candy, platform_group, False):
    candy.rect.bottom = platform.rect.top
candy_group = pygame.sprite.Group()
candy_group.add(candy)

# ИГРОВОЙ ЦИКЛ
while running:

    #### ОТСЛЕЖИВАНИЕ НАЖАТИЙ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Закрытие окна
            running = False
        elif event.type == pygame.KEYDOWN:  # если нажали на клаву
            if win == True or lose == True:  # при условии победы или поражении (3 урок)
                running = False  # завершаем игру (3 урок)
            else:
                pause = False
                if event.key == pygame.K_ESCAPE:
                    pause = True
                elif event.key == pygame.K_SPACE and not player.jumping:  # Прыжки
                    player.y_speed = player.jump_speed
                    player.jumping = True
            # elif event.key == pygame.K_SPACE and player.jumping:
            #     player.y_speed = player.jump_speed * 0.5

    #### ОТРИСОВКА
    pygame.display.flip()
    clock.tick(60)

    if pause == True:  # если пауза (3 урок)
        if win == True:  # при победе
            screen.blit(win_img, (0, 0))
        elif lose == True:  # при поражении
            screen.blit(lose_img, (0, 0))
        else:  # иначе
            screen.blit(start_img, (0, 0))
        continue  # в любои случае не продолжаем игру

    all_sprites.update()
    screen.blit(background_img, (background_x, 0))
    screen.blit(background_img, (background_x + 4096, 0))
    screen.blit(
        points_text.render(f"{points}", True, points_color),
        points_place
    )

    lava_group.draw(screen)
    platform_group.draw(screen)
    candy_group.draw(screen)  # <---- отрисовываем конфеты (4)
    all_sprites.draw(screen)

    #### ДВИЖЕНИЕ ОБЪЕКТОВ ПО ЭКРАТУ
    # Фон
    background_x -= game_speed
    if background_x <= -4096:
        background_x = 0

    # Лава
    for lava in lava_group:
        lava.rect.x -= game_speed
        if lava.rect.right < 0:  # если лава уходит за экран
            lava.rect.left = SCREEN_WIDTH  # то перемещается вправо

    # Платформы
    for platform in platform_group:
        platform.rect.x -= game_speed
        if platform.rect.right < 0:  # если платформа уходит за экран
            platform.rect.left = SCREEN_WIDTH  # то перемещается вправо
            platform.rect.y = random.randint(200, 350)

    # Конфеты
    for candy in candy_group:
        candy.rect.x -= game_speed
        if candy.rect.right < 0:  # если платформа уходит за экран
            candy.rect.left = SCREEN_WIDTH  # то перемещается вправо
            candy.rect.y = random.randint(200, 350)
            if pygame.sprite.spritecollide(candy, platform_group, False):
                candy.rect.bottom = platform.rect.top

    #### ЛОГИКА
    # Лава
    if player.invul:  # <---- если не уязвим (3)
        player.invul_cd -= 1  # <---- запускается таймер неуязвимости
        if player.invul_cd <= 0:  # <---- если таймер закончился
            player.invul = False  # <---- становится уязвим
            player.invul_cd = 50  # <---- и таймер обновляется
    elif pygame.sprite.spritecollide(player, lava_group, False):  # <---- иначе если попадает в лаву (3)
        player.hp -= 1  # <---- то теряем HP
        print("HP", player.hp)
        if player.hp > 0:  # <---- если выжил
            player.animation()  # <---- то уменьшаемся
            player.invul = True  # <---- и становимся неуязвим
        else:
            lose = pause = True  # поражение

    # Платформа
    if player.y_speed > 0 and pygame.sprite.spritecollide(player, platform_group, False):
        player.rect.bottom = platform.rect.top
        player.y_speed = 0
        player.jumping = False

    # Конфеты
    if pygame.sprite.spritecollide(player, candy_group, True):
        candy = GameObject(  # <---- Создаем новую конфету (4)
            x=SCREEN_WIDTH + random.randint(200, 800),
            y=random.randint(200, 350),
            img=candy_img
        )
        if pygame.sprite.spritecollide(candy, platform_group, False):
            candy.rect.bottom = platform.rect.top
        candy_group.add(candy)

        if player.hp < 3:  # <---- Если здоровье не полное (4)
            player.hp += 1  # <---- то лечимся (4)
            player.animation()  # <---- и обновляем спрайт (т.к. здоровья стало больше мы вырастем) (4)
            print("HP", player.hp)
        else:
            points += 10  # <---- Если здоровье полное, то добавляем очки (4)
            print("Points", points)
            if points == lvl2_value:
                game_speed = game_speed_lvl2
                lava2.rect.x = lava.rect.x + SCREEN_WIDTH // 2
                lava_group.add(lava2)
                background_img = get_image("img/background2.png", (4096, SCREEN_HEIGHT)) # <---- Сюда загружаем картинку второго заднего фона
            elif points == win_value:
                win = pause = True

pygame.quit()
sys.exit()
