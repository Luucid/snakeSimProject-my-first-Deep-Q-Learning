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


agent = Agent(fname='tmp', lr=1e-3, gamma=0.987654321, actions=sim.world.getSnake().actions, epsilon=eps, batchSize=128, inputDims=(1,43))
state = sim.getState()
agent.prepNetworksForLoad(state)

if(loadModel):
    agent.loadModel()
    
n = 250000
scores = []
water = []
mouse = []
special = []
score = []
matchNumbers = []
qValues = []
epsVal = []
bestScore = 0

demo = []

doPrint = False

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
        print("Changed epsilonMin to",0.01)
        agent.changeEpsMin(0.01)
    
    
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
            # print("\n-snakeView-\n")
            # sim.snake.printView()
            # sleep(2)
            sleep(0.04)

    epsVal.append(agent.epsilon)
    water.append(sim.getWaterEaten())   
    mouse.append(sim.getMiceEaten())   
    special.append(sim.getSpecialEaten())
    score.append(sim.getScore())
    matchNumbers.append(i)
    if (water[i]+mouse[i]+special[i]) > bestScore:
        bestScore = water[i]+mouse[i]+special[i]
        demo = sim.getReplay()
    
    if(keyboard.is_pressed('v')):
            inp = input("plot Qvalues so far? (y/n): ").lower()
            if(inp == "y"):
               x = np.arange(len(qValues))
               plt.plot(x, qValues, '.b', alpha=0.1)
               plt.show() 
                
           
    
    if i % 100 == 0:
        system('cls')
        
    print("----------------")
    print("Game %i ended." % i)
    # print("Q: %i" % qValues[i])
    print("Water: %i" % water[i])
    print("Mouse: %i" % mouse[i])
    print("special: %i" % special[i])
    print("score: %i" % score[i])
    print("----------------\n")
    if(keyboard.is_pressed("Esc")):
            break
    sim.resetGame()



x = np.arange(len(qValues))
plt.plot(x, qValues, '.b', alpha=0.1)
    
plt.show()


inp = input("Save model (y/n): ").lower()
if(inp == "y"):
    name = input("enter modelName: ")
    agent.saveModel(name)


# epsVal = np.flip(epsVal, 0)



# plt.plot(x, water, '.b', alpha=0.7)
# plt.plot(x, mouse, '.r', alpha=0.7)
# plt.plot(x, special, '.g', alpha=0.7)

# plt.xlabel("rounds")


inp = input("View best run replay? (y/n): ").lower()
if(inp == "y"):
    blockVisual = {0:'░', 1:'█', 2:'҈',7:'ꝏ', 8:'ѽ',9:'ϕ', 16:'●', 17:'•', 18:'░'}
    for frame in demo:
        system('cls')
        for row in frame:
            for tile in row:
                print(blockVisual[tile], end=' ')
            print("")
        sleep(0.04)
else:
    pass
    


