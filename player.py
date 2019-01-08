import pygame
import board_display
import themes
import pieces
import os
import json

class Player:
    def __init__(self, log_path):
        pygame.init()
        self.log = open(log_path, 'r')
        self.board = board_display.Board(piece_list = pieces.standard_list, theme = themes.theme_list['NES_Tetris'])
        self.frame = 0
        self.fps = 60
        self.run()

    def run(self):
        for line 
