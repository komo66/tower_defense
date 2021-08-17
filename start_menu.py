import pygame
import os
import math
from game.game import Game
from color_settings import *
from settings import WIN_WIDTH, WIN_HEIGHT, FPS,singleton_vol_controller, singleton_map_controller,game_status,test_transparency
from opt_menu.opt_menu import OptMenu
from exit_win.exit_win import ExitWin
from dir_path import *

MOUSE = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "mouse.png")), (20, 20))

pygame.init()
pygame.mixer.init()


class StartMenu:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        # background
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "start_menu3.png")), (WIN_WIDTH, WIN_HEIGHT))
        # button
        self.start_btn = Buttons(430, 355, 170, 50)  # x, y, width, height
        self.opt_btn=Buttons(430, 425, 170, 50)
        self.buttons = [self.start_btn,
                        self.opt_btn]
        # btn img
        # self.opt_btn_img=pygame.transform.scale(pygame.image.load(os.path.join("images", "options.png")), (338,100))

        # music and sound
        self.sound = pygame.mixer.Sound(os.path.join(SOUND_DIR,"sound.mp3"))

    def play_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(SOUND_DIR,"menu.mp3"))
        pygame.mixer.music.set_volume(singleton_vol_controller.music_volume)
        pygame.mixer.music.play(-1)
        self.sound.set_volume(singleton_vol_controller.sound_volume)

    def menu_run(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption("Arrivederci")
        self.play_music()
        while game_status["run"] :
            game_status["go_start_menu"]= False
            clock.tick(FPS)
            self.menu_win.blit(self.bg, (0, 0))

            surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            for btn in self.buttons:
                pygame.draw.rect(surface,(255,255,255,test_transparency),btn.rect)
            self.menu_win.blit(surface, (0, 0))

            x, y = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)
            self.menu_win.blit(MOUSE, (x, y))
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    exitWin=ExitWin()
                    exitWin.run()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if hit start btn
                    if self.start_btn.clicked(x, y):       
                        self.sound.play()

                        i=True
                        while i:
                            game = Game()
                            game.run()
                            if game_status["restart"]:
                                game_status["restart"]= False
                                i=True
                            else:
                                i=False

                        singleton_map_controller.change_map()


                        self.play_music()

                    if self.opt_btn.clicked(x, y):
                        self.sound.play()
                        opt_menu=OptMenu()
                        opt_menu.run()
                        self.sound.set_volume(singleton_vol_controller.sound_volume)
                        singleton_map_controller.change_map()

                    """(Q1.1) music on/off according to the button"""
                    # (hint) pygame.mixer.music.pause/unpause

            # while cursor is moving (not click)
            """(Q1.2) create button frame and draw"""
            # (hint) use a for loop to go through all the buttons, create the frame, and draw it.
            pygame.display.update()
        pygame.quit()


class Buttons:
    def __init__(self, x:int, y:int, width:int, height:int):
        self.rect = pygame.Rect(x, y, width, height)
        self.frame = None

    def clicked(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x, y):
            return True
        return False

    def create_frame(self, x: int, y: int):
        """if cursor position is on the button, create button frame"""
        if self.clicked(x, y):
            x, y, w, h = self.rect
            self.frame = pygame.Rect(x - 5, y - 5, w + 10, h + 10)
        else:
            self.frame = None

    def draw_frame(self, win: pygame.Surface):
        if self.frame is not None:
            pygame.draw.rect(win, WHITE, self.frame, 10)



