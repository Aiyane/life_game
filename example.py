import profile
from life_game import Control
import settings
from tkinter import Button, StringVar


class MyControl(Control):
    def __init__(self):
        # 初始化配置
        super(MyControl, self).__init__()
        self.cell_color = "red"
        self.sleep_time = 100

    def get_cell_color(self):
        if self.paint_nums % 10 < 5:
            return "red"
        return "blue"
    
    def pause(self):
        self.update_cells = not self.update_cells
        if self.update_cells:
            self.strvar.set("暂停")
        else:
            self.strvar.set("继续")

    def init_window(self):
        super(MyControl, self).init_window()
        self.strvar = StringVar()
        self.strvar.set('暂停')
        btn = Button(self.root, textvariable=self.strvar, command=self.pause)
        btn.pack()

def main():
    control = MyControl()
    control.config.from_object(settings)
    control.start()

if __name__ == '__main__':
    # profile.run("main()")
    main()
