import time


class Control(object):
    def __init__(self, game):
        self.game = game
        self.is_continue = True

    def pause(self):
        self.is_continue = False
    
    def go(self):
        self.is_continue = True
    
    def start(self):
        self.game._start()
        self.game._paint()
        self.control()
        self.game.root.mainloop()
    
    def control(self):
        time.sleep(self.game.mapping.sleep/10000)
        if self.is_continue:
            self.game._paint()
        self.game.cv.after(self.game.mapping.sleep, self.control)
