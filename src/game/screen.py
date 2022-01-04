from __future__ import annotations
from typing import Union
import pygame
from functions import GameExeption
from game.entity import Entity
from game.entityPlayer import EntityPlayer
from game.tile import Tile
from game.world import ScreenData, World
from game.saveData import SaveData
from settings import Settings


class Screen:
    def __init__(self, world: World, data: ScreenData, saveData: SaveData, player: EntityPlayer):
        # добавляет player в список entities
        self.surface = pygame.Surface((Settings.width, Settings.height - Settings.overlay_height))
        self.saveData = saveData
        self.world: World
        self.tiles: list[list[Tile]]
        self.entities: list[Entity]
        self.goToVar: ScreenGoTo = None

    def update(self) -> Union[None, ScreenGoTo]:
        # вызов update у всех entities. Возвращает goToVar.
        pass

    def draw(self) -> pygame.Surface:
        # вызов draw у всех entities, возвращает итоговый кадр
        pass

    def addEntity(self, entity: Entity):
        # добавляет entity в их список
        pass

    def removeEntity(self, entity: Entity):
        # удаляет entity из списка
        pass

    def goTo(self, world: str, screen: tuple[int, int]):
        # создаёт ScreenGoTo и присваивает в goToVar
        pass

    @staticmethod
    def create(world: World, x: int, y: int, saveData: SaveData, player: EntityPlayer) -> Screen:
        if (not world.screenExist(x, y)):
            raise GameExeption(f"Screen.create: screen not exist, x: {x}, y: {y}")
        return Screen(world, world[x, y], saveData, player)


class ScreenGoTo:
    def __init__(self, world: str, screen: tuple[int, int], image: pygame.Surface):
        self.world = world
        self.screen = screen
        self.image = image # изображение последнего кадра этого экрана