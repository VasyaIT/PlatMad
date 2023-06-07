import pygame

font = 'files/DS Stamper.ttf'

ALL_POSITIONS = {
    'h_x': 0,
    'h_y': 350,
    'e_x': 1500,
    'e_y': 380,
    'z_x': 1500,
    'z_y': 310,
    'g_x': 1500,
    'g_y': 290,
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
