"""
game module
"""
from tkinter import Tk, Canvas
from life_game.immutable_dict import ImmutableDict
from life_game.config import Config, ConfigAttribute
from life_game.basic_units import Mapping


class Game(object):
    """
    Game class
    """
    root = Tk()

    #: debug mode, setted `True` will print every generation cells.
    #: default is `False`
    debug = ConfigAttribute('DEBUG')

    #: the width of window
    #: default is `800`
    window_width = ConfigAttribute('WINDOW_WIDTH')

    #: the height of window
    #: default is `600`
    window_height = ConfigAttribute('WINDOW_HEIGHT')

    #: map row's number of grids
    #: default is
    row_nums = ConfigAttribute('ROW_NUMS')

    #: map column's number of grids
    #: default is `50`
    column_nums = ConfigAttribute('COLUMN_NUMS')

    #: the distance of the window from the top of the screen
    #: default is `200`
    margin_top = ConfigAttribute('MARGIN_TOP')

    #: the distance of the window from the left of the screen
    #: default is `500`
    margin_left = ConfigAttribute('MARGIN_LEFT')

    #: time interval for each update, Unit miliseconds
    #: default is `500`
    sleep_time = ConfigAttribute('SLEEP_TIME')

    #: if changed of the size of the window. it is changeabled when it is `True`.
    #: default is `False`
    window_change = ConfigAttribute('WINDOW_CHANGE')

    #: the coordinates of living cells in initialization, should be a `list` object.
    #: example: `[[0,0], [1,2]]`
    #: default is `None`
    init_cells = ConfigAttribute('INIT_CELLS')

    #: size of cell in game, type of int
    #: default is `10`
    cell_size = ConfigAttribute('CELL_SIZE')

    #: the distance of the canvas from the top of the window
    #: default is `50`
    canvas_margin_top = ConfigAttribute('CANVAS_MARGIN_TOP')

    #: the distance of the canvas from the left of the window
    #: default is `135`
    canvas_margin_left = ConfigAttribute('CANVAS_MARGIN_LEFT')

    #: color of cell
    #: default is `black`
    cell_color = ConfigAttribute('CELL_COLOR')

    #: background of canvas
    #: default is `white`
    background = ConfigAttribute('BACKGROUND')

    #: default attributes
    default_config = ImmutableDict({
        'DEBUG':                                False,
        'ROW_NUMS':                             50,
        'COLUMN_NUMS':                          50,
        'WINDOW_WIDTH':                         800,
        'WINDOW_HEIGHT':                        600,
        'MARGIN_TOP':                           200,
        'MARGIN_LEFT':                          500,
        'SLEEP_TIME':                           500,
        'WINDOW_CHANGE':                        False,
        'INIT_CELLS':                           None,
        'CELL_SIZE':                            10,
        'CANVAS_MARGIN_TOP':                    50,
        'CANVAS_MARGIN_LEFT':                   135,
        'CELL_COLOR':                           "black",
        'BACKGROUND':                           "white",
    })

    def __init__(self):
        #: title of window
        self.root.title('life game')
        #: current configuration
        self.config = Config(self.default_config)
        self.canvas = None
        self.mapping = None

    def start(self):
        """begin of game"""
        self.init_window()
        self.init_canvas()
        self.init_mapping()
        self.loop_paint()
        self.root.mainloop()

    def init_window(self):
        """initializate window"""
        width = str(self.window_width)
        height = str(self.window_height)
        left = str(self.margin_left)
        top = str(self.margin_top)

        self.root.geometry(''.join([width, 'x', height, '+', left, '+', top]))
        #: if is changeabled the size of window
        is_change = self.window_change
        self.root.resizable(width=is_change, height=is_change)

    def init_canvas(self):
        """initializate canvas"""
        root = self.root
        background = self.background
        left_x = self.canvas_margin_left
        top_y = self.canvas_margin_top
        right_x = self.cell_size*(self.row_nums+1)+self.canvas_margin_left
        bottom_y = self.cell_size*(self.column_nums+1)+self.canvas_margin_top
        width = right_x - left_x
        height = bottom_y - top_y

        self.canvas = Canvas(root, width=width, height=height, bg=background)
        self.canvas.pack()

    def init_mapping(self):
        """initializate map"""
        self.mapping = Mapping(self.column_nums, self.row_nums, self.init_cells, self.debug)

        color = self.get_cell_color()
        for cell in self.get_cells():
            if cell.lived:
                coordins = self.get_cell_position(cell.x_coordin, cell.y_coordin)
                cell.shape_obj = self.canvas.create_rectangle(*coordins, fill=color, outline=color)

    def loop_paint(self):
        """cycle drawing cells"""
        self.mapping.generate_next()
        self.paint()
        sleep_time = self.get_sleep_time()
        self.canvas.after(sleep_time, self.loop_paint)

    def paint(self):
        """draw cells"""
        color = self.get_cell_color()
        for cell in self.get_cells():
            if cell.lived and not cell.shape_obj:
                coordins = self.get_cell_position(cell.x_coordin, cell.y_coordin)
                cell.shape_obj = self.canvas.create_rectangle(*coordins, fill=color, outline=color)

            elif not cell.lived and cell.shape_obj:
                self.canvas.delete(cell.shape_obj)
                cell.shape_obj = None

    def get_sleep_time(self):
        """get timer"""
        return self.sleep_time

    def get_cell_color(self):
        """get color of cell"""
        return self.cell_color

    def get_cell_size(self):
        """get size of cell"""
        return self.cell_size

    def get_canvas_margin_left(self):
        """get the distance of the canvas from the left of window"""
        return self.canvas_margin_left

    def get_canvas_margin_top(self):
        """get the distance of the canvas from the top of window"""
        return self.canvas_margin_top

    def get_cell_position(self, x_coordin, y_coordin):
        """get coordinates of the init cells."""
        size = self.get_cell_size()

        return (
            x_coordin * size,
            y_coordin * size,
            (x_coordin + 1) * size,
            (y_coordin + 1) * size
        )

    def get_cells(self):
        """get all cells"""
        for x_coordin in range(self.mapping.map_x+1):
            for y_coordin in range(self.mapping.map_y+1):
                yield self.mapping.game_map[x_coordin][y_coordin]
