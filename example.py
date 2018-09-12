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
        return 100

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
