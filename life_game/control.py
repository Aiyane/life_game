"""
about control game
"""
from life_game import Game


class Control(Game):
    """
    the mothed's name the begin of `get`, can cantrol most attrs about the game.
    if you want to change these attrs, you can heavy load these mothed.
    """

    def __init__(self):
        super(Control, self).__init__()
        self.update_cells = True
        self.paint_nums = 0
        self.loop_nums = 0

        self.before_control_funcs = []
        self.after_control_funcs = []
        self.before_paint_funcs = []
        self.after_paint_funcs = []
        self.finally_event_funcs = []


    @property
    def map_x(self):
        """the number of game's row"""
        return self.mapping.map_x

    @property
    def map_y(self):
        """the number of game's column"""
        return self.mapping.map_y

    def start(self):
        """begin of the game"""
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.control_loop()
        self.root.mainloop()
        for func in self.finally_event_funcs:
            func(self)

    def control_loop(self):
        """cycle control"""
        # self.before_control()
        self.loop_nums += 1
        for func in self.before_control_funcs:
            func(self)

        if self.update_cells:
            self.control()

        # self.after_control()
        sleep_time = self.get_sleep_time()
        self.canvas.after(sleep_time, self.control_loop)
        for func in self.after_control_funcs:
            func(self)

    def before_control(self, f):
        """before control"""
        self.before_control_funcs.append(f)
        return f

    def control(self):
        """ont tmie control"""
        # self.before_paint()
        self.mapping.generate_next()

        for cell in self.get_cells():
            if cell.lived and cell.shape_obj:
                self.canvas.delete(cell.shape_obj)
                cell.shape_obj = None
        for func in self.before_paint_funcs:
            func(self)

        self.paint()

        # self.after_paint()
        self.paint_nums += 1
        for func in self.after_paint_funcs:
            func(self)

    def before_paint(self, f):
        """delete the existing cells before each drawing
        """
        self.before_paint_funcs.append(f)
        return f

    def after_paint(self, f):
        """after paint"""
        self.after_paint_funcs.append(f)
        return f

    def after_control(self, f):
        """after control"""
        self.after_control_funcs.append(f)
        return f

    def finally_event(self, f):
        """what you need to do after the game is over"""
        self.finally_event_funcs.append(f)
        return f
