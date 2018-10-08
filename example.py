from life_game import Control
import settings
from tkinter import Button, StringVar


class MyGame(Control):
    # 第一种控制方式：继承 Control 函数，改变以 get 开头的方法，动态控制参数
    def get_sleep_time(self):
        if self.paint_nums % 5 == 0:
            return 1000
        return 100

    def get_cell_color(self):
        if self.paint_nums % 10 < 5:
            return "red"
        return "blue"

game = MyGame()

# 第二种控制方式：自定义事件函数，利用提供的装饰器在指定时期执行
@game.after_paint
def print_hello(game):
    print("painted " + str(game.paint_nums) + " generation.")

@game.finally_event
def finally_event(game):
    print("After " + str(game.paint_nums) + " generations, goodbye!")

if __name__ == '__main__':
    # 第三种控制方式：利用配置文件，初始化就定义好属性
    game.config.from_object(settings)
    # 第四种控制方式：直接改变参数属性
    game.cell_color = "red"
    game.sleep_time = 100

    game.start()
