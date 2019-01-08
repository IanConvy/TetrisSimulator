import pieces

order = ['piece_list', 'height', 'width', 'drop_site', 'guides', 'fps', 'gravity_set', 'das_limit', 'das_floor', 'first_delay', 'entry_delay', 'line_clear_points']

layout = {
    'piece_list': {
        'label': 'Piece List: ',
        'type': 'dropbox',
        'values': ['Custom', 'Standard'],
        'assets': {
            'Custom': None,
            'Standard': pieces.standard_list
            }
        },
    'height': {
        'label': 'Height: ',
        'type': 'entry',
        },
    'width': {
        'label': 'Width: ',
        'type': 'entry'
        },
    'drop_site': {
        'label': 'Entry Block: ',
        'type': 'entry'
        },
    'line_clear_points': {
        'title': 'Line Clears: ',
        'label1': 'Rows: ',
        'label2': 'Points: ',
        'type': 'scroll'
        },
    'guides': {
        'label': 'Guides: ',
        'type': 'dropbox',
        'values': ['On', 'Off'],
        'assets': {
            'On': True,
            'Off': False
            }
        },
    'fps': {
        'label': 'FPS: ',
        'type': 'entry'
        },
    'das_limit': {
        'label': 'DAS Limit: ',
        'type': 'entry'
        },
    'das_floor': {
        'label': 'DAS Floor: ',
        'type': 'entry'
        },
    'gravity_set': {
        'label': 'Gravity: ',
        'type': 'entry'
        },
    'first_delay': {
        'label': 'First Delay: ',
        'type': 'entry'
        },
    'entry_delay': {
        'title': 'Entry Delays: ',
        'label1': 'Rows: ',
        'label2': 'Delay: ',
        'type': 'scroll'
    }
}

presets = {
    'custom': {
        'themes': {
            'playfield_theme': 'Default',
            'pieces_theme': 'Default'
            },
        'settings': {
            'piece_list': 'Standard',
            'drop_site': '(5, 0)',
            'height': 20,
            'width': 10,
            'guides': 'On',
            'fps': 60,
            'gravity_set': 0,
            'first_delay': 0,
            'das_limit': 0,
            'das_floor': 0,
            'entry_delay': {},
            'line_clear_points': {}
            }
        },

    'NES_Level19': {
        'themes': {
            'playfield_theme': 'NES Tetris',
            'pieces_theme': 'NES Red & Yellow'
            },
        'settings': {
            'piece_list': 'Standard',
            'drop_site': (5, 0),
            'height': 20,
            'width': 10,
            'guides': 'On',
            'fps': 60.1,
            'gravity_set': 2,
            'first_delay': 96,
            'das_limit': 16,
            'das_floor': 10,
            'entry_delay': {
                19: 10,
                18: 10,
                17: 12,
                16: 12,
                15: 12,
                14: 12,
                13: 14,
                12: 14,
                11: 14,
                10: 14,
                9: 16,
                8: 16,
                7: 16,
                6: 16,
                5: 18,
                4: 18,
                3: 18,
                2: 18,
                1: 18,
                0: 18
                },
            'line_clear_points': {
                1 : 800,
                2: 2000,
                3: 6000,
                4: 24000
                }
            }
        }
    }
