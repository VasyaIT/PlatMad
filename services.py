import pygame
from pygame.mixer import Sound


RED = (255, 0, 0)
BARD = (200, 0, 0)
BLACK = (0, 0, 0)
VIOLET = (162, 0, 255)
WIDTH = 1200
HEIGHT = 650
FPS = 60

pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_start_music = Sound('files/music/game_start.mp3')
game_active_music = Sound('files/music/game_active.mp3')
shoot_music = Sound('files/music/shoot_hero.mp3')
evil_shoot_music = Sound('files/music/evil_shoot.mp3')
godzilla_shoot_music = Sound('files/music/godz_shoot.mp3')
kill_music = Sound('files/music/kill.mp3')
game_over_music = Sound('files/music/game_over.mp3')
no_bullets_music = Sound('files/music/no_bullets.mp3')
recharge_music = Sound('files/music/recharge.mp3')
zombie_music = Sound('files/music/zombie.mp3')
godzilla_music = Sound('files/music/godzilla.mp3')
evil_music = Sound('files/music/evil.mp3')
line_music = Sound('files/music/line.mp3')
jump_music = Sound('files/music/jump.mp3')

game_active_music.set_volume(0.2)
shoot_music.set_volume(0.6)
game_over_music.set_volume(0.5)
zombie_music.set_volume(0.4)
godzilla_music.set_volume(0.3)
evil_music.set_volume(0.7)
godzilla_shoot_music.set_volume(0.7)

font = 'files/static/DS Stamper.ttf'

GODZILLA_BULLETS = [
    'files/bullets/godz_bull.png',
    'files/bullets/godz_bull_30.png',
    'files/bullets/godz_bull_60.png',
    'files/bullets/godz_bull_90.png',
    'files/bullets/godz_bull_120.png',
    'files/bullets/godz_bull_150.png',
    'files/bullets/godz_bull_180.png',
    'files/bullets/godz_bull_210.png',
    'files/bullets/godz_bull_240.png',
    'files/bullets/godz_bull_270.png',
    'files/bullets/godz_bull_300.png',
    'files/bullets/godz_bull_330.png',
]


def image_load(image):
    return pygame.image.load(image).convert_alpha()


def font_render(title: str, size: int, AA: bool, color):
    text = pygame.font.Font(font, size)
    surface = text.render(title, AA, color)
    return surface


def ticks():
    current = pygame.time.get_ticks()
    return current // 20


def draw_sprite(*args):
    for sprite in args:
        sprite.draw(screen)


def update_sprite(*args):
    for sprite in args:
        sprite.update()


def draw_and_update(*args):
    draw_sprite(*args)
    update_sprite(*args)


def hero_img(block_left_img):
    end = pygame.time.get_ticks() - 200
    if end >= block_left_img:
        return True


def layer(level):
    return font_render(f'LAYER {level}', 70, True, (207, 0, 0))


text_surface = font_render('PLATMAD', 50, True, BARD)
gave_over_surface = font_render('GAME OVER', 70, True, RED)
start_text_surface = font_render('PRESS SPACE TO START', 60, True, 'YELLOW')
bullets_surface = image_load('files/static/bullets.png')
health_surface = image_load('files/static/health.png')
background_surface = image_load('files/static/background.png').convert()
kit_surface = image_load('files/static/kit.png')
