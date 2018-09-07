from life_game import Control, Mapping
import settings


class MyControl(Control):
    def init_mapping(self):
        # 重载初始化地图, 去除边框
        self.game.cell_color = "red"
        self.game.init_mapping()

    def sleep(self):
        if self.paint_nums % 5 == 0:
            return 1000
        return self.mapping.sleep

    def before_paint(self):
        # 每隔5代改变一次颜色
        self.mapping.generate_next()
        if self.paint_nums % 5 == 0:
            self.game.cell_color = "blue" if self.game.cell_color == "red" else "red"
            for cell in self.get_cells():
                if cell.lived and cell.shape_obj:
                    self.cv.itemconfig(cell.shape_obj, 
                                       fill=self.game.cell_color, 
                                       outline=self.game.cell_color)


if __name__ == '__main__':
    control = MyControl()
    control.config.from_object(settings)
    control.start()
