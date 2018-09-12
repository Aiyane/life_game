"""
与游戏控制有关的类
"""
from life_game import Game


class Control(Game):
    """
    以 `get` 开头的方法, 控制整个游戏过程中的各个属性,
    自定义需要的属性, 需要重载这些方法.
    """

    def __init__(self):
        super(Control, self).__init__()
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
    def map_x(self):
        """游戏地图行数"""
        return self.mapping.map_x

    @property
    def map_y(self):
        """游戏地图列数"""
        return self.mapping.map_y

    def start(self):
        """游戏开始"""
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.control_loop()
        self.root.mainloop()
        self.finally_event()

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

    def after_paint(self):
        """每次细胞生成后的钩子"""
        self.paint_nums += 1

    def after_control(self):
        """每次控制后的钩子"""
        sleep_time = self.get_sleep_time()
        self.canvas.after(sleep_time, self.control_loop)

    def finally_event(self):
        """游戏关闭需要完成的事"""
        print("经过了" + str(self.paint_nums) + "代，再见!")
