import unittest

from life_game import Mapping, Cell, Game, Config, ConfigAttribute


class TestCell(unittest.TestCase):

    def test_init(self):
        cell = Cell(True, 4, 5)
        self.assertEqual(cell.status, True)
        self.assertEqual(cell.next, False)
        self.assertEqual(cell.x, 4)
        self.assertEqual(cell.y, 5)
        self.assertTrue(isinstance(cell, Cell))

    def test_attr(self):
        cell = Cell(False, 5, 6)
        cell.x = 7
        cell.y = 8
        cell.next = True
        cell.status = False
        self.assertEqual(cell.x, 7)
        self.assertEqual(cell.y, 8)
        self.assertEqual(cell.next, True)
        self.assertEqual(cell.status, False)

    def test_look_up(self):
        mapping = Mapping(5, 5, dot_map=[[0, 1], [1, 0], [1, 2],
                                         [1, 4], [3, 1], [4, 4]])
        game_map = mapping.game_map
        for row in game_map:
            for cell in row:
                cell.look_up(mapping)
                if (cell.x == 0 and cell.y == 1 or
                    cell.x == 1 and cell.y == 1 or
                        cell.x == 2 and cell.y == 1):
                    self.assertEqual(cell.next, True)
                else:
                    self.assertEqual(cell.next, False)


class TestMapping(unittest.TestCase):

    def test_init(self):
        mapping = Mapping(3, 4)
        self.assertEqual(mapping.map_x, 3)
        self.assertEqual(mapping.map_y, 4)
        self.assertEqual(mapping.sleep, 500)
        self.assertEqual(mapping.debug, False)
        self.assertTrue(isinstance(mapping, Mapping))

    def test_init_game_map(self):
        mapping = Mapping(3, 6)
        mapping.init_game_map(5, 4)
        self.assertEqual(mapping.map_x, 5)
        self.assertEqual(mapping.map_y, 4)
        self.assertEqual(len(mapping.game_map), 6)
        for row in mapping.game_map:
            self.assertEqual(len(row), 5)
            for cell in row:
                self.assertTrue(isinstance(cell, Cell))

    def test_init_cells(self):
        mapping = Mapping(3, 4, dot_map=[[0, 1]])
        mapping.init_cells([[0, 1], [2, 3], [1, 0]])
        game_map = mapping.game_map
        for row in game_map:
            for cell in row:
                if (cell.x == 0 and cell.y == 1 or
                    cell.x == 2 and cell.y == 3 or
                        cell.x == 1 and cell.y == 0):
                    self.assertEqual(cell.status, True)
                else:
                    self.assertEqual(cell.status, False)

    def test_generate_next(self):
        mapping = Mapping(5, 5, dot_map=[[0, 1], [1, 0], [1, 2],
                                         [1, 4], [3, 1], [4, 4]])
        mapping.generate_next()
        game_map = mapping.game_map
        for row in game_map:
            for cell in row:
                cell.look_up(mapping)
                if (cell.x == 0 and cell.y == 1 or
                    cell.x == 1 and cell.y == 1 or
                        cell.x == 2 and cell.y == 1):
                    self.assertEqual(cell.status, True)
                else:
                    self.assertEqual(cell.status, False)


class Env(object):
    test = ConfigAttribute('TEST')
    config = {'TEST': 'value'}


class TestConfig(unittest.TestCase):

    def test_init(self):
        config = Config({'a': 1, 'b': 'test'})
        self.assertEqual(config['a'], 1)
        self.assertEqual(config['b'], 'test')
        self.assertTrue(isinstance(config, Config))

    def test_key(self):
        config = Config()
        config['key'] = 'value'
        self.assertTrue('key' in config)

    def test_keyerror(self):
        config = Config()
        with self.assertRaises(KeyError):
            value = config['empty']

    def test_from_object(self):
        config = Config()
        env = Env()
        setattr(env, 'DEBUG', True)
        config.from_object(env)
        self.assertEqual(config['DEBUG'], True)


class TestConfigAttribute(unittest.TestCase):

    def test_init(self):
        ca = ConfigAttribute('test')
        self.assertEqual(ca.__name__, 'test')

    def test_get(self):
        env = Env()
        self.assertEqual(env.test, 'value')

    def test_set(self):
        env = Env()
        setattr(env, 'test', ConfigAttribute('TEST'))
        setattr(env, 'config', {})
        env.test = 'value'
        self.assertEqual(env.test, 'value')


class TestGame(unittest.TestCase):

    def test_init(self):
        game = Game()
        self.assertTrue(isinstance(game.config, Config))
        self.assertEqual(game.debug, False)
        self.assertEqual(game.window_width, 800)
        self.assertEqual(game.window_height, 600)
        self.assertEqual(game.row_nums, 50)
        self.assertEqual(game.column_nums, 50)
        self.assertEqual(game.margin_top, 200)
        self.assertEqual(game.margin_left, 500)
        self.assertEqual(game.sleep_time, 500)
        self.assertEqual(game.window_change, False)
        self.assertEqual(game.init_cells, None)
        self.assertEqual(game.cell_size, 10)
        self.assertEqual(game.canvas_margin_top, 50)
        self.assertEqual(game.canvas_margin_left, 135)

    def test_paint(self):
        pass


if __name__ == '__main__':
    unittest.main()
