"""
与游戏控制有关的类
"""
from life_game import Game
from life_game.help_func import get_sleep_time, get_cell_position


class NotInitError(Exception):
    """未初始化错误"""
    pass


class BaseConrol(type):
    """Control的元类，给Control绑定game参数，给Control类的子类初始化配置参数值"""
    def __new__(mcs, name, bases, attrs):
        mcs = super(BaseConrol, mcs).__new__(mcs, name, bases, attrs)
        if name == 'Control':
            mcs._init_game(mcs)
            delattr(mcs, '_init_game')
        else:
            for attr in dir(mcs):
                if attr.upper() in mcs.game.config:
                    setattr(mcs.game, attr, getattr(mcs, attr))
        return mcs


class Control(object, metaclass=BaseConrol):
    """
    以 `get` 开头的方法, 控制整个游戏过程中的各个属性,
    自定义需要的属性, 需要重载这些方法.
    """

    def __init__(self):
        self.update_cells = True
        self.paint_nums = 0
        self.loop_nums = 0
        if not hasattr(self, 'game'):
            self.game = Game()

    def _init_game(self):
        """初始化游戏，该方法不应该直接调用，只有在元类中会调用，调用后会删除该方法。
        该方法存在的目的是为了方便静态类型的检查，直接在元类中使用 `setattr` 方法当然可以。
        不过我们应该避免使用 `setattr` 这类对代码审查工具不友好的 '魔法方法'
        """
        self.game = Game()

    @property
    def mapping(self):
        """游戏地图"""
        if hasattr(self.game, 'mapping'):
            return self.game.mapping
        raise NotInitError("`game.mapping` 没有初始化, 尝试先调用 `init_mapping` 函数")

    @property
    def canvas(self):
        """游戏画布"""
        if hasattr(self.game, 'canvas'):
            return self.game.canvas
        raise NotInitError("`game.cv` 没有初始化, 尝试先调用 `init_canvas` 函数")

    @property
    def map_x(self):
        """游戏地图行数"""
        return self.mapping.map_x

    @property
    def map_y(self):
        """游戏地图列数"""
        return self.mapping.map_y

    @property
    def root(self):
        """Tk类实例"""
        return self.game.root

    @property
    def config(self):
        """游戏配置"""
        return self.game.config

    def get_cell_position(self, x_coordin, y_coordin):
        """重载获取位置,细胞大小函数
        使用该对象的方法来得到图像的位置属性,大小属性
        """
        return get_cell_position(self, x_coordin, y_coordin)

    def get_cells(self):
        """获取全部细胞"""
        for cell in self.game.get_cells():
            yield cell

    def start(self):
        """游戏开始"""
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.control_loop()
        self.root.mainloop()
        self.finally_event()

    def init_window(self):
        """初始化窗口"""
        self.game.init_window()

    def init_canvas(self):
        """初始化画布"""
        self.game.init_canvas()

    def init_mapping(self):
        """初始化地图"""
        self.game.init_mapping()

    def control_loop(self):
        """循环控制"""
        self.before_control()
        if self.update_cells:
            self.control()
        self.after_control()

    def before_control(self):
        """每次控制前的钩子"""
        self.loop_nums += 1

    def control(self):
        """一次循环控制"""
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
        self.game.paint(self)

    def after_paint(self):
        """每次细胞生成后的钩子"""
        self.paint_nums += 1

    def after_control(self):
        """每次控制后的钩子"""
        sleep_time = get_sleep_time(self, self.game.sleep_time)
        self.canvas.after(sleep_time, self.control_loop)

    def finally_event(self):
        """游戏关闭需要完成的事"""
        print("经过了" + str(self.paint_nums) + "代，再见!")
