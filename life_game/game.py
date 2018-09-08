from tkinter import Tk, Canvas
from life_game.immutable_dict import ImmutableDict
from life_game.config import Config, ConfigAttribute
from life_game import Mapping


class Game(object):
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

    def start(self):
        """游戏开始"""
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.loop_paint()
        self.root.mainloop()

    def init_window(self):
        #: 初始化窗口
        width = str(self.window_width)
        height = str(self.window_height)
        left = str(self.margin_left)
        top = str(self.margin_top)

        self.root.geometry(''.join([width, 'x', height, '+', left, '+', top]))
        #: 窗口大小是否可以改变
        is_change = self.window_change
        self.root.resizable(width=is_change, height=is_change)
    
    def init_canvas(self):
        #: 生命游戏的画布
        root = self.root
        width = self.window_width
        height = self.window_height
        bg = self.background

        self.cv = Canvas(root, width=width, height=height, bg=bg)
        self.cv.pack()

    def get_cell_position(self, x, y):
        size = self.cell_size
        left = self.canvas_margin_left
        top = self.canvas_margin_top

        x1 = x * size + left
        y1 = y * size + top
        x2 = (x + 1) * size + left
        y2 = (y + 1) * size + top

        return x1, y1, x2, y2

    def get_cells(self):
        for x in range(self.mapping.map_x+1):
            for y in range(self.mapping.map_y+1):
                yield self.mapping.game_map[x][y]
    
    def init_mapping(self):
        self.mapping = Mapping(self.column_nums, self.row_nums, self.init_cells, self.debug)
        # 边框
        x1 = self.canvas_margin_left
        y1 = self.canvas_margin_top
        x2 = self.cell_size*(self.mapping.map_x+1)+self.canvas_margin_left
        y2 = self.cell_size*(self.mapping.map_y+1)+self.canvas_margin_top

        self.cv.create_line(x1, y1, x2, y1)
        self.cv.create_line(x1, y1, x1, y2)
        self.cv.create_line(x2, y1, x2, y2)
        self.cv.create_line(x1, y2, x2, y2)

        # 初始化地图
        for cell in self.get_cells():
            if cell.lived:
                coordins = self.get_cell_position(cell.x, cell.y)
                color = self.cell_color
                cell.shape_obj = self.cv.create_rectangle(*coordins, fill=color, outline=color)
    
    def loop_paint(self):
        self.mapping.generate_next()
        self.paint()
        self.cv.after(self.sleep_time, self.loop_paint)


    def paint(self):
        for cell in self.get_cells():
            if cell.lived and not cell.shape_obj:
                coordins = self.get_cell_position(cell.x, cell.y)
                color = self.cell_color
                cell.shape_obj = self.cv.create_rectangle(*coordins, fill=color, outline=color)

            elif not cell.lived and cell.shape_obj:
                self.cv.delete(cell.shape_obj)
                cell.shape_obj = None
