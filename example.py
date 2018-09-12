import profile
from life_game import Control
import settings
import random


class MyControl(Control):
    def __init__(self):
        # 初始化配置
        super(MyControl, self).__init__()
        self.cell_color = "red"
        self.sleep_time = 100

    def get_sleep_time(self):
        if self.paint_nums % 5 == 0:
            return 1000
<<<<<<< HEAD
        return self.mapping.sleep

    def before_paint(self):
        color_list=["red","orange","yellow","green","blue","indigo","purple"]
        # 每隔5代改变一次颜色
        self.mapping.generate_next()
        if self.paint_nums % 5 == 0:
            self.game.cell_color=color_list[random.randint(0,6)]
            # self.game.cell_color = "blue" if self.game.cell_color == "red" else "red"
            for cell in self.get_cells():
                if cell.lived and cell.shape_obj:
                    self.cv.itemconfig(cell.shape_obj, 
                                       fill=self.game.cell_color, 
                                       outline=self.game.cell_color)
=======
        return 100
>>>>>>> 49482464675e88770795fb93213dbd44fb048eba

    def get_cell_color(self):
        if self.paint_nums % 10 < 5:
            return "red"
        return "blue"

def main():
    control = MyControl()
    control.config.from_object(settings)
    control.start()

if __name__ == '__main__':
    # profile.run("main()")
    main()
