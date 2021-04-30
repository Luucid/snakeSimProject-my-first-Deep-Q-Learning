import tensorflow as tf
import tensorflow.keras as keras
import numpy as np



class DQN(keras.Model): #deep Q network
    def __init__(self):
        super(DQN, self).__init__()
        self.input = tf.keras.layers.Flatten(input_shape=(8, 4))
        self.dense1 = tf.keras.layers.Dense(8, activation=tf.nn.sigmoid)
        self.dense2 = tf.keras.layers.Dense(8, activation=tf.nn.sigmoid)
        self.dense3 = tf.keras.layers.Dense(8, activation=tf.nn.sigmoid)
        self.output = tf.keras.layers.Dense(32, activation=tf.nn.linear)
        # self.dropout = tf.keras.layers.Dropout(0.5)

    def call(self, inputs, training=False):
        x = self.dense1(inputs)
        if training:
          x = self.dropout(x, training=training)
        return self.dense2(x)





class Agent:
    def __init__(self):
        self.gamma = 0.92
        self.eGreed = 0.1
        self.prob = 1 - self.eGreed
        self.N = 100000 
        self.memory #memory[e_0, e_1, e_2, ... ,e_n]
        
        self.qna = DQN()
        self.qnb = DQN()

    def action(self):
        pass
     
    def reward(self, s, a):
        pass
    
    def sumPQ(self):
        pass
    
    #optimal action-value function   
    def optimalQ(self, s, a): 
        pass
    
    def updateMemory(self, experience):
        if(len(self.memory >= self.N)):
            self.memory[np.random.rand(0, self.N)] = experience
        else:
            np.append(experience,self.memory)
        
   

    def getMemoryBatch(self, n=64):
        batch = np.array([np.zeros(4)]*n)
        for i in range(n):
            rndMem = self.memory[np.random.randint(0, self.N)]       
            batch[i] = rndMem
        return batch 
    

    def getAction(self):
        pass
    
    
    def deepQlearn(self, matches):
        done = False
        for i in range(matches):
            #init sequence and preprocessed sequence
            at = 0
            rt = 0
            st = 0
            sn = 0
            while not done:
                
                if np.random.random() < self.prob:
                    experience = np.array([st, at, rt, sn])
                else:
                    pass
                    
                    
                
            
    
    
    