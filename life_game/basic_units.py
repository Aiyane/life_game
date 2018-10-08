"""module of game map"""
import random


class Mapping(object):
    """game map"""
    def __init__(self, x, y, dot_map=None, debug=False):
        """init
        """
        self.debug = debug
        self.init_game_map(x, y)
        self.init_cells(dot_map)

    def print_cells(self):
        """print cell status"""
        for row in self.game_map:
            lived = [cell.lived for cell in row]
            print(lived)

    def random_init_cells(self):
        """"random init cells"""
        cells = []
        for __ in range(random.randint(1, self.map_x*self.map_y)):
            x_coordin = random.randint(0, self.map_x)
            y_coordin = random.randint(0, self.map_y)
            cells.append([x_coordin, y_coordin])
        return cells

    def init_game_map(self, x_coordin, y_coordin):
        """init game map"""
        self.map_x, self.map_y = x_coordin, y_coordin
        self.game_map = [[Cell(False, x, y) for y in range(y_coordin+1)]
                         for x in range(x_coordin+1)]

    def init_cells(self, dot_map=None):
        """init cells"""
        if not dot_map:
            dot_map = self.random_init_cells()

        for x_coordin, y_coordin in dot_map:
            self.game_map[x_coordin][y_coordin].lived = True

        if self.debug:
            print("\ninit the life game:")
            self.print_cells()

    def generate_next(self):
        """"generate next genertion"""
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
    """Cell class"""
    def __init__(self, lived, x_coordin, y_coordin):
        self.lived = lived
        self.next = False
        self.x_coordin = x_coordin
        self.y_coordin = y_coordin
        self.shape_obj = None

    def count_lived_num(self, mapping):
        """compute count of living live"""
        game_map = mapping.game_map
        x_coordin = self.x_coordin
        y_coordin = self.y_coordin
        count = 0
        for i in range(x_coordin-1, x_coordin+2):
            for j in range(y_coordin-1, y_coordin+2):
                con1 = i != x_coordin or j != y_coordin
                con2 = i >= 0 and j >= 0
                con3 = i <= mapping.map_x and j <= mapping.map_y

                if con1 and con2 and con3:
                    if game_map[i][j].lived:
                        count += 1
        return count

    def look_up(self, mapping):
        """set `next` about next genertion if alived"""
        count = self.count_lived_num(mapping)

        if count == 2:
            self.next = self.lived
        elif count == 3:
            self.next = True
        else:
            self.next = False
