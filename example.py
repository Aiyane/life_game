from life_game import Game
import settings

game = Game()
game.config.from_object(settings)
game.start()
