from typing import Any, Callable
from functions import removeFromCollisions
from game.animator import Animator, AnimatorData
from game.entity import Entity, EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("skeleton", [
    ("stay.png", 0, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("moveW.png", 150, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("moveS.png", 150, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("moveA.png", 150, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("moveD.png", 150, (9, 13), (-0.15, -0.45, 0.69, 1)),
    ("attack.png", 250, (9, 13), (-0.15, -0.45, 0.69, 1)),
])


class EntitySkeleton(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.speed = 0.05
        self.rise = True
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.strength = 0
        self.healthMax = 2
        self.health = 2
        self.width = 0.4
        self.height = 0.55
        self.state = "go"
        self.dirR = True
        self.pastY = self.y
        self.attackDelay = 0
        self.bone = None

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        if ("direction" in data):
            self.dirR = data["direction"] == "right"
        if ("rise" in data):
            self.rise = bool(data["rise"])

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags and super().canGoOn(tile)

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def update(self):
        collisions = super().update()
        removeFromCollisions(collisions, ["player"])
        if (not self.alive or Settings.disableAI):
            return
        self.attackDelay = max(self.attackDelay - 1000 / Settings.fps, 0)
        if (self.state == "go"):
            self.animator.setAnimation("moveD" if self.dirR else "moveA")
            self.speedX = self.speed * (1 if self.dirR else -1)
            self.speedY = 0
            rise = False
            if (self.dirR):
                if (self.x - int(self.x) >= (1 - self.width) / 2):
                    rise = True
            else:
                if (self.x - int(self.x) <= (1 - self.width) / 2):
                    rise = True
            if (rise or len(collisions) != 0):
                nx = int(self.x) + (1 if self.dirR else -1) + (1 - self.width) / 2
                collisions = self.predictCollisions(nx, self.y)
                removeFromCollisions(collisions, ["player"])
                if (len(collisions) != 0 or len(collisions) != 0):
                    self.dirR = not self.dirR
                    self.x = int(self.x) + (1 - self.width) / 2
                    self.state = "rise"
                    self.pastY = self.y
                    ny = int(self.y) + (-1 if self.rise else 1) + (1 - self.height) / 2
                    collisions = self.predictCollisions(self.x, ny)
                    removeFromCollisions(collisions, ["player"])
                    if (len(collisions) != 0):
                        self.rise = not self.rise
            if (self.state == "go"):
                if (abs(self.x - self.screen.player.x) < self.screen.player.width or
                        abs(self.y - self.screen.player.y) < self.screen.player.height):
                    self.speedX = 0
                    self.speedY = 0
                    self.state = "attack"
                    self.animator.setAnimation("attack")
                    self.bone = EntityAlive.createById("bone", self.screen)
                    if (abs(self.x - self.screen.player.x) < self.screen.player.width):
                        self.bone.x = self.x + (self.width - self.bone.width) / 2
                        if (self.screen.player.y >= self.y):
                            self.bone.y = self.y + self.height
                            self.bone.speedY = self.bone.speed
                        else:
                            self.bone.y = self.y - self.height - self.bone.height
                            self.bone.speedY = -self.bone.speed
                    if (abs(self.y - self.screen.player.y) < self.screen.player.height):
                        self.bone.y = self.y + (self.height - self.bone.height) / 2
                        if (self.screen.player.x >= self.x):
                            self.bone.x = self.x + self.width
                            self.bone.speedX = self.bone.speed
                        else:
                            self.bone.x = self.x - self.width - self.bone.height
                            self.bone.speedX = -self.bone.speed
        elif (self.state == "rise"):
            self.animator.setAnimation("moveW" if self.rise else "moveS")
            self.speedX = 0
            self.speedY = self.speed * (-1 if self.rise else 1)
            if (abs(self.pastY - self.y) >= 1 or len(collisions) != 0):
                self.y = int(self.y) + (1 - self.height) / 2
                self.state = "go"
        elif (self.state == "attack"):
            if (self.animator.lastState[1]):
                if (self.attackDelay <= 0):
                    self.state = "go"
                else:
                    self.animator.setAnimation("attack", 1)
            elif (self.animator.lastState[0]):
                self.attackDelay = 2000
                if (self.bone is not None):
                    self.screen.addEntity(self.bone)
                    self.bone = None


EntityAlive.registerEntity("skeleton", EntitySkeleton)
