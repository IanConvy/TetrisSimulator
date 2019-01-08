import pygame
import board_display
import grid
import pieces
import record
import copy

class PlayManager:
    def __init__(self, boss, settings, theme):
        pygame.init()
        self.title = 'Tetris Simulator'
        self.boss = boss
        self.settings = settings
        self.theme = theme
        self.reset_all()

    def set_constants(self):
        self.height = self.settings['height']
        self.width = self.settings['width']
        self.fps = self.settings['fps']
        self.gravity_set = self.settings['gravity_set']
        self.first_delay = self.settings['first_delay']
        self.das_limit = self.settings['das_limit']
        self.das_floor = self.settings['das_floor']
        self.entry_delay = self.settings['entry_delay']
        self.piece_list = self.settings['piece_list']
        self.drop_site = self.settings['drop_site']
        self.line_clear_points = self.settings['line_clear_points']

    def reset_flags(self):
        self.a_held = False
        self.s_held = False
        self.left_held = False
        self.right_held = False
        self.frozen = False
        self.soft_drop = False
        self.do_cw = False
        self.do_ccw = False
        self.do_left = False
        self.do_right = False
        self.clear_das = False
        self.das_boost = False
        self.topout = False
        self.piece_moved = False
        self.need_blit = False
        self.row_cleared = False

    def reset_counters(self):
        self.frozen_frames = 0
        self.drop_frames = 0
        self.das_frames = 0
        self.first_frames = 0
        self.row_clear_frames = 0
        self.line_count = 0
        self.score = 0
        self.topout_counter = 0
        self.total_frames = 0
        self.line_breakdown = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
            }

    def reset_all(self):
        self.set_constants()
        self.reset_flags()
        self.reset_counters()
        self.gravity = self.gravity_set
        self.changed_blocks = {}
        self.board = board_display.Board(piece_list = self.piece_list, theme = self.theme)
        self.grid = grid.Grid((self.width, self.height))
        self.current_piece = pieces.Piece(pieces.random_piece(self.piece_list), self.drop_site)
        self.next_piece = pieces.random_piece(self.piece_list)
        self.board.piece_preview.update(self.next_piece)
        self.current_piece.copy_to_dict(self.changed_blocks)
        self.logger = record.Logger()
        self.need_blit = True

    def get_entry_delay(self, piece):
        center_offset = self.piece_list[piece.name]['center_offset'][piece.orient]
        entry_delay = self.entry_delay[piece.center[1] + center_offset]
        return entry_delay

    def try_shift(self, piece, direction):
        piece.shift(direction)
        check = self.grid.collision_check(piece.coords)
        if check:
            piece.shift((-direction[0], -direction[1]))
        return check

    def try_rotate(self, piece, direction):
        piece.rotate(direction)
        check = self.grid.collision_check(piece.coords)
        if check:
            piece.rotate(-direction)
        return check

    def record_state(self):
        record = {
            'frame': self.total_frames,
            'DAS': self.das_frames,
            'score': self.score,
            'line_count': self.line_count,
            'line_breakdown': {str(x):self.line_breakdown[x] for x in self.line_breakdown.keys()},
            'next_piece': self.next_piece,
            'blocks': {str(coord):self.changed_blocks[coord] for coord in self.changed_blocks.keys()}
            }
        return record

    def event_handler(self, pressed_keys):
        self.pressed = pressed_keys
        if self.pressed[pygame.K_a] == True:
            if self.a_held == False and self.s_held == False:
                self.a_held = True
                self.do_ccw = True
        else: self.a_held = False

        if self.pressed[pygame.K_s] == True:
            if self.s_held == False and self.a_held == False:
                self.s_held = True
                self.do_cw = True
        else: self.s_held = False

        if self.pressed[pygame.K_LEFT] == True:
            if self.left_held == False and self.right_held == False:
                self.left_held = True
                self.do_left = True
                self.clear_das = True
        else: self.left_held = False

        if self.pressed[pygame.K_RIGHT] == True:
            if self.right_held == False and self.left_held == False:
                self.right_held = True
                self.do_right = True
                self.clear_das = True
        else: self.right_held = False

        if self.pressed[pygame.K_DOWN] == True:
            self.soft_drop = True
        else: self.soft_drop = False

    def run_frame(self, frame_time):
        self.piece_shadow = copy.copy(self.current_piece)
        self.frame_time = frame_time
        self.total_frames += 1
        if not self.frozen and not self.topout:

            if self.first_frames < self.first_delay and not self.soft_drop:
                self.first_frames += 1

            else:
                self.first_frames = self.first_delay
                self.drop_frames += 1

            if self.do_cw:
                if not self.try_rotate(self.current_piece, 1):
                    self.piece_moved = True
                self.do_cw = False

            elif self.do_ccw:
                if not self.try_rotate(self.current_piece, -1):
                    self.piece_moved = True
                self.do_ccw = False

            if self.do_left:
                if not self.try_shift(self.current_piece, (-1, 0)):
                    self.piece_moved = True
                else:
                    self.das_boost = True
                self.do_left = False

            elif self.do_right:
                if not self.try_shift(self.current_piece, (1, 0)):
                    self.piece_moved = True
                else:
                    self.das_boost = True
                self.do_right = False

            elif self.left_held and self.das_frames >= self.das_limit:
                self.das_frames = self.das_floor
                if not self.try_shift(self.current_piece, (-1, 0)):
                    self.piece_moved = True
                else:
                    self.das_boost = True

            elif self.right_held and self.das_frames >= self.das_limit:
                self.das_frames = self.das_floor
                if not self.try_shift(self.current_piece, (1, 0)):
                    self.piece_moved = True
                else:
                    self.das_boost = True

            if self.left_held and self.das_frames < self.das_limit:
                self.das_frames += 1

            elif self.right_held and self.das_frames < self.das_limit:
                self.das_frames += 1

            if self.clear_das:
                self.das_frames = 0
                self.clear_das = False

            if self.das_boost:
                self.das_frames = self.das_limit
                self.das_boost = False

            if self.soft_drop:
                self.gravity = 2
            else: self.gravity = self.gravity_set

            if self.drop_frames >= self.gravity:
                self.drop_frames = 0
                if not self.try_shift(self.current_piece, (0, 1)):
                    self.piece_moved = True
                else:
                    self.frozen = True
                    self.frozen_frames = 0
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
                        self.row_cleared = True

        elif self.frozen and not self.topout:
            self.do_cw = False
            self.do_ccw = False
            self.do_left = False
            self.do_right = False
            self.clear_das = False
            self.frozen_frames += 1
            if self.row_cleared:
                self.row_clear_frames += 1
                if self.row_clear_frames == 7:
                    for row in self.row_list:
                        self.changed_blocks[(self.drop_site[0], row)] = False
                        self.changed_blocks[(self.drop_site[0] - 1, row)] = False
                    self.need_blit = True

                elif self.row_clear_frames == 12:
                    for row in self.row_list:
                        self.changed_blocks[(self.drop_site[0] + 1, row)] = False
                        self.changed_blocks[(self.drop_site[0] - 2, row)] = False
                    self.need_blit = True

                elif self.row_clear_frames == 17:
                    for row in self.row_list:
                        self.changed_blocks[(self.drop_site[0] + 2, row)] = False
                        self.changed_blocks[(self.drop_site[0] - 3, row)] = False
                    self.need_blit = True

                elif self.row_clear_frames == 22:
                    for row in self.row_list:
                        self.changed_blocks[(self.drop_site[0] + 3, row)] = False
                        self.changed_blocks[(self.drop_site[0] - 4, row)] = False
                    self.need_blit = True

                elif self.row_clear_frames == 26:
                    for row in self.row_list:
                        self.changed_blocks[(self.drop_site[0] + 4, row)] = False
                        self.changed_blocks[(self.drop_site[0] - 5, row)] = False
                    self.need_blit = True

                elif self.row_clear_frames == 17 + self.get_entry_delay(self.current_piece):
                    self.grid.copy_to_dict(block_dict = self.changed_blocks, top = 0, bottom = max(self.row_list), left = 0, right = self.width - 1)
                    self.need_blit = True
                    self.row_clear_frames = 0
                    self.row_cleared = False

            elif not self.row_cleared and self.frozen_frames >= self.get_entry_delay(self.current_piece):
                self.frozen = False
                self.frozen_frames = 0
                self.current_piece = pieces.Piece(self.next_piece, self.drop_site)
                self.next_piece = pieces.random_piece(self.piece_list)
                self.current_piece.copy_to_dict(self.changed_blocks)
                self.topout = self.grid.collision_check(self.current_piece.coords)
                self.board.piece_preview.update(self.next_piece)
                self.need_blit = True

        self.frame_record = self.record_state()
        if self.piece_moved or self.need_blit:
            if self.piece_moved:
                self.piece_shadow.copy_to_dict(self.changed_blocks, clear = True)
                self.current_piece.copy_to_dict(self.changed_blocks)
            self.board.playfield.blit_from_name(self.changed_blocks)
            self.frame_record = self.record_state()
            self.changed_blocks = {}
            self.piece_moved = False
            self.need_blit = False

        self.board.info.update(fps = 1/self.frame_time, das_frames = self.das_frames)
        self.logger.log_frame(self.frame_record)
        return self.topout
