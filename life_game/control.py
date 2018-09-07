import time
from life_game import Game


class Control(object):
    def __init__(self):
        self.game = Game()
        self.update_cells = True
        self.paint_nums = 0
        self.loop_nums = 0

    @property
    def mapping(self):
        if hasattr(self.game, 'mapping'):
            return self.game.mapping
        return None

    @property
    def map_x(self):
        return self.game.mapping.map_x

    @property
    def map_y(self):
        return self.game.mapping.map_y

    @property
    def root(self):
        return self.game.root

    @property
    def config(self):
        return self.game.config

    @property
    def cv(self):
        return self.game.cv

    def get_cell_position(self, x, y):
        return (x*self.game.cell_size+self.game.canvas_margin_left,
                y*self.game.cell_size+self.game.canvas_margin_top,
                (x+1)*self.game.cell_size+self.game.canvas_margin_left,
                (y+1)*self.game.cell_size+self.game.canvas_margin_top)

    def get_cells(self):
        for x in range(self.map_x+1):
            for y in range(self.map_y+1):
                yield self.mapping.game_map[x][y]

    def pause(self):
        self.update_cells = False

    def go(self):
        self.update_cells = True

    def start(self):
        self.init_mapping()
        self.next_control_func()
        self.root.mainloop()
        self.finally_event()

    def next_control_func(self):
        self.before_control()
        self.control()
        self.after_control()

    def control(self):
        if self.update_cells:
            self.before_paint()
            self.paint()
            self.after_paint()

    def paint(self):
        self.game.paint()

    def sleep(self):
        return self.mapping.sleep

    def init_mapping(self):
        self.game.init_mapping()

    def before_paint(self):
        self.mapping.generate_next()

    def finally_event(self):
        print("再见!")

    def after_control(self):
        self.cv.after(self.sleep(), self.next_control_func)

    def after_paint(self):
        self.paint_nums += 1

    def before_control(self):
        self.loop_nums += 1
