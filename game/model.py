from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from menu.menus import Menu
import pygame
import os
from tower.towers import Tower, Vacancy
from enemy.enemy_group import EnemyGroup
from menu.menus import UpgradeMenu, BuildMenu, MainMenu
from settings import WIN_WIDTH, WIN_HEIGHT,singleton_vol_controller,singleton_map_controller
from game_UI.game_UI import GameUI
from opt_menu.opt_menu import OptMenu
from game_over.game_over import GameOver
from game_win.game_win import GameWin
from game.user_request import *
from dir_path import *


class GameModel:
    def __init__(self):
        # data
        self.level_counter = int(singleton_map_controller.map_index)
        self.bg_image = pygame.transform.scale(singleton_map_controller.curMap, (WIN_WIDTH, WIN_HEIGHT))
        singleton_map_controller.next_map_index = singleton_map_controller.map_index + 1

        self.__menu = None
        self.__main_menu = MainMenu()
        self.__plots = []
        for pt in singleton_map_controller.curVacancyList:
            self.__plots.append(Vacancy(pt[0], pt[1]))

        self.show_tower_info = False

        # selected item
        self.selected_plot = None
        self.selected_tower = None
        self.selected_button = None
        self.selected_potion_info=None
        # apply observer pattern
        self.subject = RequestSubject(self)
        self.seller = TowerSeller(self.subject)
        self.developer = TowerDeveloper(self.subject)
        self.evolution = TowerEvolution(self.subject)
        self.add_money = AddMoney(self.subject)
        self.health_up = HealthUp(self.subject)
        self.add_towers = AddTowers(self.subject)
        self.kill_all = KillAll(self.subject)
        self.factory = TowerFactory(self.subject)
        self.generator = EnemyGenerator(self.subject)
        self.dieHandler = Die(self.subject)
        self.liveHandler = Live(self.subject)

        self.muse = Muse(self.subject)
        self.music = Music(self.subject)

        self.pause = Pause(self.subject)

        self.properties = TowerProperties(self.subject)
        self.proper = Music(self.subject)

        self.mousePosTracker = MousePosTracker(self.subject)

        self.max_hp = 10
        self.hp = self.max_hp
        if self.level_counter == 1:
            self.wave = 0
            self.money = 750
        elif self.level_counter == 2:
            self.wave = 3
            self.money = 2000
        elif self.level_counter == 3:
            self.wave = 6
            self.money = 3000
        elif self.level_counter == 4:
            self.wave = 9
            self.money = 4000
        else:
            self.wave = 12
            self.money = 5000

        self.__towers = []
        self.potions = Potionfunction(self.subject)
        self.__enemies = EnemyGroup(self.wave)

        self.sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "sound.mp3"))
        self.buff_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "buff.mp3"))
        self.debuff_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "debuff.mp3"))
        self.hp_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "hp.mp3"))
        self.meteor_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "meteor.mp3"))
        self.beam_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "beam.mp3"))
        self.evil_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "evil.mp3"))
        self.sound.set_volume(singleton_vol_controller.sound_volume)

        self.UI = GameUI()
        self.opt_menu = OptMenu()
        self.GameOverMenu = GameOver()
        self.GameWinMenu = GameWin()

    def user_request(self, user_request: str):
        """ add tower, sell tower, upgrade tower"""
        self.subject.notify(user_request)

    def get_request(self, events: dict) -> str:
        """get keyboard response or button response"""
        # initial
        self.selected_button = None
        # game result
        if events["die"]:
            return "die"
        if events["live"]:
            return "live"
        # key event
        if events["keyboard key"] is not None:
            return "start new wave"
        if events["Add money"] is not None:
            return "add money"
        if events["Kill all"] is not None:
            return "kill all"
        if events["Add towers"] is not None:
            return "add towers"
        if events["health up"] is not None:
            return "health up"
        if events["pause_esc"] is not None:
            return "pause"
        # mouse event
        if events["mouse position"] is not None:
            x, y = events["mouse position"]
            self.select(x, y)
            if self.selected_button is not None:
                return self.selected_button.response
            return "nothing"
        return "nothing"

    def select(self, mouse_x: int, mouse_y: int) -> None:
        """change the state of whether the items are selected"""
        # if the item is clicked, select the item
        for tw in self.__towers:
            if tw.clicked(mouse_x, mouse_y):
                self.sound.play()
                self.selected_tower = tw
                self.selected_plot = None

        for pt in self.__plots:
            if pt.clicked(mouse_x, mouse_y):
                self.sound.play()
                self.selected_tower = None
                self.selected_plot = pt

        # if the button is clicked, get the button response.
        # and keep selecting the tower/plot.
        if self.__menu is not None:
            for btn in self.__menu.buttons:
                if btn.clicked(mouse_x, mouse_y):
                    self.sound.play()
                    self.selected_button = btn
                    # if select the move button then close the menu
                    if btn == "move":
                        self.__menu = None
            if self.selected_button is None:
                self.selected_tower = None
                self.selected_plot = None
                self.show_tower_info = False

        # menu btn
        for btn in self.__main_menu.buttons:
            if btn.clicked(mouse_x, mouse_y):
                self.selected_button = btn

    def call_menu(self):
        if self.selected_tower is not None:
            x, y = self.selected_tower.rect.center
            self.__menu = UpgradeMenu(x, y)
        elif self.selected_plot is not None:
            x, y = self.selected_plot.rect.center
            self.__menu = BuildMenu(x, y)
        else:
            self.__menu = None

    def towers_attack(self):
        for tw in self.__towers:
            tw.attack(self.__enemies.get())

    def enemies_advance(self):
        self.__enemies.advance(self)

    @property
    def enemies(self) -> EnemyGroup:
        return self.__enemies

    @property
    def towers(self) -> list:
        return self.__towers

    @property
    def menu(self)->Menu:
        return self.__menu

    @menu.setter
    def menu(self, new_menu:Menu):
        self.__menu = new_menu

    @property
    def plots(self)->list:
        return self.__plots

    @property
    def main_menu(self)->MainMenu:
        return self.__main_menu
    
    @main_menu.setter
    def main_menu(self, new_menu:Menu):
        self.__main_menu = new_menu















