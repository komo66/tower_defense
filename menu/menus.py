import pygame
import os
from dir_path import *

pygame.init()

# menu
BUILD_MENU_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "build_menu.png")), (200, 200))
UPGRADE_MENU_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "upgrade_menu.png")), (180, 180))
# buttons in upgrade menu
UPGRADE_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "upgrade_button.png")), (110, 22))
SELL_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "sell_button.png")), (110, 22))
PROPERTIES_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "properties_button.png")), (110, 22))
ULTRA_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "ultra_button.png")), (132, 45))
# buttons in build menu
MOON_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "moon_build.png")), (50, 50))
RED_FIRE_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "red_build.png")), (50, 50))
BLUE_FIRE_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "blue_build.png")), (48, 48))
OBELISK_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "obelisk_build.png")), (50, 50))
# control buttons
muse_button_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR,"muse.png")), (80, 80))
music_button_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR,"sound.png")), (80, 80))
pause_button_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR,"pause.png")), (80, 80))

up_button_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "transparent.png")),(60,55))
down_button_image = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "transparent.png")),(60,55))

BLOOD_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "blood_potion.png")), (66,61))
AOE_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "aoe_potion.png")), (66, 61))
KILL_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "kill_potion.png")), (66, 61))
SLOW_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "slow_potion.png")), (66, 61))
BOSS_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "boss_potion.png")), (66, 61))
TOWER_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "tower_potion.png")), (66, 61))


class Button:
    def __init__(self, image, name: str, x: int, y: int):
        self.image = image
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def clicked(self, x:int, y:int)-> bool:
        return True if self.rect.collidepoint(x, y) else False

    @property
    def response(self)->str:
        return self.name


class Menu:
    def __init__(self, x: int, y: int):
        self.image = UPGRADE_MENU_IMAGE

        self.rect = self.image.get_rect()
        self.rect.center = (x - 18, y + 10)
        self._buttons = []

    @property
    def buttons(self)->list:
        return self._buttons


class UpgradeMenu(Menu):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)
        self._buttons = [Button(PROPERTIES_BTN_IMAGE, "properties", self.rect.centerx, self.rect.centery - 50),
                         Button(UPGRADE_BTN_IMAGE, "upgrade", self.rect.centerx, self.rect.centery - 17),
                         Button(SELL_BTN_IMAGE, "sell", self.rect.centerx, self.rect.centery + 20),
                         Button(ULTRA_BTN_IMAGE, "ultra", self.rect.centerx + 2, self.rect.centery + 54)
                         ]


class BuildMenu(Menu):
    def __init__(self, x:int, y:int):
        super().__init__(x + 7, y - 17)
        self.image = BUILD_MENU_IMAGE
        self._buttons = [Button(MOON_BTN_IMAGE, "moon", self.rect.centerx + 11, self.rect.centery - 61),
                         Button(RED_FIRE_BTN_IMAGE, "red fire", self.rect.centerx + 10, self.rect.centery + 80),
                         Button(BLUE_FIRE_BTN_IMAGE, "blue fire", self.rect.centerx - 58, self.rect.centery + 8),
                         Button(OBELISK_BTN_IMAGE, "obelisk", self.rect.centerx + 80, self.rect.centery + 8)
                         ]


class MainMenu:
    def __init__(self):
        self._buttons = [Button(music_button_image, "music", 815, 45),
                         Button(muse_button_image, "mute", 895, 45),
                         Button(pause_button_image, "pause", 980, 45),
                         Button(up_button_image, "potion_up",43,123),
                         Button(down_button_image, "potion_down",43,566),
                         Button(BLOOD_POTION_IMAGE,'blood_potion',43,196),
                         Button(AOE_POTION_IMAGE,'aoe_potion',43,257),
                         Button(KILL_POTION_IMAGE, 'kill_potion', 43, 257 + 61),
                         Button(SLOW_POTION_IMAGE, 'slow_potion', 43, 257 + 61 * 2),
                         Button(BOSS_POTION_IMAGE, 'boss_potion', 43, 257 + 61 * 3),
                         Button(TOWER_POTION_IMAGE, 'tower_potion', 43, 257 + 61 * 4)
                         ]

    @property
    def buttons(self)->list:
        return self._buttons







