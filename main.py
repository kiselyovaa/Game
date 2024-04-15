import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 522
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sweet Life")

background_img = pygame.image.load("img/background.png").convert()
background_img = pygame.transform.scale(background_img, (4096, 522))
background_x = 0

player_walk1 = pygame.image.load("img/player1.png").convert_alpha()
player_walk1 = pygame.transform.scale(player_walk1, (71, 123))
player_walk2 = pygame.image.load("img/player2.png").convert_alpha()
player_walk2 = pygame.transform.scale(player_walk2, (71, 123))

walk_index = 0
walk_delay = 10
walk_counter = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_walk1
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 120
        self.y_speed = 0
        self.jump_speed = -15
        self.max_speed = 10
        self.jumping = False

    def update(self):
        global walk_index, walk_counter

        if walk_counter % walk_delay == 0:
            if walk_index == 0:
                self.image = player_walk1
                walk_index = 1
            elif walk_index == 1:
                self.image = player_walk2
                walk_index = 0
        walk_counter = (walk_counter + 1) % (walk_delay * 2)

        self.y_speed += GRAVITY
        self.rect.y += self.y_speed

        if self.rect.bottom >= SCREEN_HEIGHT - 120:
            self.rect.bottom = SCREEN_HEIGHT - 120
            self.y_speed = 0
            self.jumping = False


class Lava(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("img/lava.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (69, 23))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = SCREEN_HEIGHT - 110

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("img/platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


GRAVITY = 0.5

clock = pygame.time.Clock()
running = True

lava_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

lava_x = SCREEN_WIDTH
lava = Lava(lava_x)
lava_group.add(lava)

platform_x = SCREEN_WIDTH + random.randint(100, 200)
platform_y = random.randint(200, 350)
platform = Platform(platform_x, platform_y)
platform_group.add(platform)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.jumping:
                player.y_speed = player.jump_speed
                player.jumping = True
            elif event.key == pygame.K_SPACE and player.jumping:
                player.y_speed = player.jump_speed * 0.5

    if player.jumping:
        if pygame.sprite.spritecollide(player, platform_group, False):
            player.rect.bottom = platform.rect.top
            player.y_speed = 0

    if pygame.sprite.spritecollide(player, lava_group, False):
        running = False

    background_x -= 3
    if background_x <= -4096:
        background_x = 0

    for lava in lava_group:
        lava.rect.x -= 3
        if lava.rect.right < 0:
            lava.rect.left = SCREEN_WIDTH

    for platform in platform_group:
        platform.rect.x -= 3
        if platform.rect.right < 0:
            platform.rect.left = SCREEN_WIDTH
            platform.rect.y = random.randint(200, 350)

    all_sprites.update()
    screen.blit(background_img, (background_x, 0))
    screen.blit(background_img, (background_x + 4096, 0))

    lava_group.draw(screen)
    platform_group.draw(screen)
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
