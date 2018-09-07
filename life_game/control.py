import time
from life_game import Game


class Control(object):
    def __init__(self):
        self.game = Game()
        self.is_continue = True
        self.paint_nums = 0
        self.loop_nums = 0
        self.closed_default_paint = False

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
        self.is_continue = False

    def go(self):
        self.is_continue = True

    def start(self):
        self.before_init_mapping()

        if hasattr(self, 'init_mapping'):
            self.init_mapping()
        else:
            self.game.init_mapping()
            
        self.after_init_mapping()
        self.next_control_func()
        self.finally_event()
        self.root.mainloop()

    def next_control_func(self):
        self.before_control()
        self.control()
        self.after_control()

        if hasattr(self, 'sleep'):
            sleep_time = self.sleep
        else:
            sleep_time = self.mapping.sleep

        self.cv.after(sleep_time, self.next_control_func)

    def control(self):
        self.loop_nums += 1

        if self.is_continue:
            self.before_paint()
            self.mapping.generate_next()

            if self.closed_default_paint and hasattr(self, 'paint'):
                self.paint()
            else:
                self.game.paint()

            self.paint_nums += 1
            self.after_paint()
    
    def before_init_mapping(self):
        pass
    def after_init_mapping(self):
        pass
    def before_control(self):
        pass
    def after_control(self):
        pass
    def before_paint(self):
        pass
    def after_paint(self):
        pass
    def finally_event(self):
        pass