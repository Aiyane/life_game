"""
模块：life_game
life_game.Mapping: 游戏地图
life_game.Game: 游戏本身
life_game.Control: 游戏控制
life_game.mapping.Cell: 细胞
life_game.config.Config: 配置
life_game.config.ConfigAttribute: 配置参数
life_game.immutable_dict.ImmutableDict: 不可变字典
"""
from life_game.mapping import Mapping
from life_game.game import Game
from life_game.control import Control

__all__ = ['Mapping', 'Game', 'Control']
