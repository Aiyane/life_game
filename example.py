from life_game import Control, Mapping
import settings


class MyControl(Control):
    def before_init_mapping(self):
        # 初始化为红色
        self.game.cell_color = "red"

    def init_mapping(self):
        # 重载初始化地图, 去除边框
        self.game.mapping = Mapping(self.game.column_nums, self.game.row_nums, self.game.sleep_time, 
                                    self.game.init_cells, self.game.debug)
        for cell in self.get_cells():
            if cell.lived:
                cell.shape_obj = self.cv.create_rectangle(*self.get_cell_position(cell.x, cell.y), 
                                                          fill=self.game.cell_color, 
                                                          outline=self.game.cell_color)

    def before_paint(self):
        if self.paint_nums > 0 and self.paint_nums % 5 == 0:
            self.game.cell_color = "blue" if self.game.cell_color == "red" else "red"
            for cell in self.get_cells():
                if cell.lived and cell.shape_obj:
                    self.cv.itemconfig(cell.shape_obj, fill=self.game.cell_color, outline=self.game.cell_color)


if __name__ == '__main__':
    control = MyControl()
    control.config.from_object(settings)
    control.start()
