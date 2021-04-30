from GameClass import Game
# from NetworkModule import Agent

# from GameClass import trainPack
# agent = Agent()

game = Game()
# game.startGame()

session = []

matches = 10000
# for i in range(matches):
game.startGame()
while(game.getStatus):
    # agent.updateMemory(game.tick())
    # print(game.nextMove())
    session.append(game.nextMove())
#do someting clever.
print(session)
    



