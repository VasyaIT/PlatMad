from random import choice, randint

import pygame
from pygame.sprite import Sprite, Group, GroupSingle, spritecollide, groupcollide

import services
from services import image_load, font_render, draw_and_update, hero_img, GODZILLA_BULLETS, screen, layer


game_start = True
game_active = False
is_line = False
is_jump = False
is_kit = False

block_left_img = 0
score = 0

pygame.init()
pygame.display.flip()
pygame.display.set_caption('PlatMad')
icon = image_load('files/static/background.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

services.game_start_music.play(-1)


# Sprites
class Hero(Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = image_load('files/characters/hero_right.png')
        self.image_left = image_load('files/characters/hero_left.png')
        self.image_right_walk = image_load('files/characters/hero_right_walk.png')
        self.image_left_walk = image_load('files/characters/hero_left_walk.png')
        self.image_line = image_load('files/characters/hero_line.png')
        self.image_line_left = image_load('files/characters/hero_line_left.png')
        self.image = self.image_right
        self.rect = self.image.get_rect(midbottom=(170, 465), width=40)
        self.rect_line = self.image_line.get_rect()
        self.gravity = 0
        self.health = 10
        self.bullets = 10
        self.step = 0
        self.line_time = 0
        self.center = self.rect.center

    def hero_moves(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.rect.bottom == 465 and self.image != self.image_line \
                and self.image != self.image_line_left:
            global is_jump
            if not is_jump:
                services.jump_music.play()
            if self.image == self.image_line or self.image == self.image_right_walk:
                self.image = self.image_right
            elif self.image == self.image_line_left or self.image == self.image_left_walk:
                self.image = self.image_left
            self.gravity = -15
        if key[pygame.K_d] and self.rect.x < 1000:
            if self.image != self.image_line:
                if self.rect.bottom < 465:
                    self.image = self.image_right
                else:
                    self.image = self.image_right if self.step >= 0.5 else self.image_right_walk
                    self.step += 0.1
                    if self.step > 1:
                        self.step = 0
            self.rect.x += 2
        if key[pygame.K_a] and self.rect.x > 100:
            if hero_img(block_left_img):
                if self.image != self.image_line_left:
                    if self.rect.bottom < 465:
                        self.image = self.image_left
                    else:
                        self.image = self.image_left if self.step >= 0.5 else self.image_left_walk
                        self.step += 0.1
                        if self.step > 1:
                            self.step = 0
            self.rect.x -= 2
        if key[pygame.K_s]:
            if hero_img(block_left_img):
                self.rect.height = 50
                if self.image == self.image_right or self.image == self.image_right_walk:
                    self.image = self.image_line
                elif self.image == self.image_left or self.image == self.image_left_walk:
                    self.image = self.image_line_left
            global is_line
            if not is_line:
                services.line_music.play()
                is_line = True
            hero.sprite.line_time = 10

    def destroy(self):
        if self.health <= 0:
            services.game_over_music.play(0)
            global game_active
            game_active = False

    def apply_line(self):
        global is_line
        if self.line_time > 0:
            self.line_time -= 1
            if self.line_time == 0:
                is_line = False
                self.rect.height = 101
                if self.image == self.image_line:
                    self.image = self.image_right
                elif self.image == self.image_line_left:
                    self.image = self.image_left

    def apply_gravity(self):
        self.gravity += 0.9
        self.rect.y += self.gravity
        if self.gravity == 0:
            global is_jump
            is_jump = False
        if self.rect.bottom >= 465:
            self.rect.bottom = 465

    def update(self):
        self.hero_moves()
        self.apply_line()
        self.apply_gravity()
        self.destroy()


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
        if not randint(0, 300) and self.rect.x < services.WIDTH:
            if self.kind == 'godzilla':
                self.rect.centery = randint(self.rect.top, self.rect.bottom - 10)
                services.godzilla_shoot_music.play()
            if self.kind == 'evil':
                services.evil_shoot_music.play()
            bullet = BulletEnemy(self.rect.x, self.rect.centery, self.kind)
            bullets_enemy.add(bullet)

    def jump(self):
        if self.kind == 'evil' and self.rect.bottom == 465 and not randint(0, 100):
            self.gravity = -15

    def destroy(self):
        if self.health <= 0:
            services.kill_music.play()
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
        self.kind = kind
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
            self.index += 1
            if self.index > 11:
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


# Functions
def get_layer_surface():
    global score
    if 0 < score < 200:
        return layer(1)
    if 5000 <= score < 5200:
        return layer(2)
    if 10000 <= score < 10200:
        return layer(3)


def score_logic():
    if score < 5000:
        if not randint(0, 300):
            enemies.add(Enemy(c))
            if c == 'zombie':
                services.zombie_music.play()
            if c == 'godzilla':
                services.godzilla_music.play()
            if c == 'evil':
                services.evil_music.play()
        if score % 1000 == 0:
            services.recharge_music.play()
            hero.sprite.bullets += 1
    if 5000 <= score < 10000:
        if not randint(0, 200):
            enemies.add(Enemy(c))
        if score % 500 == 0:
            services.recharge_music.play()
            hero.sprite.bullets += 1
    if score >= 10000:
        if not randint(0, 100):
            enemies.add(Enemy(c))
        if score % 250 == 0:
            services.recharge_music.play()
            hero.sprite.bullets += 1


def trophies_draw():
    if 1000 < score < 5000:
        trophy_surface = image_load('files/trophies/trophy_bronz.png')
    elif 5000 <= score < 10000:
        trophy_surface = image_load('files/trophies/trophy_silver.png')
    elif 10000 <= score < 20000:
        trophy_surface = image_load('files/trophies/trophy_gold.png')
    elif score >= 20000:
        trophy_surface = image_load('files/trophies/trophy_leg.png')
    else:
        trophy_surface = None
    return trophy_surface


while True:
    for event in pygame.event.get():

        if (event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        if game_active:
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                if hero.sprite.bullets <= 0:
                    services.no_bullets_music.play()
                else:
                    services.shoot_music.play()

                    block_left_img = pygame.time.get_ticks()

                    hero.sprite.rect.height = 101
                    hero.sprite.image = hero.sprite.image_right
                    new_bullet_hero = BulletHero(hero.sprite.rect.x + hero.sprite.rect.width + 52,
                                                 hero.sprite.rect.centery - 10)
                    bullets_hero.add(new_bullet_hero)
                    hero.sprite.bullets -= 1

    keys = pygame.key.get_pressed()

    screen.blit(services.background_surface, (0, 0))

    if game_start:
        screen.blit(services.text_surface, (420, 30))
        screen.blit(services.start_text_surface, (265, 160))

        if keys[pygame.K_SPACE]:
            game_start = False
            game_active = True
            services.game_start_music.stop()
            services.game_active_music.play(-1)

    elif game_active:
        score += 1
        c = choice(['evil', 'zombie', 'godzilla'])
        score_logic()
        if get_layer_surface():
            screen.blit(get_layer_surface(), (400, 100))
        draw_and_update(hero, enemies, bullets_hero, bullets_enemy)

        if score % 5000 == 0:
            is_kit = False
            x_pos = randint(500, 800)
        if score > 5000:
            if not is_kit:
                screen.blit(services.kit_surface, (x_pos, 418))
            if x_pos - 50 < hero.sprite.rect.x < x_pos + 10 and 425 < hero.sprite.rect.bottom <= 475 and not is_kit:
                is_kit = True
                hero.sprite.health += 1

        if spritecollide(hero.sprite, enemies, False):
            hero.sprite.health = 0

        for enemy in groupcollide(enemies, bullets_hero, False, True).keys():
            enemy.health -= new_bullet_hero.damage

        for enemy_bullet in spritecollide(hero.sprite, bullets_enemy, True):
            hero.sprite.health -= enemy_bullet.damage

        bullets_count_surface = font_render(str(hero.sprite.bullets), 50, True, services.BLACK)
        health_count = font_render(str(hero.sprite.health), 50, True, services.RED)
        score_surface = font_render(f'SCORE: {str(score // 10)}', 60, True, services.VIOLET)

        screen.blit(bullets_count_surface, (50, 30))
        screen.blit(services.bullets_surface, (95, 40))
        screen.blit(health_count, (160, 30))
        screen.blit(services.health_surface, (210, 42))
        screen.blit(score_surface, (400, 20))
    else:
        services.game_active_music.stop()
        services.godzilla_music.stop()
        services.zombie_music.stop()
        services.recharge_music.stop()
        if trophies_draw():
            screen.blit(trophies_draw(), (480, 310))
        screen.blit(services.text_surface, (420, 30))
        screen.blit(services.gave_over_surface, (365, 100))
        screen.blit(score_surface, (400, 210))
        screen.blit(services.start_text_surface, (265, 500))
        enemies.empty()
        bullets_hero.empty()
        bullets_enemy.empty()
        hero.empty()

        if keys[pygame.K_SPACE]:
            hero.add(Hero())
            score = 0
            game_active = True
            services.game_over_music.stop()
            services.game_active_music.play(-1)

    pygame.display.update()
    clock.tick(services.FPS)
