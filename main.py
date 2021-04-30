from simulation import SnakeSim
from NetworkModule import Agent
from os import system
from time import sleep





sim = SnakeSim()

agent = Agent(gamma=0.96, actions=sim.world.getSnake().moves, epsilon=0.1, batchSize=128, inputDims=(3,8))

n=100


for i in range(n):
    while sim.gameTick():
        agent.updateMemory(sim.getMemory())
        sleep(0.1)
        system('cls')
    sim.resetGame()
    



