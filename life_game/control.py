import time
from life_game import Game


class Control(object):
    def __init__(self):
        self.game = Game()
        self.update_cells = True
        self.paint_nums = 0
        self.loop_nums = 0
    
    def init_window(self):
        self.game.init_window()
    
    def init_canvas(self):
        self.game.init_canvas()
   
    def init_mapping(self):
        self.game.init_mapping()
    
   
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
    
    def get_cell_color(self):
        return self.game.cell_color
    
    def get_cell_size(self):
        return self.game.cell_size
    
    def get_canvas_margin_left(self):
        return self.game.canvas_margin_left
    
    def get_canvas_margin_top(self):
        return self.game.canvas_margin_top
    
    def sleep(self):
        return self.mapping.sleep

    def get_cell_position(self, x, y):
        return (x*self.game.cell_size+self.get_canvas_margin_left(),
                y*self.game.cell_size+self.get_canvas_margin_top(),
                (x+1)*self.game.cell_size+self.get_canvas_margin_left(),
                (y+1)*self.game.cell_size+self.get_canvas_margin_top())

    def get_cells(self):
        for cell in self.game.get_cells():
            yield cell

    def pause(self):
        self.update_cells = False

    def go(self):
        self.update_cells = True
    
    def start(self):
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.next_control_func()
        self.root.mainloop()
        self.finally_event()

    def next_control_func(self):
        self.before_control()
        self.control()
        self.after_control()
    
    def before_control(self):
        self.loop_nums += 1

    def control(self):
        if self.update_cells:
            self.before_paint()
            self.paint()
            self.after_paint()

    def before_paint(self):
        self.mapping.generate_next()

    def paint(self):
        self.game.paint()
    
    def after_paint(self):
        self.paint_nums += 1
    
    
    def after_control(self):
        self.cv.after(self.sleep(), self.next_control_func)

    def finally_event(self):
        print("再见!")
