import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.optimizers as kOptimizers
import keyboard
import numpy as np
from time import sleep
##learn and replayBuffer inspired by RunarEckholdt @ github

class DQN(keras.Model): #deep Q network
    def __init__(self, nActions, inputShape):
        super(DQN, self).__init__()
        self.nActions = nActions
        self.inputShape = inputShape  
        
        self.inputLayer = tf.keras.layers.Flatten(input_shape=self.inputShape, dtype=np.int32)
        
        self.dense1 = tf.keras.layers.Dense(512, activation='sigmoid')
        self.dense2 = tf.keras.layers.Dense(256, activation='sigmoid')
        self.dense3 = tf.keras.layers.Dense(128, activation='sigmoid')
        self.dense4 = tf.keras.layers.Dense(64, activation='sigmoid')
        self.dense5 = tf.keras.layers.Dense(32, activation='sigmoid')
        
        self.outputLayer = tf.keras.layers.Dense(self.nActions, activation='linear')
        

    def call(self, state):
        x = self.inputLayer(state)
        
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.dense4(x)
        x = self.dense5(x) 
        
        x = self.outputLayer(x)
        return x
        




class ReplayBuffer():
    def __init__(self, maxSize, inputShape):
        self.memSize = maxSize
        self.memCntr = 0
        self.stateMemory = np.zeros((self.memSize,*inputShape),dtype=np.float32)
        self.newStateMemory = np.zeros((self.memSize,*inputShape),dtype=np.float32)
        
        self.actionMemory = np.zeros(self.memSize,dtype=np.int32)
        self.rewardMemory = np.zeros(self.memSize,dtype=np.int32)
        self.terminalMemory = np.zeros(self.memSize,dtype=np.bool)
        
        
    def storeTransition(self,state, action,reward,state_,alive):
        index = self.memCntr % self.memSize
               
        self.stateMemory[index] = state
        self.newStateMemory[index] = state_
        self.rewardMemory[index] = reward
        self.actionMemory[index] = action
        self.terminalMemory[index] = not alive
        
        if(keyboard.is_pressed('r')):
            print("reward: ", reward)
            sleep(0.2)
        
        self.memCntr += 1
    
    def sampleBuffer(self, batchSize):
        maxMemory = min(self.memCntr, self.memSize)
        batch = np.random.choice(maxMemory,batchSize,replace=False)
        states = self.stateMemory[batch]
        newStates = self.newStateMemory[batch]
        actions = self.actionMemory[batch]
        rewards = self.rewardMemory[batch]
        done = self.terminalMemory[batch]
        
        return states,actions,rewards,newStates,done
  





class Agent:
    def __init__(self, lr, gamma, actions, epsilon, 
                 batchSize, inputDims, epsilonDec=1e-4,
                 epsilonMin=0.01,fname='dqn' ,memSize=10000, replace=100):
        
        self.actionSpace = np.array([0, 1, 2])
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonDec = epsilonDec
        self.epsilonMin = epsilonMin
        self.replace = replace
        self.batchSize = batchSize
        self.memory = ReplayBuffer(memSize, inputDims)
        self.learnStepCounter = 0
        self.qEval = DQN(len(actions),inputDims)
        self.qNext = DQN(len(actions),inputDims)

        self.qEval.compile(optimizer=kOptimizers.Adam(learning_rate=lr),loss='mean_squared_error')
        self.qNext.compile(optimizer=kOptimizers.Adam(learning_rate=lr),loss='mean_squared_error')
        
        self.fname = fname



    def storeTransition(self, state, action, reward, newState, done):
        self.memory.storeTransition(state, action, reward, newState, done)

    def chooseAction(self, observation):
        state = np.array([observation])
        networkActionQ = self.qEval(state)[0]
        networkAction = tf.math.argmax(networkActionQ).numpy()
       
       
        
        if(np.random.random() < self.epsilon): 
            if self.epsilon < 0.5:
                action = np.random.choice(self.actionSpace[self.actionSpace != networkAction]) #make sure all choices amount to 100%
            else:
                action = np.random.choice(self.actionSpace) #give exploring more freedom in the beginning  
        else:  
            state = np.array([observation])
            action = networkAction
            

        if(keyboard.is_pressed('.')):
            print("networkAction: ", networkAction, " | choosen action: ", action)
            sleep(0.2)
        return action,networkActionQ.numpy()[action]



    def learn(self):
        if(self.memory.memCntr < self.batchSize):
            return
        
        
        #if it has learned x amount of times, put main network's weights into the qNext network
        if(self.learnStepCounter % self.replace == 0):
            #print(self.qEval.get_weights())
            self.qNext.set_weights(self.qEval.get_weights())
        
        
        states,actions,rewards,states_, dones = self.memory.sampleBuffer(self.batchSize)
        

        #predicting future rewards
        qNext = self.qNext(states_)
        
        # print(qNext)
        #getting the maximum reward from each state reward prediction
        qNext = tf.math.reduce_max(qNext, axis=1, keepdims=True).numpy()
        # print(qNext)
        # sleep(100)
        
        #predictiong q values for states before action
        qTarget = self.qEval(states).numpy()
        
        
        
        
        #itterates over each sample changing the q value for each action done
        # to be de possible best outcome of future actions
        for idx,terminal in enumerate(dones):
            # print(idx, terminal)
            if terminal:
                qNext[idx] = 0.0
            qTarget[idx][actions[idx]] = rewards[idx] + self.gamma*qNext[idx]
            # print(qTarget[idx][actions[idx]])
        
        
        self.qEval.train_on_batch(states,qTarget)
        
        # self.epsilon = self.epsilon - self.epsilonDec if self.epsilon > self.epsilonMin else self.epsilonMin
        if self.epsilon > self.epsilonMin:
            self.epsilon -=  self.epsilonDec
        
        self.learnStepCounter += 1
        if(keyboard.is_pressed('e')):
            print("epsilon: ", self.epsilon)
            sleep(0.2)
        
   
    def saveModel(self):
        self.qEval.save_weights(self.fname,save_format="tf")
        
    def prepNetworksForLoad(self,observation):
        observation = np.array([observation])
        self.qEval(observation)
        self.qNext(observation)
        
    def loadModel(self):
        self.qEval.load_weights(self.fname)
       
        
        
    def changeEpsMin(self,value):
        self.epsilonMin = value















    
   
                    
                    
                
            
    
    
    