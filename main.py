from GameClass import Game
from time import sleep



matches = 10
for i in range(matches):
    game = Game()
    game.startGame()
    sleep(3)