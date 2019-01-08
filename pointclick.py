import pygame
import os
import board_display
import grid
import pieces
import settings
import record

class PlayManager:
    def __init__(self, boss, settings, theme, center):
        pygame.init()
        self.title = 'Tetris Practice'
        self.center = center
        self.boss = boss
        self.settings = settings
        self.theme = theme
        self.allowed_block = pygame.image.load(os.path.join('images', 'allowedblock.png')).convert_alpha()
        self.disallowed_block = pygame.image.load(os.path.join('images', 'disallowedblock.png')).convert_alpha()
        self.guide_block = pygame.image.load(os.path.join('images', 'guideblock.png')).convert_alpha()
        self.reset_all()

    def set_constants(self):
        self.height = self.settings['height']
        self.width = self.settings['width']
        self.piece_list = self.settings['piece_list']
        self.line_clear_points = self.settings['line_clear_points']
        self.gravity = self.settings['gravity_set']
        self.drop_site = self.settings['drop_site']
        self.das_limit = self.settings['das_limit']
        self.das_floor = self.settings['das_floor']

    def reset_counters(self):
        self.line_count = 0
        self.score = 0
        self.line_breakdown= {
            1: 0,
            2: 0,
            3: 0,
            4: 0
            }

    def reset_all(self):
        self.set_constants()
        self.reset_counters()
        self.board = board_display.Board(piece_list = self.piece_list, theme = self.theme, pointclick = True)
        self.grid = grid.Grid((self.width, self.height))
        self.current_piece = pieces.Piece(pieces.random_piece(self.piece_list), center = (0, 0))
        self.next_piece = pieces.random_piece(self.piece_list)
        self.board.piece_preview.update(self.next_piece)
        self.guides = {}
        self.create_guides(self.current_piece, self.guides)
        self.board.playfield.blit_to_background(self.guides, self.grid.copy_to_dict(block_dict = {}, whole = True))
        self.mouse_coord = (-1, -1)
        self.record = record.Record()
        self.record.coherent_records_update(self.grid.grid, self.line_breakdown, self.line_count, self.score, None)
        self.queue = {'current': self.current_piece.name, 'next': self.next_piece}
        self.piece_selected = self.board.select_piece.mouse_click(self.board.select_piece.buttons['random'].location)

    def highlight_to_dict(self, coords, block_dict, allowed = True):
        if allowed:
            cover = self.allowed_block
        else:
            cover = self.disallowed_block
        for coord in coords:
            block_dict[coord] = cover
        return block_dict

    def unhighlight_to_dict(self, coords, block_dict):
        for (x, y) in coords:
            block_dict[(x, y)] = self.grid.grid[y][x]
        return block_dict

    def assign_current_piece(self):
        if self.piece_selected == 'random':
            if self.record.move == self.record.max_move:
                current_piece = pieces.Piece(self.queue['current'], self.mouse_coord)
            else:
                current_piece = pieces.Piece(self.record.retrieve_piece(self.record.move + 1), self.mouse_coord)
        else:
            current_piece = pieces.Piece(self.piece_selected, self.mouse_coord)
        return current_piece

    def assign_next_piece(self):
        if self.piece_selected == 'random':
            if self.record.move == self.record.max_move:
                next_piece = self.queue['next']
            elif self.record.move == self.record.max_move - 1:
                next_piece = self.queue['current']
            else:
                next_piece = self.record.retrieve_piece(self.record.move + 2)
        else:
            next_piece = self.piece_selected
        return next_piece

    def check_queue(self, queue):
        if self.record.move == self.record.max_move:
            if self.piece_selected == 'random':
                queue['current'] = queue['next']
                queue['next'] = pieces.random_piece(self.piece_list)
            else:
                queue['current'] = self.piece_selected
                queue['next'] = self.piece_selected

    def translate_record(self):
        self.new_state = self.record.retrieve_state()
        self.grid.grid = self.new_state['grid']
        self.line_breakdown = self.new_state['line_breakdown']
        self.line_count = self.new_state['line_count']
        self.score = self.new_state['score']
        self.next_piece = self.assign_next_piece()
        self.current_piece = self.assign_current_piece()
        self.create_guides(self.current_piece, self.guides)
        self.board.playfield.blit_to_background(self.guides, self.grid.copy_to_dict(block_dict = {}, whole = True))
        self.board.piece_preview.update(self.next_piece)
        self.board.line_count.update(self.line_count)
        self.board.score.update(self.score)
        self.board.cleared_lines.update(self.line_breakdown)
        self.board.playfield.blit_from_name(self.grid.copy_to_dict(block_dict = {}, whole = True))

    def create_guides(self, piece, guide_dict):
        for coord in list(guide_dict.keys()):
            guide_dict[coord] = False
        test_set = set()
        for (x, y) in pieces.get_coords({'center': (0, 0), 'name': piece.name, 'orient': piece.orient}):
            test_set.add(x)
        left_offset = min(test_set)
        right_offset = max(test_set)
        coord_set = set()
        coord_set.update(pieces.get_coords({'center': self.drop_site, 'name': piece.name, 'orient': piece.orient}))
        for frame_left in range(1 + (self.drop_site[0] - 1 + left_offset) * (self.das_limit - self.das_floor)):
            center = (-1 + self.drop_site[0] - (frame_left // (self.das_limit - self.das_floor)), self.drop_site[1] + (1 + frame_left) // self.gravity)
            print(center)
            coord_set.update(pieces.get_coords({'center': center, 'name': piece.name, 'orient': piece.orient}))
        for frame_right in range(1 + (self.width - 1 - self.drop_site[0] - 1 - right_offset) * (self.das_limit - self.das_floor)):
            center = (1 + self.drop_site[0] + (frame_right // (self.das_limit - self.das_floor)), self.drop_site[1] + (1 + frame_right) // self.gravity)
            print(center)
            coord_set.update(pieces.get_coords({'center': center, 'name': piece.name, 'orient': piece.orient}))
        for coord in coord_set:
            guide_dict[coord] = self.guide_block

    def event_handler(self, events):
        self.events = events
        for event in self.events:

            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_rect = pygame.Rect((event.pos[0] - self.board.canvas.get_rect(center = self.center).left, event.pos[1]), (1, 1))
                if self.board.playfield.location.contains(self.mouse_rect):
                    self.old_mouse_coord = self.mouse_coord
                    self.mouse_coord = self.board.playfield.pixel_to_coord((event.pos[0] - self.board.canvas.get_rect(center = self.center).left, event.pos[1]))
                    if self.mouse_coord != self.old_mouse_coord:
                        self.board.playfield.blit_from_name(self.unhighlight_to_dict(self.current_piece.coords, block_dict = {}))
                        self.current_piece.center = self.mouse_coord
                        self.current_piece.assign_coords()
                        if self.grid.collision_check(self.current_piece.coords):
                            self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = False))
                            self.allowed = False
                        else:
                            self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = True))
                            self.allowed = True
                else:
                     self.board.playfield.blit_from_name(self.unhighlight_to_dict(self.current_piece.coords, block_dict = {}))
                     self.mouse_coord = (-1, -1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_rect = pygame.Rect((event.pos[0] - self.board.canvas.get_rect(center = self.center).left, event.pos[1]), (1, 1))
                if event.button == 1:
                    if self.board.playfield.location.contains(self.mouse_rect) and self.allowed:
                        self.allowed = False
                        self.grid.grid_piece(self.current_piece)
                        self.row_list = self.grid.get_filled_rows()
                        self.total_rows = len(self.row_list)
                        if self.row_list:
                            self.line_count += self.total_rows
                            self.score += self.line_clear_points[self.total_rows]
                            self.line_breakdown[self.total_rows] += 1
                            self.board.line_count.update(self.line_count)
                            self.board.score.update(self.score)
                            self.board.cleared_lines.update(self.line_breakdown)
                            self.grid.row_clear(self.row_list)
                            self.board.playfield.blit_from_name(self.unhighlight_to_dict(self.current_piece.coords, block_dict = {}))
                            self.board.playfield.blit_from_name(self.grid.copy_to_dict(block_dict = {}, top = 0, bottom = max(self.row_list), left = 0, right = self.drop_site[0] - 1))
                        else:
                            self.board.playfield.blit_from_name(self.current_piece.copy_to_dict(block_dict = {}))
                        self.check_queue(self.queue)
                        self.record.shift(1)
                        self.record.coherent_records_update(self.grid.grid, self.line_breakdown, self.line_count, self.score, self.current_piece.name)
                        self.current_piece = self.assign_current_piece()
                        self.next_piece = self.assign_next_piece()
                        self.board.piece_preview.update(self.next_piece)
                        self.create_guides(self.current_piece, self.guides)
                        self.board.playfield.blit_to_background(self.guides, self.grid.copy_to_dict(block_dict = {}, whole = True))
                    elif self.board.select_piece.location.contains(self.mouse_rect):
                        self.piece_selected = self.board.select_piece.mouse_click(self.mouse_rect)
                        if self.piece_selected and self.piece_selected != 'random':
                            self.current_piece = pieces.Piece(self.piece_selected, self.mouse_coord)
                            self.next_piece = self.piece_selected
                        elif self.piece_selected == 'random':
                            self.current_piece = pieces.Piece(pieces.random_piece(self.piece_list), self.mouse_coord)
                            self.next_piece = pieces.random_piece(self.piece_list)
                        self.create_guides(self.current_piece, self.guides)
                        self.board.playfield.blit_to_background(self.guides, self.grid.copy_to_dict(block_dict = {}, whole = True))
                        self.board.piece_preview.update(self.next_piece)

                elif event.button == 3 and self.board.playfield.location.contains(self.mouse_rect):
                    self.board.playfield.blit_from_name(self.unhighlight_to_dict(self.current_piece.coords, block_dict = {}))
                    self.current_piece.rotate(1)
                    self.create_guides(self.current_piece, self.guides)
                    self.board.playfield.blit_to_background(self.guides, self.grid.copy_to_dict(block_dict = {}, whole = True))
                    if self.grid.collision_check(self.current_piece.coords):
                        self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = False))
                    else:
                        self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = True))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and self.board.playfield.location.contains(self.mouse_rect):
                    self.board.playfield.blit_from_name(self.unhighlight_to_dict(self.current_piece.coords, block_dict = {}))
                    self.current_piece.rotate(-1)
                    self.create_guides(self.current_piece, self.guides)
                    self.board.playfield.blit_to_background(self.guides, self.grid.copy_to_dict(block_dict = {}, whole = True))
                    if self.grid.collision_check(self.current_piece.coords):
                        self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = False))
                    else:
                        self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = True))

                elif event.key == pygame.K_s and self.board.playfield.location.contains(self.mouse_rect):
                    self.board.playfield.blit_from_name(self.unhighlight_to_dict(self.current_piece.coords, block_dict = {}))
                    self.current_piece.rotate(1)
                    self.create_guides(self.current_piece, self.guides)
                    self.board.playfield.blit_to_background(self.guides, self.grid.copy_to_dict(block_dict = {}, whole = True))
                    if self.grid.collision_check(self.current_piece.coords):
                        self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = False))
                    else:
                        self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = True))

                elif event.key == pygame.K_z:
                    if self.record.move > 0:
                        self.piece_selected = self.board.select_piece.mouse_click(self.board.select_piece.buttons['random'].location)
                        self.record.shift(-1)
                        self.translate_record()
                        if self.grid.collision_check(self.current_piece.coords):
                            self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = False))
                            self.allowed = False
                        else:
                            self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = True))
                            self.allowed = True

                elif event.key == pygame.K_x:
                    if self.record.move < max(self.record.move_record.keys()):
                        self.piece_selected = self.board.select_piece.mouse_click(self.board.select_piece.buttons['random'].location)
                        self.record.shift(1)
                        self.translate_record()
                        if self.grid.collision_check(self.current_piece.coords):
                            self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = False))
                            self.allowed = False
                        else:
                            self.board.playfield.blit_blocks(self.highlight_to_dict(self.current_piece.coords, block_dict = {}, allowed = True))
                            self.allowed = True
