import os
from tkinter import *
from life_game.immutable_dict import ImmutableDict
from life_game.config import Config, ConfigAttribute
from life_game.mapping import Mapping


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
        'CELL_COLOR':                           "black"
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
        self.root.geometry(''.join([str(self.window_width), 'x', str(self.window_height), '+',
                                    str(self.margin_left), '+', str(self.margin_top)]))
        #: 窗口大小是否可以改变
        self.root.resizable(width=self.window_change,
                            height=self.window_change)
    
    def init_canvas(self):
        #: 生命游戏的画布
        self.cv = Canvas(self.root, width=self.window_width, height=self.window_height, bg='white')
        self.cv.pack()

    def get_cell_position(self, x, y):
        return (x*self.cell_size+self.canvas_margin_left,
                y*self.cell_size+self.canvas_margin_top,
                (x+1)*self.cell_size+self.canvas_margin_left,
                (y+1)*self.cell_size+self.canvas_margin_top)

    def get_cells(self):
        for x in range(self.mapping.map_x+1):
            for y in range(self.mapping.map_y+1):
                yield self.mapping.game_map[x][y]
    
    def init_mapping(self):
        self.mapping = Mapping(self.column_nums, self.row_nums, self.init_cells, self.debug)
        # 边框
        dot_x1 = self.canvas_margin_left
        dot_y1 = self.canvas_margin_top
        dot_x2 = self.cell_size*(self.mapping.map_x+1)+self.canvas_margin_left
        dot_y2 = self.cell_size*(self.mapping.map_y+1)+self.canvas_margin_top

        self.cv.create_line(dot_x1, dot_y1, dot_x2, dot_y1)
        self.cv.create_line(dot_x1, dot_y1, dot_x1, dot_y2)
        self.cv.create_line(dot_x2, dot_y1, dot_x2, dot_y2)
        self.cv.create_line(dot_x1, dot_y2, dot_x2, dot_y2)

        # 初始化地图
        for cell in self.get_cells():
            if cell.lived:
                cell.shape_obj = self.cv.create_rectangle(*self.get_cell_position(cell.x, cell.y),
                                                          fill=self.cell_color, outline=self.cell_color)
    
    def loop_paint(self):
        self.mapping.generate_next()
        self.paint()
        self.cv.after(self.sleep_time, self.loop_paint)


    def paint(self):
        for cell in self.get_cells():
            if cell.lived and not cell.shape_obj:
                cell.shape_obj = self.cv.create_rectangle(*self.get_cell_position(cell.x, cell.y),
                                                          fill=self.cell_color, outline=self.cell_color)
            elif not cell.lived and cell.shape_obj:
                self.cv.delete(cell.shape_obj)
                cell.shape_obj = None
