import pygame
import os
from singleton import VolController,MapController
from dir_path import *

# screen size
WIN_WIDTH = 1024
WIN_HEIGHT = 600
# frame rate
FPS = 60
# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (147, 0, 147)

# image
HP_GRAY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR,"hp_gray.png")), (35, 33))
HP_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR,"hp.png")), (35, 33))
MOUSE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "mouse.png")), (20, 20))

# singleton
singleton_vol_controller=VolController()
singleton_map_controller=MapController(WIN_WIDTH, WIN_HEIGHT)

# global var
game_status:dict={
    "run":True,
    "go_start_menu":False,
    "restart":False
}

potion_price:dict={
    "blood_potion":2000,
    "aoe_potion":1000,
    "kill_potion":4000,
    "slow_potion":1500,
    "boss_potion":5000,
    "tower_potion":3000
}

# transparency of some menu btn
test_transparency=0