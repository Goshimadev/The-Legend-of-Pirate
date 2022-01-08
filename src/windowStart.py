import pygame
from window import Window
from functions import createSprite, load_image
from windowSaveSelection import WindowSaveSelection


class WindowStart(Window):
    image_start = load_image("start.png")
    image_quit = load_image("quit.png")

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        scale = 0.4

        self.start = createSprite(WindowStart.image_start, scale, self.all_sprites, 0.3, 0.15)
        self.quit = createSprite(WindowStart.image_quit, scale, self.all_sprites, 0.3, 0.55)

        self.starting = False

    def draw(self, screen: pygame.Surface):
        self.all_sprites.draw(screen)

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit.rect.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if self.start.rect.collidepoint(event.pos):
                self.starting = True

    def update(self):
        if self.starting:
            return WindowSaveSelection()