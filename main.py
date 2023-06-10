from random import choice, randint

import pygame
from pygame.sprite import Sprite, Group, GroupSingle, spritecollide, groupcollide

from services import image_load, font_render, draw_and_update, hero_img, GODZILLA_BULLETS

WIDTH = 1200
HEIGHT = 650
FPS = 60

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BARD = (200, 0, 0)

game_start = True
game_active = False

block_left_img = 0
game_duration = 0

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.flip()
pygame.display.set_caption('PlatMad')
icon = image_load('files/characters/zombie.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

text_surface = font_render('PLATMAD', 50, True, BARD)
gave_over_surface = font_render('GAME OVER', 70, True, RED)
start_text_surface = font_render('PRESS SPACE TO START', 60, True, 'YELLOW')
bullets_surface = image_load('files/bullets/bullets.png')
health_surface = image_load('files/health.png')

background_surface = image_load('files/background.png').convert()


class Hero(Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = image_load('files/characters/hero_right.png')
        self.image_left = image_load('files/characters/hero_left.png')
        self.image = self.image_right
        self.rect = self.image.get_rect(midbottom=(170, 465), width=40)
        self.gravity = 0
        self.health = 10
        self.bullets = 10

    def hero_moves(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.rect.bottom == 465:
            self.gravity = -15
        if key[pygame.K_d] and self.rect.x < 1000:
            self.image = self.image_right
            self.rect.x += 2
        if key[pygame.K_a] and self.rect.x > 100:
            if hero_img(block_left_img):
                self.image = self.image_left
            self.rect.x -= 2
        if key[pygame.K_s]:
            self.rect.bottom += 2

    def apply_gravity(self):
        self.gravity += 0.9
        self.rect.y += self.gravity
        if self.rect.bottom >= 465:
            self.rect.bottom = 465

    def update(self):
        self.hero_moves()
        self.apply_gravity()


class Enemy(Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        if kind == 'evil':
            self.image = image_load('files/characters/evil.png')
            self.rect = self.image.get_rect(midbottom=(1280, 465))
            self.speed = 1
            self.gravity = 0
            self.health = 2
        if kind == 'zombie':
            self.image = image_load('files/characters/zombie.png')
            self.rect = self.image.get_rect(midbottom=(1280, 465))
            self.speed = 1
            self.gravity = 0
            self.health = 3
        if kind == 'godzilla':
            self.image = image_load('files/characters/godzilla.png')
            self.rect = self.image.get_rect(midbottom=(1280, 465))
            self.speed = 1
            self.health = 5
            self.gravity = 0

    def shoot(self):
        if not randint(0, 300) and self.rect.x < WIDTH:
            bullet = BulletEnemy(self.rect.x, self.rect.centery, self.kind)
            bullets_enemy.add(bullet)

    def jump(self):
        if self.kind == 'evil' and self.rect.bottom == 465 and not randint(0, 100):
            self.gravity = -15

    def destroy(self):
        if self.health <= 0:
            self.kill()
            hero.sprite.bullets += 3

    def apply_gravity(self):
        if self.kind != 'zombie':
            self.gravity += 0.7
            self.rect.y += self.gravity
            if self.rect.bottom >= 465:
                self.rect.bottom = 465

    def update(self):
        self.rect.x -= self.speed
        self.apply_gravity()
        self.shoot()
        self.jump()
        self.destroy()


class BulletHero(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_start = image_load('files/bullets/hero_bull.png')
        self.image_post = image_load('files/bullets/h_bull_bang.png')
        self.image = self.image_start
        self.rect = self.image.get_rect(x=x, y=y)
        self.damage = 1

    def destroy(self):
        if self.rect.x > 1150:
            self.kill()

    def update(self):
        self.rect.x += 15
        self.destroy()


class BulletEnemy(Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        if kind == 'evil':
            self.image = image_load('files/bullets/evil_bull.png')
            self.rect = self.image.get_rect(x=x, y=y)
            self.damage = 1
            self.speed = 10
        if kind == 'godzilla':
            self.images = []
            for image in GODZILLA_BULLETS:
                self.images.append(image_load(image))
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(x=x, y=y)
            self.damage = 2
            self.speed = 5
        if kind == 'zombie':
            self.image = image_load('files/bullets/godz_bull.png')
            self.rect = self.image.get_rect(x=3000, y=1500)
            self.damage = 0
            self.speed = 0

    def animation(self):
        try:
            self.index += 5
            if self.index > 10:
                self.index = 0
            self.image = self.images[int(self.index)]
        except AttributeError:
            return

    def destroy(self):
        if self.rect.x < 0 or self.rect.x == 3000:
            self.kill()

    def update(self):
        self.rect.x -= self.speed
        self.animation()
        self.destroy()


# Groups
hero = GroupSingle()
hero.add(Hero())

enemies = Group()

bullets_hero = Group()

bullets_enemy = Group()


while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and hero.sprite.bullets > 0
            and game_active
        ):

            block_left_img = pygame.time.get_ticks()

            hero.sprite.image = hero.sprite.image_right
            new_bullet_hero = BulletHero(hero.sprite.rect.x + hero.sprite.rect.width + 52,
                                         hero.sprite.rect.centery - 10)
            bullets_hero.add(new_bullet_hero)
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
        game_duration += 1
        if game_duration % 1000 == 0:
            hero.sprite.bullets += 1

        c = choice(['evil', 'zombie', 'godzilla'])
        if not randint(0, 300) and game_duration < 5000:
            enemies.add(Enemy(c))
        if not randint(0, 200) and 5000 < game_duration < 10000:
            enemies.add(Enemy(c))
        if not randint(0, 100) and game_duration > 10000:
            enemies.add(Enemy(c))

        draw_and_update(hero, enemies, bullets_hero, bullets_enemy, screen=screen)

        if spritecollide(hero.sprite, enemies, False):
            game_active = False

        for enemy in groupcollide(enemies, bullets_hero, False, True).keys():
            enemy.health -= new_bullet_hero.damage

        for i in spritecollide(hero.sprite, bullets_enemy, True):
            hero.sprite.health -= i.damage
            if hero.sprite.health <= 0:
                game_active = False

        bullets_count_surface = font_render(str(hero.sprite.bullets), 50, True, BLACK)
        health_count = font_render(str(hero.sprite.health), 50, True, RED)

        screen.blit(bullets_count_surface, (50, 30))
        screen.blit(bullets_surface, (95, 40))
        screen.blit(health_count, (160, 30))
        screen.blit(health_surface, (210, 42))
    else:
        game_duration = 0
        screen.blit(gave_over_surface, (365, 300))
        screen.blit(start_text_surface, (265, 430))
        enemies.empty()
        bullets_hero.empty()
        bullets_enemy.empty()
        hero.empty()

        if keys[pygame.K_SPACE]:
            hero.add(Hero())
            game_active = True

    pygame.display.update()
    clock.tick(FPS)
