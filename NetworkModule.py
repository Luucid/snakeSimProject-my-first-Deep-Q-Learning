import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.optimizers as kOptimizers

import numpy as np

try:
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
  # Invalid device or cannot modify virtual devices once initialized.
  pass

class DQN(keras.Model): #deep Q network
    def __init__(self, nActions, inputShape):
        super(DQN, self).__init__()
        self.nActions = nActions
        self.inputShape = inputShape  
        
        self.inputLayer = tf.keras.layers.Flatten(input_shape=self.inputShape, dtype=np.int32)
        
        self.dense1 = tf.keras.layers.Dense(128, activation='sigmoid')
        self.dense2 = tf.keras.layers.Dense(128, activation='sigmoid')
        self.dense3 = tf.keras.layers.Dense(64, activation='sigmoid')
        
        self.outputLayer = tf.keras.layers.Dense(self.nActions, activation='linear')
        

    def call(self, state):
        # print("in call: \n\n")
        x = self.inputLayer(state)
        # print("inputLayer: ", x)
        x = self.dense1(x)
        # print("dense1: ", x)
        x = self.dense2(x)
        # print("dense2: ", x)
        x = self.dense3(x)
        # print("dense3: ", x)
        x = self.outputLayer(x)
        # print("outputLayer: ", x)
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
        
        # print(reward)
        # print(index)
        # print(state)
        
        self.stateMemory[index] = state
        self.newStateMemory[index] = state_
        self.rewardMemory[index] = reward
        self.actionMemory[index] = action
        self.terminalMemory[index] = not alive
        
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
                 batchSize, inputDims, epsilonDec=1e-3,
                 epsilonMin=0.01 ,memSize=10000, replace=100):
        
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




    def storeTransition(self, state, action, reward, newState, done):
        self.memory.storeTransition(state, action, reward, newState, done)

    def chooseAction(self, observation):
        state = np.array([observation])
        networkActionQ = self.qEval(state)[0]
        networkAction = tf.math.argmax(networkActionQ).numpy()
        # networkAction = 
       
        
        if(np.random.random() < self.epsilon):
            #chose random action that is not the same as networkAction
            action = np.random.choice(self.actionSpace[self.actionSpace != networkAction])
            # print("rand action: ",action)
        else:
            state = np.array([observation])
            action = networkAction
            #actions = self.qEval(net)
            # print("network action: ",action)
            # action = tf.math.argmax(actions,axis=1).numpy()[0]

        
            
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
        
        
        #getting the maximum reward from each state reward prediction
        qNext = tf.math.reduce_max(qNext, axis=1, keepdims=True).numpy()
        
        #predictiong q values for states before action
        qTarget = self.qEval(states).numpy()
 
        
        #itterates over each sample changing the q value for each action done
        # to be de possible best outcome of future actions
        for idx,terminal in enumerate(dones):
            #print(idx)
            if terminal:
                qNext[idx] = 0.0
            qTarget[idx][actions[idx]] = rewards[idx] + self.gamma*qNext[idx]
        
        
        self.qEval.train_on_batch(states,qTarget)
        
        self.epsilon = self.epsilon - self.epsilonDec if self.epsilon > self.epsilonMin else self.epsilonMin
        
        self.learnStepCounter += 1
        
   
    def saveModel(self):
        self.qEval.save_weights(self.fname,save_format="tf")
        
    def prepNetworksForLoad(self,observation):
        observation = np.array([observation])
        self.qEval(observation)
        self.qNext(observation)
        
    def loadModel(self):
        #print("Before loading: \n")
        #print(self.qEval.get_weights())
        self.qEval.load_weights(self.fname)
        #print("\n\n\n After loading: \n")
        #print(self.qEval.get_weights())
        #self.qNext.set_weights(self.qEval.get_weights())
        
        
        
    def changeEpsMin(self,value):
        self.epsilonMin = value















    
    # def action(self):
    #     pass
     
    # def reward(self, s, a):
    #     pass
    
    # def sumPQ(self):
    #     pass
    
    # #optimal action-value function   
    # def optimalQ(self, s, a): 
    #     pass
    
    # def updateMemory(self, experience):
    #     print(experience)
    #     if(len(self.memory >= self.N)):
    #         self.memory[np.random.rand(0, self.N)] = experience
    #     else:
    #         np.append(experience,self.memory)
        
   

    # def getMemoryBatch(self, n=64):
    #     batch = np.array([np.zeros(4)]*n)
    #     for i in range(n):
    #         rndMem = self.memory[np.random.randint(0, self.N)]       
    #         batch[i] = rndMem
    #     return batch 
    

    # def getAction(self):
    #     pass
    
    
    # def deepQlearn(self, matches):
    #     done = False
    #     for i in range(matches):
    #         #init sequence and preprocessed sequence
    #         at = 0
    #         rt = 0
    #         st = 0
    #         sn = 0
    #         while not done:
                
    #             if np.random.random() < self.prob:
    #                 experience = np.array([st, at, rt, sn])
    #             else:
    #                 pass
                    
                    
                
            
    
    
    