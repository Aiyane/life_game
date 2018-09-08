import time
from life_game import Game


class NotInitError(Exception):
    pass


class BaseConrol(type):
    def __new__(cls, name, bases, attrs):
        cls = super(BaseConrol, cls).__new__(cls, name, bases, attrs)
        if name == 'Control':
            setattr(cls, 'game', Game())
        else:
            for attr in dir(cls):
                if attr.upper() in cls.game.config:
                    setattr(cls.game, attr, getattr(cls, attr))
        return cls


class Control(object, metaclass=BaseConrol):
    def __init__(self):
        self.update_cells = True
        self.paint_nums = 0
        self.loop_nums = 0

    @property
    def mapping(self):
        if hasattr(self.game, 'mapping'):
            return self.game.mapping
        raise NotInitError("`game.mapping` 没有初始化, 尝试先调用 `init_mapping` 函数")

    @property
    def canvas(self):
        if hasattr(self.game, 'cv'):
            return self.game.cv
        raise NotInitError("`game.cv` 没有初始化, 尝试先调用 `init_canvas` 函数")

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

    def get_cell_position(self, x, y):
        return self.game.get_cell_position(x, y)

    def get_cells(self):
        for cell in self.game.get_cells():
            yield cell

    def start(self):
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.next_control_func()
        self.root.mainloop()
        self.finally_event()
    
    def init_window(self):
        self.game._init_window()
    
    def init_canvas(self):
        self.game._init_canvas()

    def init_mapping(self):
        self.game._init_mapping()

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
        self.game._paint()

    def after_paint(self):
        self.paint_nums += 1

    def sleep(self):
        return self.game.sleep_time

    def after_control(self):
        self.canvas.after(self.sleep(), self.next_control_func)

    def finally_event(self):
        print("再见!")
