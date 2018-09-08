from life_game import Control
import settings


class MyControl(Control):
    # 初始化配置
    cell_color = "red"
    sleep_time = 100

    def sleep(self):
        if self.paint_nums % 5 == 0:
            return 1000
        return 100

    def before_paint(self):
        # 每隔5代改变一次颜色
        self.mapping.generate_next()
        if self.paint_nums > 0 and self.paint_nums % 5 == 0:
            self.game.cell_color = "blue" if self.game.cell_color == "red" else "red"
            for cell in self.get_cells():
                if cell.lived and cell.shape_obj:
                    self.canvas.itemconfig(cell.shape_obj,
                                           fill=self.game.cell_color,
                                           outline=self.game.cell_color)


if __name__ == '__main__':
    control = MyControl()
    control.config.from_object(settings)
    control.start()
