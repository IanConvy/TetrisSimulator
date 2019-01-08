import pygame
import random

def random_piece(piece_list):
    piece_name = random.choice(list(piece_list.keys()))
    return piece_name

def get_coords(piece):
    piece_coord = [(x + piece['center'][0], y + piece['center'][1]) for (x, y) in all_pieces[piece['name']]['shape'][piece['orient']]]
    return piece_coord

class Piece:
    def __init__(self, piece_name, center, orient = 0):
        self.name = piece_name
        self.center = center
        self.orient =  orient
        self.assign_coords()

    def assign_coords(self):
        self.coords = [(x + self.center[0], y + self.center[1]) for (x, y) in all_pieces[self.name]['shape'][self.orient]]

    def shift(self, direction):
        self.center = (self.center[0] + direction[0], self.center[1] + direction[1])
        self.assign_coords()

    def rotate(self, direction):
        new_orient = self.orient + direction
        if new_orient == -1:
            new_orient = 3
        elif new_orient == 4:
            new_orient = 0
        self.orient = new_orient
        self.assign_coords()

    def copy_to_dict(self, block_dict, clear = False):
        if not clear:
            cover = self.name
        else:
            cover = False
        for coord in self.coords:
             block_dict[coord] = cover
        return block_dict

all_pieces = {
    'L-piece right': {
        'name': 'L-piece right',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            3 : [(0, 0 - 1), (0, 0), (0, 0 + 1), (0 + 1, 0 + 1)],
            0 : [(0 + 1, 0), (0, 0), (0 - 1, 0), (0 - 1, 0 + 1)],
            1 : [(0, 0 + 1), (0, 0), (0, 0 - 1), (0 - 1, 0 - 1)],
            2 : [(0 - 1, 0), (0, 0), (0 + 1, 0), (0 + 1, 0 - 1)]
        }
    },

    'L-piece left': {
        'name': 'L-piece left',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            1 : [(0, 0 - 1), (0, 0), (0, 0 + 1), (0 - 1, 0 + 1)],
            2 : [(0 + 1, 0), (0, 0), (0 - 1, 0), (0 - 1, 0 - 1)],
            3 : [(0, 0 + 1), (0, 0), (0, 0 - 1), (0 + 1, 0 - 1)],
            0 : [(0 - 1, 0), (0, 0), (0 + 1, 0), (0 + 1, 0 + 1)]
        }
    },

    'S-piece right': {
        'name': 'S-piece right',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            0 : [(0 + 1, 0), (0, 0), (0, 0 + 1), (0 - 1, 0 + 1)],
            1 : [(0, 0 - 1), (0, 0), (0 + 1, 0), (0 + 1, 0 + 1)],
            2 : [(0 + 1, 0), (0, 0), (0, 0 + 1), (0 - 1, 0 + 1)],
            3 : [(0, 0 - 1), (0, 0), (0 + 1, 0), (0 + 1, 0 + 1)]
        }
    },

    'S-piece left': {
        'name': 'S-piece left',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            0 : [(0 -1 , 0), (0, 0), (0, 0 + 1), (0 + 1, 0 + 1)],
            1 : [(0, 0 + 1), (0, 0), (0 + 1, 0), (0 + 1, 0 - 1)],
            2 : [(0 - 1, 0), (0, 0), (0, 0 + 1), (0 + 1, 0 + 1)],
            3 : [(0, 0 + 1), (0, 0), (0 + 1, 0), (0 + 1, 0 - 1)]
        }
    },

    'I-piece': {
        'name': 'I-piece',
        'center_offset': {
            0 : 0,
            1 : 1,
            2 : 0,
            3 : 1
            },
        'shape': {
            1 : [(0, 0 - 2), (0, 0), (0, 0 - 1), (0, 0 + 1)],
            2 : [(0 + 1, 0), (0, 0), (0 - 1, 0), (0 - 2, 0)],
            3 : [(0, 0 - 2), (0, 0), (0, 0 - 1), (0, 0 + 1)],
            0 : [(0 + 1, 0), (0, 0), (0 - 1, 0), (0 - 2, 0)]
        }
    },

    'T-piece': {
        'name': 'T-piece',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            2 : [(0, 0 - 1), (0 - 1, 0), (0, 0), (0 + 1, 0)],
            3 : [(0 + 1, 0), (0, 0 - 1), (0, 0), (0, 0 + 1)],
            0 : [(0, 0 + 1), (0 + 1, 0), (0, 0), (0 - 1, 0)],
            1 : [(0 - 1, 0), (0, 0 + 1), (0, 0), (0, 0 - 1)]
        }
    },

    'Sq-piece': {
        'name': 'Sq-piece',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            0 : [(0 - 1, 0), (0, 0), (0 - 1, 0 + 1), (0, 0 + 1)],
            1 : [(0 - 1, 0), (0, 0), (0 - 1, 0 + 1), (0, 0 + 1)],
            2 : [(0 - 1, 0), (0, 0), (0 - 1, 0 + 1), (0, 0 + 1)],
            3 : [(0 - 1, 0), (0, 0), (0 - 1, 0 + 1), (0, 0 + 1)]
        }
    },
    'block': {
        'name': 'block',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape':{
            0 : [(0, 0)],
            1 : [(0, 0)],
            2 : [(0, 0)],
            3 : [(0, 0)]
        }
    }
}

standard_list = {
    'L-piece right': {
        'name': 'L-piece right',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            3 : [(0, 0 - 1), (0, 0), (0, 0 + 1), (0 + 1, 0 + 1)],
            0 : [(0 + 1, 0), (0, 0), (0 - 1, 0), (0 - 1, 0 + 1)],
            1 : [(0, 0 + 1), (0, 0), (0, 0 - 1), (0 - 1, 0 - 1)],
            2 : [(0 - 1, 0), (0, 0), (0 + 1, 0), (0 + 1, 0 - 1)]
        }
    },

    'L-piece left': {
        'name': 'L-piece left',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            1 : [(0, 0 - 1), (0, 0), (0, 0 + 1), (0 - 1, 0 + 1)],
            2 : [(0 + 1, 0), (0, 0), (0 - 1, 0), (0 - 1, 0 - 1)],
            3 : [(0, 0 + 1), (0, 0), (0, 0 - 1), (0 + 1, 0 - 1)],
            0 : [(0 - 1, 0), (0, 0), (0 + 1, 0), (0 + 1, 0 + 1)]
        }
    },

    'S-piece right': {
        'name': 'S-piece right',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            0 : [(0 + 1, 0), (0, 0), (0, 0 + 1), (0 - 1, 0 + 1)],
            1 : [(0, 0 - 1), (0, 0), (0 + 1, 0), (0 + 1, 0 + 1)],
            2 : [(0 + 1, 0), (0, 0), (0, 0 + 1), (0 - 1, 0 + 1)],
            3 : [(0, 0 - 1), (0, 0), (0 + 1, 0), (0 + 1, 0 + 1)]
        }
    },

    'S-piece left': {
        'name': 'S-piece left',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            0 : [(0 -1 , 0), (0, 0), (0, 0 + 1), (0 + 1, 0 + 1)],
            1 : [(0, 0 + 1), (0, 0), (0 + 1, 0), (0 + 1, 0 - 1)],
            2 : [(0 - 1, 0), (0, 0), (0, 0 + 1), (0 + 1, 0 + 1)],
            3 : [(0, 0 + 1), (0, 0), (0 + 1, 0), (0 + 1, 0 - 1)]
        }
    },

    'I-piece': {
        'name': 'I-piece',
        'center_offset': {
            0 : 0,
            1 : 1,
            2 : 0,
            3 : 1
            },
        'shape': {
            1 : [(0, 0 - 2), (0, 0), (0, 0 - 1), (0, 0 + 1)],
            2 : [(0 + 1, 0), (0, 0), (0 - 1, 0), (0 - 2, 0)],
            3 : [(0, 0 - 2), (0, 0), (0, 0 - 1), (0, 0 + 1)],
            0 : [(0 + 1, 0), (0, 0), (0 - 1, 0), (0 - 2, 0)]
        }
    },

    'T-piece': {
        'name': 'T-piece',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            2 : [(0, 0 - 1), (0 - 1, 0), (0, 0), (0 + 1, 0)],
            3 : [(0 + 1, 0), (0, 0 - 1), (0, 0), (0, 0 + 1)],
            0 : [(0, 0 + 1), (0 + 1, 0), (0, 0), (0 - 1, 0)],
            1 : [(0 - 1, 0), (0, 0 + 1), (0, 0), (0, 0 - 1)]
        }
    },

    'Sq-piece': {
        'name': 'Sq-piece',
        'center_offset': {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
            },
        'shape': {
            0 : [(0 - 1, 0), (0, 0), (0 - 1, 0 + 1), (0, 0 + 1)],
            1 : [(0 - 1, 0), (0, 0), (0 - 1, 0 + 1), (0, 0 + 1)],
            2 : [(0 - 1, 0), (0, 0), (0 - 1, 0 + 1), (0, 0 + 1)],
            3 : [(0 - 1, 0), (0, 0), (0 - 1, 0 + 1), (0, 0 + 1)]
        }
    }
}
