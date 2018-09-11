import profile
from life_game import Control
import settings


class MyControl(Control):
    # 初始化配置
    cell_color = "red"
    sleep_time = 100

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
