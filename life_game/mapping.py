"""游戏地图相关模块"""
import random


class Mapping(object):
    """游戏地图"""
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
        """打印细胞状态"""
        for row in self.game_map:
            lived = [cell.lived for cell in row]
            print(lived)

    def random_init_cells(self):
        """"随机初始化细胞"""
        cells = []
        for __ in range(random.randint(1, self.map_x*self.map_y)):
            x_coordin = random.randint(0, self.map_x)
            y_coordin = random.randint(0, self.map_y)
            cells.append([x_coordin, y_coordin])
        return cells

    def init_game_map(self, x_coordin, y_coordin):
        """初始化地图"""
        self.map_x, self.map_y = x_coordin, y_coordin
        self.game_map = [[Cell(False, x, y) for y in range(y_coordin+1)]
                         for x in range(x_coordin+1)]

    def init_cells(self, dot_map=None):
        """初始化细胞"""
        if not dot_map:
            dot_map = self.random_init_cells()

        for x_coordin, y_coordin in dot_map:
            self.game_map[x_coordin][y_coordin].lived = True

        if self.debug:
            print("\n初始化生命游戏:")
            self.print_cells()

    def generate_next(self):
        """"生成下一代细胞"""
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
    """细胞类"""
    def __init__(self, lived, x_coordin, y_coordin):
        self.lived = lived
        self.next = False
        self.x = x_coordin
        self.y = y_coordin
        self.shape_obj = None

    def look_up(self, mapping):
        """下一代是否还存活"""
        game_map = mapping.game_map
        x_coordin = self.x
        y_coordin = self.y
        count = 0
        for i in range(x_coordin-1, x_coordin+2):
            for j in range(y_coordin-1, y_coordin+2):
                con1 = i != x_coordin or j != y_coordin
                con2 = i >= 0 and j >= 0
                con3 = i <= mapping.map_x and j <= mapping.map_y

                if con1 and con2 and con3:
                    if game_map[i][j].lived:
                        count += 1

        if count == 2:
            self.next = self.lived
        elif count == 3:
            self.next = True
        else:
            self.next = False
