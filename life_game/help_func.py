"""
Game 和 Control 类需要的一些方法
"""

def get_sleep_time(game, sleep_time):
    """获取定时器"""
    if hasattr(game, 'get_sleep_time'):
        return game.get_sleep_time()
    return sleep_time

def get_cell_color(game, cell_color):
    """获取细胞颜色"""
    if hasattr(game, 'get_cell_color'):
        return game.get_cell_color()
    return cell_color

def get_cell_size(game, cell_size):
    """获取细胞大小"""
    if hasattr(game, 'get_cell_size'):
        return game.get_cell_size()
    return cell_size

def get_canvas_margin_left(game, canvas_margin_left):
    """获取画布左边距"""
    if hasattr(game, 'get_canvas_margin_left'):
        return game.get_canvas_margin_left()
    return canvas_margin_left

def get_canvas_margin_top(game, canvas_margin_top):
    """获取画布上边距"""
    if hasattr(game, 'get_canvas_margin_top'):
        return game.get_canvas_margin_top()
    return canvas_margin_top

def get_cell_position(control_or_game, x_coordin, y_coordin):
    """获取细胞坐标"""
    if hasattr(control_or_game, 'game'):
        game = control_or_game.game
    else:
        game = control_or_game

    size = get_cell_size(game, game.cell_size)
    left = get_canvas_margin_left(game, game.canvas_margin_left)
    top = get_canvas_margin_top(game, game.canvas_margin_top)

    return (
        x_coordin * size + left,
        y_coordin * size + top,
        (x_coordin + 1) * size + left,
        (y_coordin + 1) * size + top
    )
