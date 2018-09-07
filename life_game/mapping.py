import random


class Mapping(object):
    def __init__(self, x, y, dot_map=None, debug=False):
        """"初始化
        param x: 地图宽
        param y: 地图高
        param dot_map: 初始化活得细胞 list
        """
        self.debug = debug
        self.init_game_map(x, y)
        self.init_cells(dot_map)

    def print_cells(self):
        for row in self.game_map:
            lived = [cell.lived for cell in row]
            print(lived)

    def random_init_cells(self):
        cells = []
        for i in range(random.randint(1, self.map_x*self.map_y)):
            cell = [random.randint(0, self.map_x),
                    random.randint(0, self.map_y)]
            cells.append(cell)
        return cells

    def init_game_map(self, x, y):
        """初始化地图"""
        self.map_x, self.map_y = x, y
        self.game_map = [[Cell(False, x, y) for y in range(y+1)]
                         for x in range(x+1)]

    def init_cells(self, dot_map=None):
        """初始化细胞"""
        if not dot_map:
            dot_map = self.random_init_cells()

        for x, y in dot_map:
            self.game_map[x][y].lived = True

        if self.debug:
            print("\n初始化生命游戏:")
            self.print_cells()

    def generate_next(self):
        for row in self.game_map:
            for cell in row:
                cell.look_up(self)

        for row in self.game_map:
            for cell in row:
                cell.lived = cell.next

        if self.debug:
            print("")
            self.print_cells()


class Cell(object):
    def __init__(self, lived, x, y):
        self.lived = lived
        self.next = False
        self.x = x
        self.y = y
        self.shape_obj = None

    def look_up(self, mapping):
        game_map = mapping.game_map
        x = self.x
        y = self.y
        count = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if ((i != x or j != y) and
                    i >= 0 and j >= 0 and
                    i <= mapping.map_x and
                    j <= mapping.map_y and
                        game_map[i][j].lived):
                    count += 1

        if count == 2:
            self.next = self.lived
        else:
            self.next = True if count == 3 else False
