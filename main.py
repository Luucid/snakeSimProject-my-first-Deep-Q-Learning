from simulation import SnakeSim
from NetworkModule import Agent
from os import system
from time import sleep
import keyboard


loadModel = True
sim = SnakeSim()

agent = Agent(lr=1e-3, gamma=0.97, actions=sim.world.getSnake().actions, epsilon=0.4, batchSize=128, inputDims=(1,22))
state = sim.getState()
agent.prepNetworksForLoad(state)

if(loadModel):
    agent.loadModel()
    
n=5000
scores = []
food = []
mouse = []
matchNumbers = []
qValues = []

doPrint = False

for i in range(n):
    if(i == 1000):
        print("Changed epsilonMin to",0.2)
        agent.changeEpsMin(0.2)
    elif(i == 2000):
        print("Changed epsilonMin to",0.1)
        agent.changeEpsMin(0.1)
    elif(i == 3000):
        print("Changed epsilonMin to",0.05)
        agent.changeEpsMin(0.05)
    
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


