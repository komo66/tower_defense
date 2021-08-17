import pygame
import os
from settings import WIN_WIDTH, WIN_HEIGHT,FPS,game_status,singleton_vol_controller,test_transparency,singleton_map_controller,MOUSE
from exit_win.exit_win import ExitWin
from dir_path import *

VIC_IMG=pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR,"victory.png")), (WIN_WIDTH, WIN_HEIGHT))

class Victory:
    def __init__(self):
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.reward_btn = pygame.Rect(385, 355, 250, 50)  # x, y, width, height
        self.exit_btn=pygame.Rect(452, 415, 120, 50)
        self.buttons=[self.reward_btn,
                      self.exit_btn]

        self.sound = pygame.mixer.Sound(os.path.join(SOUND_DIR,"sound.mp3"))
        self.sound.set_volume(singleton_vol_controller.sound_volume)

        self.has_draw_reward=False
        self.font = pygame.font.Font(os.path.join(FONT_DIR, "orange juice 2.0.ttf"), 40)
    
    def draw(self):
        self.win.blit(VIC_IMG,(0,0))
        surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        for btn in self.buttons:
            pygame.draw.rect(surface,(255,255,255,128),btn)
        self.win.blit(surface, (0, 0))

        if self.has_draw_reward:
            self.draw_reward()
            
        x, y = pygame.mouse.get_pos()
        self.win.blit(MOUSE, (x, y))

    def draw_reward(self):
        surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        sheet= pygame.Rect(160, 100, 720, 400)
        pygame.draw.rect(surface,(255, 222, 173, 150), sheet)

        text_color = (29, 24, 21)
        text = self.font.render("Thank You!.", True, text_color)
        surface.blit(text, (415, 120))
        text = self.font.render("There are some hotkey used in development", True, text_color)
        surface.blit(text, (163,170))
        text = self.font.render("and now they are yours.", True, text_color)
        surface.blit(text, (315, 220))
        text=self.font.render("\"Tab\" is used to get lots of money.",True, text_color)
        surface.blit(text, (175,290))
        text=self.font.render("\"k\" is used to kill all enemies in a wave.",True, text_color)
        surface.blit(text, (175,340))
        text=self.font.render("\"t\" is used to build towers randomly.",True, text_color)
        surface.blit(text, (175,390))
        text=self.font.render("\"h\" is used to recover 1 HP once.",True, text_color)
        surface.blit(text, (175,440))

        self.win.blit(surface, (0,0))


    def play_music(self):
        pygame.mixer.music.fadeout(int(1*1000)) 
        pygame.mixer.music.load(os.path.join(SOUND_DIR,"victory.mp3"))
        pygame.mixer.music.set_volume(singleton_vol_controller.music_volume)
        pygame.mixer.music.play(-1)
        self.sound.set_volume(singleton_vol_controller.sound_volume)

    def run(self):
        clock = pygame.time.Clock()
        
        run=True
        self.play_music()
        while run:
            clock.tick(FPS)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitWin=ExitWin()
                    exitWin.run()
                    if game_status["run"]:
                        run=True
                    else:
                        run=False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.has_draw_reward=False

                    if self.reward_btn.collidepoint(x, y):
                        self.has_draw_reward=True
                    
                    if self.exit_btn.collidepoint(x, y):
                        game_status["go_start_menu"]= True
                        run=False

            pygame.display.update()