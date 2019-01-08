import os
import json

class Record:
    def __init__(self):
        self.move_record = {0: {}}
        self.piece_record = {}
        self.move = 0
        self.max_move = 0

    def coherent_records_update(self, grid, line_breakdown, line_count, score, placed_piece):
        if self.move < self.max_move:
            if placed_piece != self.piece_record[self.move]:
                print('pieces not equal')
                self.max_move = self.move
                for x in list(self.piece_record.keys()):
                    if x > self.move:
                        self.piece_record.pop(x)
                        try:
                            self.move_record.pop(x)
                        except KeyError: pass
            elif self.move > max(self.move_record.keys()) or grid != self.move_record[self.move]['grid']:
                print('board not same')
                for x in list(self.move_record.keys()):
                    if x > self.move:
                        self.move_record.pop(x)
        self.log_state(grid, line_breakdown, line_count, score)
        self.log_piece(placed_piece)

    def log_state(self, grid, line_breakdown, line_count, score, move = -1):
        if move < 0:
            move = self.move
        self.move_record[move] = {}
        self.move_record[move]['grid'] = {y: grid[y].copy() for y in grid.keys()}
        self.move_record[move]['line_breakdown'] = line_breakdown.copy()
        self.move_record[move]['line_count'] = line_count
        self.move_record[move]['score'] = score

    def log_piece(self, piece_name, move = -1):
        if move < 0:
            move = self.move
        self.piece_record[move] = piece_name

    def retrieve_state(self, move = -1):
        state = {}
        if move < 0:
            move = self.move
        state['grid'] = {y: self.move_record[move]['grid'][y].copy() for y in self.move_record[move]['grid']}
        state['line_breakdown'] = self.move_record[move]['line_breakdown'].copy()
        state['line_count'] = self.move_record[move]['line_count']
        state['score'] = self.move_record[move]['score']
        return state

    def retrieve_piece(self, move = -1):
        if move < 0:
            move = self.move
        return self.piece_record[move]

    def shift(self, direction):
        self.move += direction
        print(self.move)
        if self.move > max(self.piece_record.keys()):
            self.max_move = self.move
            self.move_record[self.move] = {}

class Logger:
    def __init__(self, target = False):
        if target:
            self.log = target
        else:
            open(os.path.join('logs', 'log_1.txt'), 'w').close()
            self.log = open(os.path.join('logs', 'log_1.txt'), 'a+')

    def log_frame(self, frame_info):
        string = json.dumps(frame_info)
        self.log.write(string + '\n')
