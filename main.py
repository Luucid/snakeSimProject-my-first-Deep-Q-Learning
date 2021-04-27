from GameClass import Game
from GameClass import winTrack
# import tensorflow as tf
# import tensorflow.keras as keras
from time import sleep
# from GameClass import trainPack


# game = Game(True)
# game.startGame()


matches = 10000
for i in range(matches):
    # print("iteration: %i" % i)
    if(i%100 == 0):
        print(i)
    
    game = Game()
    game.startGame()
    
print(winTrack)


