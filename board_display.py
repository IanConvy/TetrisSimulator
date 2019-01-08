import pygame

class DisplayObject:
    def __init__(self, board, theme):
        self.board = board
        self.location = theme['location']
        self.blank = pygame.Surface(self.location.size).convert()
        self.blank.blit(theme['cover'], (0, 0))
        self.canvas = pygame.Surface(self.location.size).convert()
        self.canvas.blit(theme['cover'], (0, 0))

class Board:
    def __init__(self, piece_list, theme, pointclick = False):
        self.size = theme['board']['size']
        self.canvas = pygame.Surface(self.size)
        self.canvas.blit(theme['board']['cover'], (0, 0))
        self.playfield = Playfield(board = self, playfield_theme = theme['playfield'], piece_covers = theme['piece_covers'])
        self.score = ScoreCount(board = self, score_theme = theme['score'])
        self.line_count = LineCount(board = self, line_count_theme = theme['line_count'])
        self.level = LevelDisplay(board = self, level_display_theme = theme['level_display'])
        self.cleared_lines = ClearedLines(board = self, cleared_lines_theme = theme['cleared_lines'])
        self.piece_displays = {}
        for piece in piece_list.keys():
            self.piece_displays[piece_list[piece]['name']] = self.create_piece_display(coord = piece_list[piece]['shape'][0], cover = theme['piece_covers'][piece])
            self.piece_displays[piece_list[piece]['name']].convert()
        self.piece_preview = PiecePreview(board = self, piece_displays = self.piece_displays, piece_preview_theme = theme['piece_preview'])
        if not pointclick:
            self.info = InfoDisplay(board = self, info_theme = theme['info'])
        else:
            self.select_piece = SelectPiece(board = self, select_piece_theme = theme['select_piece'], piece_displays = self.piece_displays)

    def create_piece_display(self, coord, cover):
        initial_surface = pygame.Surface((1000, 1000))
        block_list = []
        canvas = pygame.Rect(500, 500, 1, 1)
        for (x, y) in coord:
            block = pygame.Rect(500 + 32 * x, 500 + 32 * y, 32, 32)
            block_list.append(block)
            canvas = canvas.union(block)
            initial_surface.blit(cover, block)
        final_image = pygame.Surface(canvas.size)
        final_image.blit(initial_surface, (0, 0), area = canvas)
        return final_image


class Playfield(DisplayObject):
    def __init__(self, board, playfield_theme, piece_covers):
        DisplayObject.__init__(self, board, playfield_theme)
        self.theme = playfield_theme
        self.piece_covers = piece_covers
        self.dim = playfield_theme['dimmensions']
        self.block_size = playfield_theme['block_size']
        self.blockgrid = {}
        for y in range(self.dim[1]):
            self.blockgrid[y] = {}
            for x in range(self.dim[0]):
                self.blockgrid[y][x] = Block(coord = (x, y), size = self.block_size)
        self.blockgrid[self.dim[1]] = {}
        for x in range(self.dim[0]):
            self.blockgrid[self.dim[1]][x] = Block(coord = (x, self.dim[1]), size = self.block_size)
        self.board.canvas.blit(self.canvas, self.location)


    def blit_blocks(self, coord_cover):
        for (x, y) in coord_cover.keys():
            try:
                if coord_cover[(x, y)]:
                    self.canvas.blit(coord_cover[(x, y)], (self.blockgrid[y][x].x, self.blockgrid[y][x].y))
                else:
                    self.canvas.blit(self.blank, (self.blockgrid[y][x].x, self.blockgrid[y][x].y), area = (self.blockgrid[y][x].x, self.blockgrid[y][x].y, self.block_size[0], self.block_size[1]))
            except KeyError: pass
        self.board.canvas.blit(self.canvas, self.location)

    def blit_from_name(self, coord_name):
        coord_cover = {}
        for coord in coord_name.keys():
            if coord_name[coord]:
                coord_cover[coord] = self.piece_covers[coord_name[coord]]
            else:
                coord_cover[coord] = False
        self.blit_blocks(coord_cover)

    def pixel_to_coord(self, pixel):
        relative_position = (pixel[0] - self.location.left, pixel[1] - self.location.top)
        coord = (relative_position[0] // self.block_size[0], relative_position[1] // self.block_size[1])
        return coord

    def blit_to_background(self, coord_cover, grid):
        for (x, y) in coord_cover.keys():
            try:
                if coord_cover[(x, y)]:
                    self.blank.blit(coord_cover[(x, y)], (self.blockgrid[y][x].x, self.blockgrid[y][x].y))
                else:
                    self.blank.blit(self.theme['cover'], (self.blockgrid[y][x].x, self.blockgrid[y][x].y), area = (self.blockgrid[y][x].x, self.blockgrid[y][x].y, self.block_size[0], self.block_size[1]))
            except KeyError: pass
        self.canvas.blit(self.blank, (0, 0))
        self.blit_from_name(grid)

class Block(pygame.Rect):
    def __init__(self, coord, size):
        pygame.Rect.__init__(self, size[0] * coord[0], size[1] * coord[1], size[0], size[1])

class ScoreCount(DisplayObject):
    def __init__(self, board, score_theme):
        DisplayObject.__init__(self, board, score_theme)
        self.font = score_theme['font']
        self.max_digits = score_theme['max_digits']
        self.text = self.font.render('0' * self.max_digits, False, (250, 250, 250))
        self.canvas.blit(self.text, (0, 0))
        self.board.canvas.blit(self.canvas, self.location)

    def update(self, score):
        self.canvas.blit(self.blank, (0, 0))
        self.text = self.font.render('{0:06}'.format(score), False, (250, 250, 250))
        self.canvas.blit(self.text, (0, 0))
        self.board.canvas.blit(self.canvas, self.location)

class LineCount(DisplayObject):
    def __init__(self, board, line_count_theme):
        DisplayObject.__init__(self, board, line_count_theme)
        self.font = line_count_theme['font']
        self.max_digits = line_count_theme['max_digits']
        self.text = self.font.render('LINES-'+'0' * 3, False, (250, 250, 250))
        self.canvas.blit(self.text, (0, 0))
        self.board.canvas.blit(self.canvas, self.location)

    def update(self, lines):
        self.canvas.blit(self.blank, (0, 0))
        self.text = self.font.render('LINES-{0:03d}'.format(lines), False, (250, 250, 250))
        self.canvas.blit(self.text, (0, 0))
        self.board.canvas.blit(self.canvas, self.location)

class LevelDisplay(DisplayObject):
    def __init__(self, board, level_display_theme): pass

class InfoDisplay(DisplayObject):
    def __init__(self, board, info_theme):
        DisplayObject.__init__(self, board, info_theme)
        self.font = info_theme['font']
        self.board.canvas.blit(self.canvas, self.location)

    def update(self, fps, das_frames):
        self.canvas.blit(self.blank, (0, 0))
        self.fps_text = self.font.render('FPS - {0:.0f}'.format(fps), False, (250, 250, 250))
        self.das_text = self.font.render('DAS - {0:02}'.format(das_frames), False, (250, 250, 250))
        #self.frozen_frames_text = self.font.render('FROZE - {0:02}'.format(frozen_frames), False, (250, 250, 250))
        self.canvas.blit(self.fps_text, self.fps_text.get_rect(center = (self.location.size[0]/2, 30)))
        self.canvas.blit(self.das_text, self.das_text.get_rect(center = (self.location.size[0]/2, 80)))
        #self.canvas.blit(self.frozen_frames_text, self.frozen_frames_text.get_rect(center = (self.location.size[0]/2, 130)))
        self.board.canvas.blit(self.canvas, self.location)

class PiecePreview(DisplayObject):
    def __init__(self, board, piece_displays, piece_preview_theme):
        DisplayObject.__init__(self, board, piece_preview_theme)
        self.piece_displays = piece_displays
        self.board.canvas.blit(self.canvas, self.location)

    def update(self, piece_name):
        self.canvas.blit(self.blank, (0, 0))
        self.newpiece = self.piece_displays[piece_name]
        self.canvas.blit(self.newpiece, self.newpiece.get_rect(center = (self.location.size[0]/2, self.location.size[1]/2)))
        self.board.canvas.blit(self.canvas, self.location)

class ClearedLines(DisplayObject):
    def __init__(self, board, cleared_lines_theme):
        DisplayObject.__init__(self, board, cleared_lines_theme)
        self.font = cleared_lines_theme['font']
        self.max_digits = cleared_lines_theme['max_digits']
        self.update({1: 0, 2: 0, 3: 0, 4: 0})

    def update(self, line_breakdown):
        self.canvas.blit(self.blank, (0, 0))
        self.single_text = self.font.render('SINGLE - {0:02}'.format(line_breakdown[1]), False, (250, 250 ,250))
        self.double_text = self.font.render('DOUBLE - {0:02}'.format(line_breakdown[2]), False, (250, 250 ,250))
        self.triple_text = self.font.render('TRIPLE - {0:02}'.format(line_breakdown[3]), False, (250, 250 ,250))
        self.tetris_text = self.font.render('TETRIS - {0:02}'.format(line_breakdown[4]), False, (250, 250 ,250))
        self.canvas.blit(self.single_text, self.single_text.get_rect(center = (self.location.size[0]/2, 20)))
        self.canvas.blit(self.double_text, self.double_text.get_rect(center = (self.location.size[0]/2, 70)))
        self.canvas.blit(self.triple_text, self.triple_text.get_rect(center = (self.location.size[0]/2, 120)))
        self.canvas.blit(self.tetris_text, self.tetris_text.get_rect(center = (self.location.size[0]/2, 170)))
        self.board.canvas.blit(self.canvas, self.location)

class SelectPiece(DisplayObject):
    def __init__(self, board, piece_displays, select_piece_theme):
        DisplayObject.__init__(self, board, select_piece_theme)
        self.piece_displays = piece_displays
        self.font = select_piece_theme['font']
        self.buttons = {}
        button_number = -1
        for piece in sorted(self.piece_displays.keys()):
            button_number += 1
            location = self.piece_displays[piece].get_rect()
            location.top = 10 + 85 * (button_number // 2)
            location.left = 10 + 160 * (button_number % 2)
            self.buttons[piece] = PieceButton(piece, pygame.Rect(location.left + self.location.left, location.top + self.location.top, location.size[0], location.size[1]))
            self.canvas.blit(self.piece_displays[piece], location)
        random_character = self.font.render('?', False, (250, 250, 250))
        self.piece_displays['random'] = pygame.Surface(random_character.get_size())
        self.piece_displays['random'].blit(random_character, (0, 0))
        self.buttons['random'] = PieceButton('random', self.piece_displays['random'].get_rect(left = self.location.left + 180, top = self.location.top + 270))
        self.canvas.blit(self.piece_displays['random'], (180, 270))
        self.board.canvas.blit(self.canvas, self.location)

    def mouse_click(self, mouse_rect):
        selected_button = False
        for button in self.buttons.keys():
            if self.buttons[button].location.contains(mouse_rect):
                selected_button = button
                highlight = pygame.Surface((self.buttons[button].location.size[0] + 10, self.buttons[button].location.size[1] + 10))
                highlight.fill((250, 0, 0))
                self.canvas.blit(highlight, (self.buttons[button].location.left - self.location.left - 5, self.buttons[button].location.top - self.location.top - 5))
                self.canvas.blit(self.piece_displays[button], (self.buttons[button].location.left - self.location.left, self.buttons[button].location.top - self.location.top))
                self.board.canvas.blit(self.canvas, self.location)
                break
        if selected_button:
            for button in self.buttons.keys():
                if button != selected_button:
                    unhighlight = pygame.Surface((self.buttons[button].location.size[0] + 10, self.buttons[button].location.size[1] + 10))
                    self.canvas.blit(unhighlight, (self.buttons[button].location.left - self.location.left - 5, self.buttons[button].location.top - self.location.top - 5))
                    self.canvas.blit(self.piece_displays[button], (self.buttons[button].location.left - self.location.left, self.buttons[button].location.top - self.location.top))
                    self.board.canvas.blit(self.canvas, self.location)
        return selected_button

class PieceButton:
    def __init__(self, piece, location):
        self.piece = piece
        self.location = location
