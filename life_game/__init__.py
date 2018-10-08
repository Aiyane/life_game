"""
package: life_game
life_game.Mapping: game map
life_game.Game: Game
life_game.Control: game control
life_game.mapping.Cell: cell
life_game.config.Config: configuration
life_game.config.ConfigAttribute: Config Attribute
life_game.immutable_dict.ImmutableDict: ImmutableDict
"""
from life_game.basic_units import Mapping
from life_game.game import Game
from life_game.control import Control

__all__ = ['Mapping', 'Game', 'Control']
