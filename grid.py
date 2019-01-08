import pieces

class Grid:
    def __init__(self, dim):
        self.dim = dim
        self.grid = {}
        for y in range(-3, dim[1] + 5):
            self.grid[y] = {}
            for x in range(-5, dim[0] + 5):
                self.grid[y][x] = 'block'
        for y in range(-3, dim[1]):
            for x in range(dim[0]):
                self.grid[y][x] = False

    def copy_to_dict(self, block_dict, whole = False, top = 0, bottom = 0, left = 0, right = 0):
        if whole:
            top = 0
            bottom = self.dim[1] - 1
            left = 0
            right = self.dim[0] - 1
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                block_dict[(x, y)] = self.grid[y][x]
        return block_dict

    def grid_piece(self, piece, clear = False):
        for (x, y) in piece.coords:
            self.grid[y][x] = piece.name

    def get_filled_rows(self):
        row_list = []
        for y in range(0, self.dim[1]):
            if all(self.grid[y].values()):
                row_list.append(y)
        return row_list

    def row_clear(self, row_list):
        for row in row_list:
            for y in range(row, -3, -1):
                self.grid[y] = self.grid[y - 1].copy()

    def collision_check(self, coords):
        check = False
        for (x, y) in coords:
            if self.grid[y][x]:
                check = True
        return check
