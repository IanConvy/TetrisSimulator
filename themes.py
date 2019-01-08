import pygame
import os

pygame.init()

theme_list = {

    'NES_Tetris': {
        'board': {
            'cover': pygame.image.load(os.path.join('images', 'tetrisboard.png')).convert(),
            'size': (1035, 899)
            },
        'playfield': {
            'cover': pygame.Surface((320, 640)).convert(),
            'dimmensions': (10, 20),
            'location': pygame.Rect(390, 162, 320, 640),
            'block_size': (32, 32)
            },
        'score': {
            'cover': pygame.Surface((197, 33)).convert(),
            'location': pygame.Rect(777, 250, 197, 33),
            'font': pygame.font.SysFont('Classic NES Font Regular', 32),
            'max_digits': 6
            },
        'line_count': {
            'cover': pygame.Surface((335, 43)).convert(),
            'location': pygame.Rect(390, 62, 335, 43),
            'font': pygame.font.SysFont('Classic NES Font Regular', 36),
            'max_digits': 3
            },
        'level_display': {
            },
        'info': {
            'cover': pygame.Surface((280, 332)).convert(),
            'location': pygame.Rect(58, 246, 280, 332),
            'font': pygame.font.SysFont('Classic NES Font Regular', 26)
            },
        'piece_preview': {
            'cover': pygame.Surface((130, 74)).convert(),
            'location': pygame.Rect(774,  442, 130, 74),
            },
        'cleared_lines': {
            'cover': pygame.Surface((280, 185)).convert(),
            'location': pygame.Rect(60, 624, 280, 185),
            'font': pygame.font.SysFont('Classic NES Font Regular', 22),
            'max_digits': 2
            },
        'select_piece': {
            'cover': pygame.Surface((280, 332)).convert(),
            'location': pygame.Rect(58, 246, 280, 332),
            'font': pygame.font.SysFont('Classic NES Font Regular', 56)
            },
        'block_covers': {
            'yellowblock': pygame.image.load(os.path.join('images', 'yellowblock.png')).convert_alpha(),
            'redblock': pygame.image.load(os.path.join('images', 'redblock.png')).convert_alpha(),
            'whiteblock': pygame.image.load(os.path.join('images', 'whiteblock.png')).convert_alpha(),
            'emptyblock': pygame.image.load(os.path.join('images', 'blackblock.png')).convert_alpha(),
            'greyblock': pygame.image.load(os.path.join('images', 'greyblock.png')).convert_alpha()
            },
        'piece_covers': {
            'L-piece right': pygame.image.load(os.path.join('images', 'yellowblock.png')).convert_alpha(),
            'L-piece left': pygame.image.load(os.path.join('images', 'redblock.png')).convert_alpha(),
            'S-piece right': pygame.image.load(os.path.join('images', 'redblock.png')).convert_alpha(),
            'S-piece left': pygame.image.load(os.path.join('images', 'yellowblock.png')).convert_alpha(),
            'I-piece': pygame.image.load(os.path.join('images', 'whiteblock.png')).convert_alpha(),
            'T-piece': pygame.image.load(os.path.join('images', 'whiteblock.png')).convert_alpha(),
            'Sq-piece': pygame.image.load(os.path.join('images', 'whiteblock.png')).convert_alpha(),
            'block': pygame.image.load(os.path.join('images', 'greyblock.png')).convert_alpha()
            }
        }
    }
