import pygame
import tkinter
import simulator
import pointclick
import settings
import menu_display
import os
import time

class BigBoss:
    def __init__(self):
        self.run_menu()

    def run_menu(self):
        self.root = tkinter.Tk()
        self.menu_manager = menu_display.MenuManager(self.root, bigboss = self)
        self.root.mainloop()

    def run_pointclick(self):
        self.root.destroy()
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.center_screen = (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2)
        import themes
        self.playmanager = pointclick.PlayManager(boss = self, theme = themes.theme_list['NES_Tetris'], settings = self.menu_manager.settings_menu.setting_output, center = self.center_screen)
        self.retry_prompt = RetryPromp(board_size = self.playmanager.board.canvas.get_size(), center_position = self.center_screen)
        self.retry_blitted = False
        self.retry = False

        self.screen.blit(self.playmanager.board.canvas, self.playmanager.board.canvas.get_rect(center = self.center_screen))
        pygame.display.flip()

        self.mainloop = True
        while self.mainloop == True:
            self.events = pygame.event.get()
            pygame.event.clear()
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.retry = True
                if event.type == pygame.QUIT:
                    self.mainloop = False
            if not self.retry:
                self.playmanager.event_handler(self.events)
                self.screen.blit(self.playmanager.board.canvas, self.playmanager.board.canvas.get_rect(center = self.center_screen))
                pygame.display.flip()
            elif self.retry:
                if not self.retry_blitted:
                    self.screen.blit(self.retry_prompt.background, self.playmanager.board.canvas.get_rect(center = self.center_screen))
                    self.screen.blit(self.retry_prompt.yes_highlight, self.retry_prompt.yes_highlight.get_rect(center = self.center_screen))
                    self.retry_blitted = True
                self.choice = self.retry_prompt.event_handler(events = self.events, screen = self.screen)
                pygame.display.flip()
                if self.choice == 'YES':
                    self.retry = False
                    self.retry_blitted = False
                    self.playmanager.reset_all()
                    pygame.display.flip()
                elif self.choice == 'NO':
                    self.retry_blitted = False
                    self.retry = False
                    self.mainloop = False
        pygame.display.quit()
        self.run_menu()

    def run_simulator(self):
        self.root.destroy()
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.center_screen = (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2)
        pygame.mouse.set_visible(False)
        import themes
        self.playmanager = simulator.PlayManager(boss = self, theme = themes.theme_list['NES_Tetris'], settings = self.menu_manager.settings_menu.setting_output)
        self.retry_prompt = RetryPromp(board_size = self.playmanager.board.canvas.get_size(), center_position = self.center_screen)
        self.retry_blitted = False

        self.screen.blit(self.playmanager.board.canvas, self.playmanager.board.canvas.get_rect(center = self.center_screen))
        pygame.display.flip()

        self.mainloop = True
        self.topout_check = False
        self.begin_time = time.clock()
        while self.mainloop == True:
            self.pressed_keys = pygame.key.get_pressed()
            pygame.event.clear()

            if self.pressed_keys[pygame.K_ESCAPE] == True:
                self.topout_check = True
            if pygame.event.get(pygame.QUIT):
                self.mainloop = False
            self.playmanager.event_handler(pressed_keys = self.pressed_keys)

            self.frame_time = time.clock() - self.begin_time
            if self.frame_time >= 1/self.playmanager.fps and self.topout_check == False:
                self.begin_time = time.clock()
                self.topout_check = self.playmanager.run_frame(self.frame_time)
                self.screen.blit(self.playmanager.board.canvas, self.playmanager.board.canvas.get_rect(center = self.center_screen))
                pygame.display.flip()

            elif self.topout_check:
                if not self.retry_blitted:
                    self.screen.blit(self.retry_prompt.background, self.playmanager.board.canvas.get_rect(center = self.center_screen))
                    self.screen.blit(self.retry_prompt.yes_highlight, self.retry_prompt.yes_highlight.get_rect(center = self.center_screen))
                    self.retry_blitted = True
                self.choice = self.retry_prompt.event_handler(pressed_buttons = self.pressed_keys, screen = self.screen)
                pygame.display.flip()
                if self.choice == 'YES':
                    self.topout_check = False
                    self.retry_blitted = False
                    self.playmanager.reset_all()
                    pygame.display.flip()
                elif self.choice == 'NO':
                    self.retry_blitted = False
                    self.topout_check = False
                    self.mainloop = False
        pygame.display.quit()
        self.run_menu()

class RetryPromp:
    def __init__(self, board_size, center_position):
        self.center = center_position
        self.background = pygame.Surface(board_size)
        self.background.fill((50, 50, 50))
        self.background.set_alpha(200)
        self.yes_highlight = pygame.image.load(os.path.join('images', 'retry_text_yes.png'))
        self.no_highlight = pygame.image.load(os.path.join('images', 'retry_text_no.png'))
        self.selected = 'YES'

    def event_handler(self, screen, pressed_buttons = False, events = False):
        if pressed_buttons:
            if pressed_buttons[pygame.K_LEFT]:
                self.selected = 'NO'
                screen.blit(self.no_highlight, self.yes_highlight.get_rect(center = self.center))
            elif pressed_buttons[pygame.K_RIGHT]:
                self.selected = 'YES'
                screen.blit(self.yes_highlight, self.yes_highlight.get_rect(center = self.center))
            if pressed_buttons[pygame.K_RETURN]:
                return self.selected
        elif events:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.selected = 'NO'
                        screen.blit(self.no_highlight, self.yes_highlight.get_rect(center = self.center))
                    elif event.key == pygame.K_RIGHT:
                        self.selected = 'YES'
                        screen.blit(self.yes_highlight, self.yes_highlight.get_rect(center = self.center))
                    if event.key == pygame.K_RETURN:
                        return self.selected

boss = BigBoss()
