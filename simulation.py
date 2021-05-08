import numpy as np
from time import sleep



class GameMap():
    def __init__(self, x=16, y=16, stoneChance=0.0):
        self.__worldBlocks = {'ground':0, 'stone':1, 'pit':2, 'specialFruit':7,'water':8,'mouse':9, 'snakeHead':16, 'snakeTail':17, 'snakeEyes':18}
        self.blockVisual = {0:'░', 1:'█', 2:'҈',7:'ꝏ', 8:'ѽ',9:'ϕ', 16:'☻', 17:'•', 18:'░'}
        self.__stoneChance = stoneChance
        
      
        self.__animalList = []
        self.__snake = 0
        self.__height = y
        self.__width = x
        self.__map = np.zeros((y, x))
        self.__generateWorld()
        self.replay = [np.copy(self.__map)]
        
      
        
        
    def __generateWorld(self):
        for y in range(self.__height):
            for x in range(self.__width):
                
                ########################################################
                ###################spawn map borders####################
                ########################################################
                
                if y <= 1 or y >= self.__height-2:
                    self.__map[y][x] = self.__worldBlocks['pit']
                elif x <= 1 or x >= self.__width-2:
                    self.__map[y][x] = self.__worldBlocks['pit']
                
                ######################################################## 
                ###################spawn ground and rocks####################
                ########################################################
                
                else:
                    if np.random.random() < self.__stoneChance:
                        self.__map[y][x] = self.__worldBlocks['stone']
                    else:
                        self.__map[y][x] = self.__worldBlocks['ground']                      
                
     
    
    def spawnAnimal(self, animal):
        self.__animalList.append(animal)
        self.moveAnimal(animal)
    
    def spawnSnake(self, snake):
        self.__snake = snake
        self.moveSnake()
    
         
    def getBlock(self, block):
        return self.__worldBlocks[block]
    
    def getSnake(self):
        return self.__snake
        # return self.__animalList[0]
    
    def prepSnakeForMove(self):
        snakeHead = self.__snake.getPos('head') 
        snakeBody = self.__snake.getPos('body')
        self.setTile(snakeHead, 'ground')
        for part in snakeBody:
            self.setTile(part, 'ground')
    
    # def moveAnimal(self, animal, setGround=False):
    #     animalHead = animal.getPos('head')
    #     if setGround:
    #         self.setTile(animalHead, 'ground')
    #     else:
    #         self.setTile(animalHead, animal.getAnimal('head'))
            
    #     if animal.hasBody:
    #         animalBody = animal.getPos('body')
    #         for part in animalBody:
    #             if setGround:
    #                 self.setTile(part, 'ground')
    #             else:
    #                 self.setTile(part, animal.getAnimal('body'))
    
    
    def moveSnake(self):
        snakeHead = self.__snake.getPos('head') 
        snakeBody = self.__snake.getPos('body')
        self.setTile(snakeHead, 'snakeHead')
        for part in snakeBody:
            self.setTile(part, 'snakeTail')
        
                    
                    
        
    
    def addFood(self, n, kind='water'):
        for i in range(n):
            xFood = np.random.randint(1, self.__width-1)
            yFood = np.random.randint(1, self.__height-1)
            
            while self.__map[yFood][xFood] != self.__worldBlocks['ground']:
                xFood = np.random.randint(1, self.__width-1)
                yFood = np.random.randint(1, self.__height-1)
            self.__map[yFood][xFood] = self.__worldBlocks[kind]

     

        
    def printWorld(self):
    
        print("HP: ", self.__snake.getHealth(), " | body: ", self.__snake.getBodySize())
        print("")
        for y, row in enumerate(self.__map):
            for x, tile in enumerate(row):                                       
                print(self.blockVisual[tile], end=' ')
            print("")
            
    
        
    
        
             
                     
    def getTile(self, x, y):
        return self.__map[y][x]
    
    def setTile(self, pos, tile):
        self.__map[pos[1]][pos[0]] = self.__worldBlocks[tile]
    
    def setVision(self, pos, tile):
        
        if pos[0] < self.__width and pos[0] > 0 and pos[1] < self.__height and pos[1] > 0:
            if self.__map[pos[1]][pos[0]] == self.getBlock('ground'):
                self.__map[pos[1]][pos[0]] = self.__worldBlocks[tile]
        
    def updateWorld(self, action): 
        self.__snake.move(action)
        self.moveSnake()
        self.replay.append(np.copy(self.__map))
        return self.__snake.alive





class Sight():
    def __init__(self, world, sFov=5, sRange=8):
        self.__sFov = sFov   #width of vision
        self.__sRange = sRange #n tiles visible forward
        self.__view = np.zeros((sRange, sFov))
        self.__leftMidRight = np.array([0, 0, 0, 0, 0])
        # self.__leftMidRight = np.array([0, 0, 0])
        # self.coordView = np.array([[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]]*sRange)
        self.world = world

 
        
    
    def getView(self):
        return self.__view
    
    
    def setLeftMidRight(self, vision, pos, ori):
        #if horizontal, vision == 1, else vision == 0.  0-1 = -1, since only two pos in pos, -1 == last element. 
        if vision == 1: #horizontal
            self.__leftMidRight[0] = pos - ori*2
            self.__leftMidRight[1] = pos - ori
            self.__leftMidRight[2] = pos
            self.__leftMidRight[3] = pos + ori
            self.__leftMidRight[4] = pos + ori*2
        else:   
            self.__leftMidRight[4] = pos - ori*2
            self.__leftMidRight[3] = pos - ori
            self.__leftMidRight[2] = pos
            self.__leftMidRight[1] = pos + ori
            self.__leftMidRight[0] = pos + ori*2

        
    def updateView(self, pos, ori, world):
        
        getDir = [True, True, True, True, True]     
        vision = abs(ori[0])
        
        
        self.setLeftMidRight(vision, pos[vision], ori[vision-1])
 
        tmpMid = pos[vision-1]
        for y, row in enumerate(self.__view):
            for i in range(self.__sFov):
                # print(self.__view, "\n\n")
                if getDir[i]:      
                    
                    if vision == 1:
                        self.__view[y][i] = world.getTile(tmpMid, self.__leftMidRight[i])
                        # self.coordView[y][i] = np.array([tmpMid, self.__leftMidRight[i]])
                    else:
                        self.__view[y][i] = world.getTile(self.__leftMidRight[i], tmpMid)  
                        # self.coordView[y][i] = np.array([self.__leftMidRight[i], tmpMid])
                    
                    if self.__view[y][i] == world.getBlock('pit'):
                        getDir[i] = False
                else:
                    self.__view[y][i] = world.getBlock('pit')                    
            tmpMid += ori[vision-1]  
        # print("here?")
        
        
        
          
class RewardSystem():
    def __init__(self):
        self.rewards = {'mouse':200, 'water':150, 'ground': -0.1, 'specialFruit':300, 'stone':-200, 'pit':-10000, 'snakeTail':-100000 }
        self.tiles = { 0:'ground', 1:'stone', 2:'pit', 7:'specialFruit', 8:'water',9:'mouse', 16:'snakeHead', 17:'snakeTail' }
        self.consumed = {'mouse':0, 'water':0, 'specialFruit':0}
        self.lastReward = 0
        self.score = 0
        
    def calcReward(self, tile): 
        if tile in self.tiles:
            self.lastReward = self.rewards[self.tiles[tile]]
            if self.tiles[tile] in self.consumed:
                self.consumed[self.tiles[tile]] += 1            
        self.score = sum(self.consumed.values())  
        return self.lastReward, self.score
                
        
            

class Snake():
    def __init__(self, x, y, world):
        
        ######################World########################
        
        self.actions = np.array([3, 0, 1])
        self.headVisual = ['▲','►','▼','◄']
        self.__legalMoves = {3:'left', 0:'forward', 1:'right'}
 
        self.__navigator = Position(x, y)
        self.__world = world
        self.rewards = RewardSystem()
        self.lastReward = self.rewards.lastReward
        self.score = self.rewards.score
        
        ######################health########################
        
        self.__health = 100 #train on achieving highest HP 
        self.bestHp = self.__health  
        self.__hpUpgrade = 200
        self.__hpDowngrade = 100
        
        #######################body#########################
        
        self.__head = self.__navigator.getPos()
        self.__body = np.array([self.__navigator.getPos() - self.__navigator.getOri()])
        self.bodyParts = 1
        
        self.sight = Sight(world)
        self.sight.updateView(self.__head, self.__navigator.getOri(), world)     
        self.__currentView = self.sight.getView()
      
        self.hasBody = True
        self.alive = True
        

        
    def getBodySize(self):
        return self.bodyParts

    def updateView(self):
       self.sight.updateView(self.__head, self.__navigator.getOri(), self.__world)
       self.__currentView = self.sight.getView()
       self.__world.blockVisual[16] = self.headVisual[self.__navigator.getdirectionIdx()]
       # self.__world.printWorld()
       # sleep(2)
       
     
       
    def checkIfUpgrade(self, bodyPart):
        if self.__health >= self.__hpUpgrade:
            self.__hpDowngrade += 100
            self.__hpUpgrade += 100
            self.addTail(bodyPart)
        
        elif (self.__health < self.__hpDowngrade) and (self.__health > 100):
            self.__hpDowngrade -= 100
            self.__hpUpgrade -= 100
            self.removeTail()
        
    
    def move(self, action):        
        
        direction = action
        bodyLength = len(self.__body)
        for b in self.__body:
            self.__world.setTile(b, 'ground')
        if bodyLength > 1:    
            i = bodyLength-1
            while i > 0:            
                self.__body[i] = self.__body[i-1]
                i -= 1  
         
        self.__body[0] = self.__head
        for b in self.__body:
            self.__world.setTile(b, 'snakeTail')    
        
        self.__navigator.update(self.__legalMoves[direction])
        self.__head = self.__navigator.getPos()
       
     
        ##############################################################################
        self.lastReward, self.score = self.rewards.calcReward(self.__world.getTile(self.__head[0], self.__head[1]))  
        self.__health += self.lastReward
        self.checkIfUpgrade(self.__body[-1])
        # self.calcReward(self.__body[-1], self.__world.getTile(self.__head[0], self.__head[1]))  
            
        if self.__health <= 0:
            self.alive = False
        else:
            self.updateView()
        
        ##############################################################################
        
       
          
    
    def addTail(self, pos):
        self.lastReward += 100
        self.__body = np.append(self.__body, [pos], axis=0)
        self.__world.setTile(self.__body[-1], 'snakeTail')
        self.bodyParts = len(self.__body)

    def removeTail(self):
        self.lastReward -= 100
        self.__world.setTile(self.__body[-1], 'ground')
        self.__body = self.__body[:-1]
        self.bodyParts = len(self.__body)
        

    
    def getHealth(self):
        return self.__health
        
    
    def getPos(self, part):
        if part == 'head':
            return self.__head
        if part == 'body':
            return self.__body
      
    def getAnimal(self, part):
        if part == 'head':
            return 'snakeHead'
        if part == 'body':
            return 'snakeTail'
        
    def getView(self):
        return np.copy(self.__currentView)
   
    def printView(self):
        print("\n----------------\n")
        body = True
        for row in self.__currentView:
            print()
            if body:
                print('░','░','•', '░', '░') 
                print('░','░','▼', '░', '░')
                body = False
            for tile in row:
                print(self.__world.blockVisual[tile], end=' ')
            print(end=' ')
   
        
           

class Position():
    def __init__(self, sx=1, sy=1):
        self.__legalMoves = {'left':3, 'forward':0, 'right':1}
        
        self.direction = {'North':np.array([0, -1]), 
                            'East':np.array([1, 0]), 
                            'South':np.array([0, 1]), 
                            'West':np.array([-1, 0])}
        
        self.__dirList = ['North', 'East', 'South', 'West']
        self.__curDir = 0    
        self.__curPos = np.array([sx, sy], dtype=np.int32)
        self.__orientation = self.direction['North']
 
    def update(self, move):
        self.__reorientate(move) 
        self.__curPos += self.__orientation
        
    def __reorientate(self, move):
        self.__curDir = (self.__curDir + self.__legalMoves[move]) % 4
        self.__orientation = self.direction[self.__dirList[self.__curDir]]
            

    def getPos(self):
        return self.__curPos
    

    def getOri(self):
        return self.__orientation
    def getdirectionIdx(self):
        return self.__curDir
        
    
  
    

class SnakeSim():
    def __init__(self, x=32, y=32, sc = 0.1, fc = 0.001):
        self.sc = sc
        self.mapX = x
        self.mapY = y
        self.world = GameMap(x=self.mapX, y=self.mapY, stoneChance=self.sc)
        self.snake = Snake(16, 16, self.world)
        self.world.spawnSnake(self.snake)
        self.world.addFood(x//4, 'water')
        self.world.addFood(x//8, 'mouse')
        self.world.addFood(2, 'specialFruit')
        self.foodChance = fc
        # self.world.printWorld()

        
    
    def gameTick(self, action):     
        if np.random.random() < self.foodChance:
            self.world.addFood(1)
        self.world.updateWorld(action)
        
    def alive(self):
        return self.snake.alive
    
    def step(self, action):
        self.gameTick(action)
        reward = self.snake.lastReward
        alive = self.snake.alive
        state = self.getState()
        return reward, state, alive
    

    
    def getWaterEaten(self):
        return self.snake.rewards.consumed['water']
    
    def getSpecialEaten(self):
        return self.snake.rewards.consumed['specialFruit']
    
    def getMiceEaten(self):
        return self.snake.rewards.consumed['mouse']
    
    def getScore(self):
        return self.snake.score
    
    def getState(self):
         
        inputHealth = self.snake.getHealth()
        inputVision = self.snake.getView()
        inputBody = self.snake.bodyParts
        score = self.snake.score
        
        state = np.zeros(43) 
        
        i=0
        for row in inputVision:
            for tile in row:      
                state[i] = tile
                i+=1
        state[i] = inputHealth 
        i += 1
        state[i] = score
        i += 1
        state[i] = inputBody
    
        state = np.array(state,dtype=np.float32)

        return state
        
    
    def getReplay(self):
        return self.world.replay
    
    def resetGame(self):
        self.world = GameMap(x=self.mapX, y=self.mapY, stoneChance=self.sc)
        self.snake = Snake(16, 16, self.world)
        self.world.spawnSnake(self.snake)
        self.world.addFood(self.mapX//8, 'water')
        self.world.addFood(self.mapX//4, 'mouse')
        self.world.addFood(2, 'specialFruit')
        
        
   
        

    
    


