from life_game import Control
import settings


class MyControl(Control):
    def before_control(self):
        if hasattr(self, 'sleep'):
            delattr(self, 'sleep')

        if self.paint_nums % 10 == 0:
            for cell in self.get_cells():
                if cell.shape_obj:
                    self.cv.itemconfig(cell.shape_obj, fill="black", outline='black')

    def after_paint(self):
        if self.paint_nums % 10 == 0:
            for cell in self.get_cells():
                if cell.shape_obj:
                    self.cv.itemconfig(cell.shape_obj, fill="blue", outline='blue')

            self.sleep = 1000


if __name__ == '__main__':
    control = MyControl()
    control.config.from_object(settings)
    control.start()
