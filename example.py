from life_game import Game, Control
import settings

game = Game()
game.config.from_object(settings)
control = Control(game)
control.start()
