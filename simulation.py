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
        snakeBody = self.__snake.getPos('body')
       
        print("HP: ", self.__snake.getHealth(), " | body: ", self.__snake.getBodySize())
        print()
        for y, row in enumerate(self.__map):
            for x, tile in enumerate(row):
                if self.__map[y][x] == self.__worldBlocks['snakeTail']:
                    if [x, y] not in snakeBody:
                        self.__map[y][x] = self.__worldBlocks['ground']
                        
                    
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
        # self.cleanTails()
        return self.__snake.alive





class Sight():
    def __init__(self, world, sFov=5, sRange=7):
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
        
        
        
        
        # for row in self.coordView:
        #     for v in row:
        #         self.world.setVision(v, 'snakeEyes')
                
           
            
            
            
              
           

class Snake():
    def __init__(self, x, y, world):
        self.actions = np.array([3, 0, 1])
        self.__legalMoves = {3:'left', 0:'forward', 1:'right'}
        self.__navigator = Position(x, y)
        self.__world = world
        
        
        self.headVisual = ['▲','►','▼','◄']
        
        ####################################################
        
        self.__health = 100 #train on achieving highest HP
        
        self.bestHp = self.__health
        self.score = self.bestHp - 100
        
        self.waterEaten = 0
        self.miceEaten = 0
        self.specialEaten = 0
        self.rocksWithPower = 0
        self.rocksWithoutPower = 0
        
        self.bodyParts = 1
        self.lastReward = 0
        
        self.__hpUpgrade = 200
        self.__hpDowngrade = 100
        
        ####################################################
        self.__head = self.__navigator.getPos()
        self.__body = np.array([self.__navigator.getPos() - self.__navigator.getOri()])
        
        self.sight = Sight(world)
        self.sight.updateView(self.__head, self.__navigator.getOri(), world)     
        self.__currentView = self.sight.getView()
        # self.coordView = self.sight.coordView
        self.rockImmunity = 0
        self.hasBody = True
        self.alive = True
        
        
        
    def getBodySize(self):
        return self.bodyParts

    def updateView(self):
       self.sight.updateView(self.__head, self.__navigator.getOri(), self.__world)
       self.__currentView = self.sight.getView()
       if self.rockImmunity > 0:
           self.__world.blockVisual[16] = '☼'
       else:
           self.__world.blockVisual[16] = self.headVisual[self.__navigator.getdirectionIdx()]
       
       
        
    
    def move(self, action):        
        # direction = np.random.choice(self.moves)
        direction = action
        bodyLength = len(self.__body)
        ##############################################################################
        #move body before head.
        # newBody = np.copy(self.__body[0]) #in case food is eaten.    
        if bodyLength > 1:    
            # newBody = np.copy(self.__body[-1]) 
            i = bodyLength-1
            # self.__world.setTile(self.__body[-1], 'ground')
            while i > 0:            
                self.__world.setTile(self.__body[i], 'snakeTail')
                self.__body[i] = self.__body[i-1]
                i -= 1  
         
            
         
        self.__body[0] = np.copy(self.__head)
        if len(self.__body > 1):
            self.__world.setTile(self.__body[-1], 'ground')
        else:
            self.__world.setTile(self.__body[0], 'snakeTail')
        ##############################################################################
        #move head.
        self.__navigator.update(self.__legalMoves[direction])
        self.__head = self.__navigator.getPos()
       
     
        ##############################################################################
        self.calcReward(self.__body[-1], self.__world.getTile(self.__head[0], self.__head[1]))  
            
        if self.__health <= 0:
            self.alive = False
        else:
            self.updateView()
        ##############################################################################
        # print(self.__currentView)
       
        
    def calcReward(self, bodyPart, tile):
        
        if tile == self.__world.getBlock('water'): #+120 on water.
            self.lastReward = 120
            self.waterEaten += 1
            self.__health += 120
            self.__world.addFood(1)
            
        elif tile == self.__world.getBlock('mouse'): #+250 on mouse.
            self.lastReward = 250
            self.miceEaten += 1
            self.__health += 250
            self.__world.addFood(1, 'mouse')
        elif tile == self.__world.getBlock('specialFruit'): #25 frames of rock-immunity, +500 reward.
            self.lastReward = 500
            self.specialEaten += 1
            self.__health += 300
            self.rockImmunity += 25
            self.__world.addFood(1, 'specialFruit')
          
        elif tile == self.__world.getBlock('snakeTail'): #death on tail.
            self.lastReward = self.__health*(-1)
            self.__health = 0
        elif tile == self.__world.getBlock('pit'): #death on pit.
            self.lastReward = self.__health*(-1)
            self.__health = 0
        elif tile == self.__world.getBlock('stone'): #-100 on stone
            if self.rockImmunity > 0:
                self.lastReward = +100
                self.rocksWithPower += 1
            else:
                self.lastReward = -200
                self.__health -= 200
                self.rocksWithoutPower += 1
        else:
            self.lastReward = -1.2
            self.__health -= 1.2 #punish each step without food.
        
        if self.__health >= self.__hpUpgrade:
            self.__hpDowngrade += 100
            self.__hpUpgrade += 100
            self.addTail(bodyPart)
        
        elif (self.__health < self.__hpDowngrade) and (self.__health > 100):
            self.__hpDowngrade -= 100
            self.__hpUpgrade -= 100
            self.removeTail()
        if self.__health > self.bestHp:
            self.bestHp = self.__health
            self.score = self.bestHp-100
        if self.rockImmunity > 0:
            self.rockImmunity -= 1
            
        
    
    def addTail(self, pos):
        self.__body = np.append(self.__body, [pos], axis=0)
        self.bodyParts = len(self.__body)

    def removeTail(self):
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
        return self.snake.waterEaten
    
    def getSpecialEaten(self):
        return self.snake.specialEaten
    
    def getMiceEaten(self):
        return self.snake.miceEaten
    
    def getScore(self):
        return self.snake.score
    def getRocksCrushed(self, power=True):
        if power:
            return self.snake.rocksWithPower
        return self.snake.rocksWithoutPower
    
    def getState(self):
         
        inputHealth = self.snake.getHealth()
        inputVision = self.snake.getView()
        
        state = np.zeros(36) 
        
        i=0
        for row in inputVision:
            for tile in row:      
                state[i] = tile
                i+=1
        state[i] = inputHealth  
    
        state = np.array(state,dtype=np.float32)

        return state
        
    
    def resetGame(self):
        self.world = GameMap(x=self.mapX, y=self.mapY, stoneChance=self.sc)
        self.snake = Snake(16, 16, self.world)
        self.world.spawnSnake(self.snake)
        self.world.addFood(self.mapX//8, 'water')
        self.world.addFood(self.mapX//4, 'mouse')
        self.world.addFood(2, 'specialFruit')
        # self.world.printWorld()
        
   
        

    
    

# def setLeftMidRight(self, vision, pos, ori):
#         if vision == 1: #horizontal
#             self.__leftMidRight[0] = pos - ori
#             self.__leftMidRight[1] = pos
#             self.__leftMidRight[2] = pos + ori
#         else:             
#             self.__leftMidRight[2] = pos - ori
#             self.__leftMidRight[1] = pos
#             self.__leftMidRight[0] = pos + ori
    
# if vision == 1: #horizontal
  #     leftMidRight[0] = pos[vision] - ori[vision-1]
  #     leftMidRight[1] = pos[vision]
  #     leftMidRight[2] = pos[vision] + ori[vision-1] 
  # else:
  #     leftMidRight[2] = pos[vision] - ori[vision-1]
  #     leftMidRight[1] = pos[vision]
  #     leftMidRight[0] = pos[vision] + ori[vision-1]  
