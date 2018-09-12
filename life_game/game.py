"""
游戏模块
"""
from tkinter import Tk, Canvas
from life_game.immutable_dict import ImmutableDict
from life_game.config import Config, ConfigAttribute
from life_game.basic_units import Mapping


class Game(object):
    """
    游戏类
    """
    root = Tk()

    #: debug模式, 设置为 `True` 会打印出每一次迭代细胞的具体情况,
    #: 默认为 `False`
    debug = ConfigAttribute('DEBUG')

    #: 窗口宽度
    #: 默认为 `800`
    window_width = ConfigAttribute('WINDOW_WIDTH')

    #: 窗口高度
    #: 默认为 `600`
    window_height = ConfigAttribute('WINDOW_HEIGHT')

    #: 生命游戏地图一行的格子数
    #: 默认为 `50`
    row_nums = ConfigAttribute('ROW_NUMS')

    #: 生命游戏地图一列的格子数
    #: 默认为 `50`
    column_nums = ConfigAttribute('COLUMN_NUMS')

    #: 窗口里屏幕顶部的距离
    #: 默认为 `200`
    margin_top = ConfigAttribute('MARGIN_TOP')

    #: 窗口里屏幕左部的距离
    #: 默认为 `500`
    margin_left = ConfigAttribute('MARGIN_LEFT')

    #: 生命游戏更新一代细胞的时间间隔, 单位: 毫秒
    #: 默认为 `500`
    sleep_time = ConfigAttribute('SLEEP_TIME')

    #: 窗口大小是否可以改变, 为 `True` 时可以改变
    #: 默认为 `False`
    window_change = ConfigAttribute('WINDOW_CHANGE')

    #: 初始化活细胞的坐标, 应该为一个 list 对象
    #: 例如: `[[0,0], [1,2]]`
    #: 默认为 `None`
    init_cells = ConfigAttribute('INIT_CELLS')

    #: 生命游戏细胞大小, int 类型
    #: 默认为: `10`
    cell_size = ConfigAttribute('CELL_SIZE')

    #: 画布距离窗口顶部距离
    #: 默认为: `50`
    canvas_margin_top = ConfigAttribute('CANVAS_MARGIN_TOP')

    #: 画布距离窗口左部距离
    #: 默认为: `135`
    canvas_margin_left = ConfigAttribute('CANVAS_MARGIN_LEFT')

    #: 细胞颜色
    #: 默认为: `black`
    cell_color = ConfigAttribute('CELL_COLOR')

    #: 画布背景
    #: 默认为: `white`
    background = ConfigAttribute('BACKGROUND')

    #: 默认配置参数
    default_config = ImmutableDict({
        'DEBUG':                                False,
        'ROW_NUMS':                             50,
        'COLUMN_NUMS':                          50,
        'WINDOW_WIDTH':                         800,
        'WINDOW_HEIGHT':                        600,
        'MARGIN_TOP':                           200,
        'MARGIN_LEFT':                          500,
        'SLEEP_TIME':                           500,
        'WINDOW_CHANGE':                        False,
        'INIT_CELLS':                           None,
        'CELL_SIZE':                            10,
        'CANVAS_MARGIN_TOP':                    50,
        'CANVAS_MARGIN_LEFT':                   135,
        'CELL_COLOR':                           "black",
        'BACKGROUND':                           "white",
    })

    def __init__(self):
        #: 窗口标题
        self.root.title('生命游戏')
        #: 当前配置
        self.config = Config(self.default_config)
        self.cell_color = "black"

    def start(self):
        """游戏开始"""
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.loop_paint()
        self.root.mainloop()

    def init_window(self):
        """初始化窗口"""
        width = str(self.window_width)
        height = str(self.window_height)
        left = str(self.margin_left)
        top = str(self.margin_top)

        self.root.geometry(''.join([width, 'x', height, '+', left, '+', top]))
        #: 窗口大小是否可以改变
        is_change = self.window_change
        self.root.resizable(width=is_change, height=is_change)

    def init_canvas(self):
        """初始化生命游戏的画布"""
        root = self.root
        width = self.window_width
        height = self.window_height
        background = self.background

        self.canvas = Canvas(root, width=width, height=height, bg=background)
        self.canvas.pack()

    def add_border(self):
        """增加边框"""
        left_x = self.canvas_margin_left
        top_y = self.canvas_margin_top
        right_x = self.cell_size*(self.mapping.map_x+1)+self.canvas_margin_left
        bottom_y = self.cell_size*(self.mapping.map_y+1)+self.canvas_margin_top

        self.canvas.create_line(left_x, top_y, right_x, top_y)
        self.canvas.create_line(left_x, top_y, left_x, bottom_y)
        self.canvas.create_line(right_x, top_y, right_x, bottom_y)
        self.canvas.create_line(left_x, bottom_y, right_x, bottom_y)

    def init_mapping(self):
        """初始化地图"""
        self.mapping = Mapping(self.column_nums, self.row_nums, self.init_cells, self.debug)
        self.add_border()

        # 初始化地图
        color = self.get_cell_color()
        for cell in self.get_cells():
            if cell.lived:
                coordins = self.get_cell_position(cell.x, cell.y)
                cell.shape_obj = self.canvas.create_rectangle(*coordins, fill=color, outline=color)

    def loop_paint(self):
        """循环绘制细胞"""
        self.mapping.generate_next()
        self.paint()
        sleep_time = self.get_sleep_time()
        self.canvas.after(sleep_time, self.loop_paint)

    def paint(self):
        """绘制细胞"""
        color = self.get_cell_color()
        for cell in self.get_cells():
            if cell.lived and not cell.shape_obj:
                coordins = self.get_cell_position(cell.x, cell.y)
                cell.shape_obj = self.canvas.create_rectangle(*coordins, fill=color, outline=color)

            elif not cell.lived and cell.shape_obj:
                self.canvas.delete(cell.shape_obj)
                cell.shape_obj = None

    def get_sleep_time(self):
        """获取定时器"""
        return self.sleep_time

    def get_cell_color(self):
        """获取细胞颜色"""
        return self.cell_color

    def get_cell_size(self):
        """获取细胞大小"""
        return self.cell_size

    def get_canvas_margin_left(self):
        """获取画布左边距"""
        return self.canvas_margin_left

    def get_canvas_margin_top(self):
        """获取画布上边距"""
        return self.canvas_margin_top

    def get_cell_position(self, x_coordin, y_coordin):
        """获取细胞坐标"""
        size = self.get_cell_size()
        left = self.get_canvas_margin_left()
        top = self.get_canvas_margin_top()

        return (
            x_coordin * size + left,
            y_coordin * size + top,
            (x_coordin + 1) * size + left,
            (y_coordin + 1) * size + top
        )

    def get_cells(self):
        """获取所有细胞"""
        for x_coordin in range(self.mapping.map_x+1):
            for y_coordin in range(self.mapping.map_y+1):
                yield self.mapping.game_map[x_coordin][y_coordin]
