from simulation import SnakeSim
from NetworkModule import Agent
from os import system
from time import sleep
import keyboard


loadModel = False

sim = SnakeSim()

agent = Agent(lr=1e-3, gamma=0.96, actions=sim.world.getSnake().actions, epsilon=1, batchSize=128, inputDims=(1,22))

state = sim.getState()

agent.prepNetworksForLoad(state)

if(loadModel):
    agent.loadModel()
    
n=100
scores = []
food = []
matchNumbers = []
qValues = []

for i in range(n):
    if(i == 3000):
        print("Changed epsilonMin to",0.2)
        agent.changeEpsMin(0.2)
    elif(i == 5000):
        print("Changed epsilonMin to",0.1)
        agent.changeEpsMin(0.1)
    elif(i == 7000):
        print("Changed epsilonMin to",0.05)
        agent.changeEpsMin(0.05)
    
    alive = True
    state = sim.getState()
    
    while alive:
        if(keyboard.is_pressed('VK_RIGHT')):
            doPrint = True
        else:
            doPrint = False
        
        # system('cls')
        action,Q = agent.chooseAction(state)
        move = sim.snake.actions[action]
        qValues.append(Q)
        reward, state_, alive = sim.step(move)
        agent.storeTransition(state, action, reward, state_, alive)
        
        state = state_
        agent.learn()
        # sleep(0.3)
        if doPrint:
            system('cls')
            sim.world.printWorld()
            sleep(0.1)
    
    score = sim.getScore()
    scores.append(score)
    food.append(sim.getFoodEaten())   
    matchNumbers.append(i)
    print("----------------")
    print("Game %i ended." % i)
    print("Score: %i" % scores[i])
    print("Food: %i" % food[i])
    print("----------------\n")
     
    
    
 
        
        
    sim.resetGame()

inp = input("Save model (y/n): ").lower()
if(inp == "y"):
     agent.saveModel()


