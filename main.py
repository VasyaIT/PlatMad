import pygame
from pygame.sprite import Sprite, Group, GroupSingle, spritecollide, groupcollide

from services import image_load, font_render, draw_and_update

WIDTH = 1200
HEIGHT = 650
FPS = 60

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BARD = (200, 0, 0)

game_start = True
game_active = False

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.flip()
pygame.display.set_caption('PlatMad')
clock = pygame.time.Clock()

text_surface = font_render('PLATMAD', 50, True, BARD)
gave_over_surface = font_render('GAME OVER', 70, True, RED)
start_text_surface = font_render('PRESS SPACE TO START', 60, True, 'YELLOW')

background_surface = image_load('files/background.png').convert()


class Hero(Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = image_load('files/characters/hero_right.png')
        self.image_left = image_load('files/characters/hero_left.png')
        self.image = self.image_right
        self.rect = self.image.get_rect(midbottom=(170, 465))
        self.gravity = 0
        self.bullets = 10

    def hero_moves(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.rect.bottom == 465:
            self.gravity = -15
        if key[pygame.K_d] and self.rect.x < 1000:
            self.image = self.image_right
            self.rect.x += 2
        if key[pygame.K_a] and self.rect.x > 100:
            self.image = self.image_left
            self.rect.x -= 2
        if key[pygame.K_s]:
            self.rect.bottom += 2

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 465:
            self.rect.bottom = 465

    def update(self):
        self.hero_moves()
        self.apply_gravity()


class Evil(Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_load('files/characters/evil.png')
        self.rect = self.image.get_rect(midbottom=(0, 465))
        self.gravity = 0


class Zombie(Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_load('files/characters/zombie.png')
        self.rect = self.image.get_rect(midbottom=(1200, 465))
        self.speed = 1

    def update(self):
        self.rect.x -= self.speed


class Godzilla(Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_load('files/characters/godzilla.png')
        self.rect = self.image.get_rect(midbottom=(0, 465))
        self.gravity = 0


class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_start = image_load('files/characters/hero_bull.png')
        self.image_post = image_load('files/characters/h_bull_bang.png')
        self.image = self.image_start
        self.rect = self.image.get_rect(x=x, y=y)
        self.gravity = 0

    def update(self):
        self.rect.x += 15


# Groups
hero = GroupSingle()
hero.add(Hero())

zombies = GroupSingle()
zombies.add(Zombie())

bullets = Group()


while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hero.sprite.bullets > 0:
            hero.sprite.image = hero.sprite.image_right
            new_bullet = Bullet(hero.sprite.rect.x + hero.sprite.rect.width, hero.sprite.rect.centery - 10)
            bullets.add(new_bullet)
            hero.sprite.bullets -= 1

    keys = pygame.key.get_pressed()

    screen.blit(background_surface, (0, 0))
    screen.blit(text_surface, (420, 30))

    if game_start:
        screen.blit(start_text_surface, (265, 160))

        if keys[pygame.K_SPACE]:
            game_start = False
            game_active = True

    elif game_active:
        draw_and_update(hero, zombies, bullets, screen=screen)

        if spritecollide(hero.sprite, zombies, False):
            game_active = False

        if spritecollide(zombies.sprite, bullets, True):
            zombies.sprite.kill()
            zombies.add(Zombie())
            # zombies.draw(screen)
            # zombies.update()

    else:
        screen.blit(gave_over_surface, (365, 300))
        screen.blit(start_text_surface, (265, 430))

        if keys[pygame.K_SPACE]:
            game_active = True

    pygame.display.update()
    clock.tick(FPS)
