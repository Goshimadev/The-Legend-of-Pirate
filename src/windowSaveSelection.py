import pygame
from window import Window
from functions import createSprite, load_image
from windowGame import WindowGame


class WindowSaveSelection(Window):
    image_start = load_image("start.png", -1)
    image_quit = load_image("quit.png", -1)

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        scale = 16

        self.save1 = createSprite(WindowSaveSelection.image_start, scale, self.all_sprites, 750, 200)
        self.save2 = createSprite(WindowSaveSelection.image_start, scale, self.all_sprites, 750, 450)
        self.save3 = createSprite(WindowSaveSelection.image_start, scale, self.all_sprites, 750, 700)

        self.startSave = None

    def draw(self, screen: pygame.Surface):
        self.all_sprites.draw(screen)

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.save1.rect.collidepoint(event.pos):
                self.startSave = 1
            if self.save2.rect.collidepoint(event.pos):
                self.startSave = 2
            if self.save3.rect.collidepoint(event.pos):
                self.startSave = 3

    def update(self):
        if (self.startSave is not None):
            return WindowGame(self.startSave)
