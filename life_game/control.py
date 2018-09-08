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
    """
    以 `get` 开头的方法, 控制整个游戏过程中的各个属性,
    自定义需要的属性, 需要重载这些方法.
    """
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
        return self.mapping.map_x

    @property
    def map_y(self):
        return self.mapping.map_y

    @property
    def root(self):
        return self.game.root

    @property
    def config(self):
        return self.game.config

    def get_sleep_time(self):
        return self.game.sleep_time

    def get_cell_color(self):
        return self.game.cell_color

    def get_cell_size(self):
        return self.game.cell_size

    def get_canvas_margin_left(self):
        return self.game.canvas_margin_left

    def get_canvas_margin_top(self):
        return self.game.canvas_margin_top

    def get_cell_position(self, x, y):
        """重载获取位置,细胞大小函数
        使用该对象的方法来得到图像的位置属性,大小属性
        """
        size = self.get_cell_size()
        left = self.get_canvas_margin_left()
        top = self.get_canvas_margin_top()

        x1 = x * size + left
        y1 = y * size + top
        x2 = (x + 1) * size + left
        y2 = (y + 1) * size + top

        return x1, y1, x2, y2

    def get_cells(self):
        for cell in self.game.get_cells():
            yield cell

    def start(self):
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.control_loop()
        self.root.mainloop()
        self.finally_event()

    def init_window(self):
        self.game.init_window()

    def init_canvas(self):
        self.game.init_canvas()

    def init_mapping(self):
        self.game.init_mapping()

    def control_loop(self):
        self.before_control()
        if self.update_cells:
            self.control()
        self.after_control()

    def before_control(self):
        self.loop_nums += 1

    def control(self):
        self.before_paint()
        self.paint()
        self.after_paint()

    def before_paint(self):
        """在每次画图前将以存在的图删去
        保证每一次画图都是将全部活细胞重新绘制
        """
        self.mapping.generate_next()

        for cell in self.get_cells():
            if cell.lived and cell.shape_obj:
                self.canvas.delete(cell.shape_obj)
                cell.shape_obj = None

    def paint(self):
        """重载画图函数
        使用该对象的方法来得到图像的属性
        """
        for cell in self.get_cells():
            lived = cell.lived
            shaped = cell.shape_obj

            if lived and not shaped:
                coordins = self.get_cell_position(cell.x, cell.y)
                color = self.get_cell_color()
                cell.shape_obj = self.canvas.create_rectangle(*coordins, fill=color, outline=color)

            elif not lived and shaped:
                self.canvas.delete(cell.shape_obj)
                cell.shape_obj = None

    def after_paint(self):
        self.paint_nums += 1

    def after_control(self):
        sleep_time = self.get_sleep_time()
        self.canvas.after(sleep_time, self.control_loop)

    def finally_event(self):
        print("再见!")
