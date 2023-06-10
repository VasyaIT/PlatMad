import pygame


font = 'files/DS Stamper.ttf'

GODZILLA_BULLETS = {
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
}


def image_load(image):
    return pygame.image.load(image).convert_alpha()


def font_render(title: str, size: int, AA: bool, color):
    text = pygame.font.Font(font, size)
    surface = text.render(title, AA, color)
    return surface


def ticks():
    current = pygame.time.get_ticks()
    return current // 20


def draw_sprite(*args, screen):
    for sprite in args:
        sprite.draw(screen)


def update_sprite(*args):
    for sprite in args:
        sprite.update()


def draw_and_update(*args, screen):
    draw_sprite(*args, screen=screen)
    update_sprite(*args)


def hero_img(block_left_img):
    end = pygame.time.get_ticks() - 200
    if end >= block_left_img:
        return True
