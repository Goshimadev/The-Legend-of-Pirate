import pygame
from typing import Callable
from functions import getPosMult, getRectMult, load_image, load_sound, multPos as multPosFull
from game.gameDialog import GameDialog
from settings import Settings


multRect = getRectMult(Settings.width, Settings.height - Settings.overlay_height)
multPos = getPosMult(Settings.width, Settings.height - Settings.overlay_height)

sound_btn = load_sound("btn1.mp3", "btn")
sound_btn2 = load_sound("btn2.wav", "btn")


class GameDialog_exit(GameDialog):
    multRectInner = getRectMult(*multPos((0.35, 0.55)))
    btnSize = multPosFull((2.13, 1.28), Settings.tileSize)
    btnSize = (int(btnSize[0]), int(btnSize[1]))
    yes_img = pygame.transform.scale(load_image("yes.png"), btnSize)
    no_img = pygame.transform.scale(load_image("no.png"), btnSize)
    yes_img_a = pygame.transform.scale(load_image("yes_active.png"), btnSize)
    no_img_a = pygame.transform.scale(load_image("no_active.png"), btnSize)
    yes_rect = multRectInner((0.12, 0.65, 0.36, 0.3))
    no_rect = multRectInner((0.59, 0.65, 0.36, 0.3))

    def __init__(self, onClose: Callable):
        super().__init__(onClose, *multPos((0.35, 0.55)))
        font = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.77) + 1)
        font2 = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.5) + 1)
        self.text1 = font.render("Вы уверены, что", True, pygame.Color(81, 44, 40))
        self.text2 = font.render("хотите выйти?", True, pygame.Color(81, 44, 40))
        self.text3 = font2.render("Прогресс будет сохранён", True, pygame.Color(81, 44, 40))
        self.selected = 1

    def draw(self) -> pygame.Surface:
        self.drawBack()
        self.surface.blit(self.yes_img_a if self.selected == 0 else self.yes_img,
                          self.yes_rect.topleft, (0, 0, self.yes_rect.width, self.yes_rect.height))
        self.surface.blit(self.no_img_a if self.selected == 1 else self.no_img, self.no_rect.topleft)
        self.surface.blit(self.text1, multPos((0.028, 0.08)))
        self.surface.blit(self.text2, multPos((0.05, 0.18)))
        self.surface.blit(self.text3, multPos((0.025, 0.28)))
        return self.surface

    def action(self):
        if (self.selected == 0):
            self.closed = True
            self.onClose(True)
            sound_btn.play()
        if (self.selected == 1):
            self.close()

    def close(self):
        sound_btn.play()
        self.closed = True
        self.onClose(False)

    def onMove(self, pos: tuple[int, int]):
        pos = super().onMove(pos)
        if (self.yes_rect.collidepoint(pos)):
            if (self.selected != 0):
                sound_btn2.play()
            self.selected = 0
        if (self.no_rect.collidepoint(pos)):
            if (self.selected != 1):
                sound_btn2.play()
            self.selected = 1

    def onMouseUp(self, pos: tuple[int, int]):
        self.action()

    def onKeyUp(self, key):
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            self.selected = ((self.selected + 1) + 2) % 2
            sound_btn2.play()
        if (key == pygame.K_a or key == pygame.K_LEFT):
            self.selected = ((self.selected - 1) + 2) % 2
            sound_btn2.play()
        if (key == pygame.K_RETURN or key == pygame.K_SPACE):
            self.action()
        if (key == pygame.K_ESCAPE):
            self.close()

    def onJoyHat(self, value):
        if (value[0] > 0):
            self.selected = ((self.selected + 1) + 2) % 2
            sound_btn2.play()
        if (value[0] < 0):
            self.selected = ((self.selected - 1) + 2) % 2
            sound_btn2.play()

    def onJoyButonUp(self, button):
        if (button == 0):
            self.action()
        if (button == 6):
            self.close()
