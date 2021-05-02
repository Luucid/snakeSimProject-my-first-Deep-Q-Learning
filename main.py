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




agent = Agent(fname='qtest', lr=1e-3, gamma=0.97, actions=sim.world.getSnake().actions, epsilon=eps, batchSize=128, inputDims=(1,22))
state = sim.getState()
agent.prepNetworksForLoad(state)

if(loadModel):
    agent.loadModel()
    
n = 1000000
scores = []
food = []
mouse = []
matchNumbers = []
qValues = []

doPrint = False

for i in range(n):
    # if(i == 1000):
    #     print("Changed epsilonMin to",0.2)
    #     agent.changeEpsMin(0.2)
    # elif(i == 2000):
    #     print("Changed epsilonMin to",0.1)
    #     agent.changeEpsMin(0.1)
    # elif(i == 10000):
    #     print("Changed epsilonMin to",0.05)
    #     agent.changeEpsMin(0.05)
    if(i == 25000):
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
            # sleep(3)
            sleep(0.02)
    
        
    
    score = sim.getScore()
    scores.append(score)
    food.append(sim.getFoodEaten())   
    mouse.append(sim.getMiceEaten())   
    matchNumbers.append(i)
    print("----------------")
    print("Game %i ended." % i)
    print("Score: %i" % scores[i])
    print("Water: %i" % food[i])
    print("Mouse: %i" % mouse[i])
    print("----------------\n")
    if(keyboard.is_pressed("Esc")):
            break
    sim.resetGame()

inp = input("Save model (y/n): ").lower()
if(inp == "y"):
     agent.saveModel()

x = np.arange(len(scores))
x1 = np.arange(len(food))
x2 = np.arange(len(mouse))

plt.plot(x, scores, '-b', alpha=0.7)
plt.plot(x1, food, '-r', alpha=0.7)
plt.plot(x2, mouse, '-g', alpha=0.7)
plt.show()