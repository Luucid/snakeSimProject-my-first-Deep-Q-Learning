from simulation import SnakeSim
from NetworkModule import Agent
from os import system
from time import sleep
import keyboard
import matplotlib.pyplot as plt
import numpy as np

loadModel = False
eps = 1
if loadModel:
    eps = 0.2


sim = SnakeSim()




agent = Agent(fname='Q5wStoneSuperFruit', lr=1e-3, gamma=0.97, actions=sim.world.getSnake().actions, epsilon=eps, batchSize=128, inputDims=(1,36))
state = sim.getState()
agent.prepNetworksForLoad(state)

if(loadModel):
    agent.loadModel()
    
n = 1000000
scores = []
water = []
mouse = []
special = []
rocks = []
rocksPower = []
matchNumbers = []
qValues = []

doPrint = True

for i in range(n):
    if(i == 1000):
        print("Changed epsilonMin to",0.2)
        agent.changeEpsMin(0.2)
    elif(i == 2000):
        print("Changed epsilonMin to",0.1)
        agent.changeEpsMin(0.1)
    elif(i == 5000):
        print("Changed epsilonMin to",0.05)
        agent.changeEpsMin(0.05)
    elif(i == 25000):
        print("Changed epsilonMin to",0.005)
        agent.changeEpsMin(0.005)
    
    
    alive = True
    state = sim.getState()
    
    while alive:
        if(keyboard.is_pressed('p')):
            sleep(0.5)
            doPrint = not doPrint
        
        
    
        action,Q = agent.chooseAction(state)
        move = sim.snake.actions[action]
        qValues.append(Q)
        reward, state_, alive = sim.step(move)
        agent.storeTransition(state, action, reward, state_, alive)
        
        state = state_
        agent.learn()

        if doPrint:
            system('cls')
            sim.world.printWorld()
            print("\n-snakeView-\n")
            sim.snake.printView()
            # sleep(2)
            sleep(0.04)
    
        
    
    # score = sim.getScore()
    # scores.append(score)
    water.append(sim.getWaterEaten())   
    mouse.append(sim.getMiceEaten())   
    special.append(sim.getSpecialEaten())
    rocks.append(sim.getRocksCrushed(power=False))
    rocksPower.append(sim.getRocksCrushed(power=True))
    matchNumbers.append(i)
    print("----------------")
    print("Game %i ended." % i)
    # print("Q: %i" % qValues[i])
    print("Water: %i" % water[i])
    print("Mouse: %i" % mouse[i])
    print("special: %i" % special[i])
    print("rocks with power: %i" % rocksPower[i])
    print("rocks without power: %i" % rocks[i])
    print("----------------\n")
    if(keyboard.is_pressed("Esc")):
            break
    sim.resetGame()

inp = input("Save model (y/n): ").lower()
if(inp == "y"):
     agent.saveModel()

# x = np.arange(len(scores))
x1 = np.arange(len(water))
x2 = np.arange(len(mouse))
x3 = np.arange(len(special))

plt.plot(x1, water, '-b', alpha=0.7)
plt.plot(x2, mouse, '-r', alpha=0.7)
plt.plot(x3, special, '-g', alpha=0.7)
plt.show()