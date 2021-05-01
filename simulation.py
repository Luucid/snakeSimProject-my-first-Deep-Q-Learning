import numpy as np




class GameMap():
    def __init__(self, x=16, y=16, stoneChance=0.0):
        self.__worldBlocks = {'ground':0, 'stone':1, 'pit':2, 'food':8,'mouse':9, 'snakeHead':16, 'snakeTail':17}
        self.blockVisual = {0:' ', 1:'█', 2:'҈', 8:'ѽ',9:'ϕ', 16:'☻', 17:'•'}
        self.__stoneChance = stoneChance
        
      
        self.__animalList = []
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
         
    def getBlock(self, block):
        return self.__worldBlocks[block]
    
    def getSnake(self):
        return self.__animalList[0]
    
    def moveAnimal(self, animal, setGround=False):
        animalHead = animal.getPos('head')
        if setGround:
            self.setTile(animalHead, 'ground')
        else:
            self.setTile(animalHead, animal.getAnimal('head'))
            
        if animal.hasBody:
            animalBody = animal.getPos('body')
            for part in animalBody:
                if setGround:
                    self.setTile(part, 'ground')
                else:
                    self.setTile(part, animal.getAnimal('body'))
                    
        
    
    def addFood(self, n, kind='food'):
        for i in range(n):
            xFood = np.random.randint(1, self.__width-1)
            yFood = np.random.randint(1, self.__height-1)
            
            if self.__map[yFood][xFood] == self.__worldBlocks['ground']:
                self.__map[yFood][xFood] = self.__worldBlocks[kind]
            else:
                xFood = np.random.randint(1, self.__width-1)
                yFood = np.random.randint(1, self.__height-1)
     

        
    def printWorld(self):
        
        for row in self.__map:
            for tile in row:
                print(self.blockVisual[tile], end=' ')
            print("")
            
            
    def snakeView(self):
        sv = self.__animalList[0].getView()
        # sh = self.animalList[0].getPos('head')
        # sb = self.animalList[0].getPos('body')
        
        for row in sv:
            for tile in row:
                print(self.blockVisual[tile], end=' ')
            print("")
        
        
        
        
        
             
                     
    def getTile(self, x, y):
        return self.__map[y][x]
    
    def setTile(self, pos, tile):
        self.__map[pos[1]][pos[0]] = self.__worldBlocks[tile]
        
    def updateWorld(self, action): 
        for animal in self.__animalList:
            self.moveAnimal(animal, True)
            animal.move(action)
            self.moveAnimal(animal)
            # print("HP: %i"%animal.getHealth())
            
        
        
        # self.printWorld()
        return self.__animalList[0].alive




class Sight():
    def __init__(self, sFov=3, sRange=7):
        self.__sFov = sFov   #increase width of vision with per n rangeStep
        self.__sRange = sRange #n tiles visible forward
        self.__view = np.zeros((sRange, sFov))

 
        
    
    def getView(self):
        return self.__view
    

        
    def updateView(self, pos, ori, world):
        
        getDir = [True, True, True]
        
        vision = abs(ori[0])
        # vision = 1 if(ori[1] == 0) else 0
        leftMidRight = np.array([0, 0, 0])
  
        
        if vision == 1:
            leftMidRight[0] = pos[vision] - ori[vision-1]
            leftMidRight[1] = pos[vision]
            leftMidRight[2] = pos[vision] + ori[vision-1] #if horizontal, vision == 1, else vision == 0.  0-1 = -1, since only two pos in pos, -1 == last element. 
        else:
            leftMidRight[2] = pos[vision] - ori[vision-1]
            leftMidRight[1] = pos[vision]
            leftMidRight[0] = pos[vision] + ori[vision-1] 
        
    
        for y, row in enumerate(self.__view):
            tmpMid = pos[vision-1]
            for i in range(3):
                if getDir[i]:      
                    
                    if vision == 1:
                        self.__view[y][i] = world.getTile(tmpMid, leftMidRight[i])
                    else:
                        self.__view[y][i] = world.getTile(leftMidRight[i], tmpMid)    
                    
                    if self.__view[y][i] == 1:
                        getDir[i] = False
                else:
                    self.__view[y][i] = world.getBlock('pit')                    
                tmpMid += ori[vision-1]  
           
            
            
            
              
           

class Snake():
    def __init__(self, x, y, world):
        self.actions = np.array([3, 0, 1])
        self.__legalMoves = {3:'left', 0:'forward', 1:'right'}
        self.__navigator = Position(x, y)
        self.__world = world
        ####################################################
        
        self.__health = 100 #train on achieving highest HP
        
        self.bestHp = self.__health
        self.score = self.bestHp - 100
        self.foodEaten = 0
        self.miceEaten = 0
        self.bodyParts = 1
        self.lastReward = 0
        
        self.__hpUpgrade = 200
        self.__hpDowngrade = 100
        
        ####################################################
        self.__head = self.__navigator.getPos()
        self.__body = np.array([self.__navigator.getPos() - self.__navigator.getOri()])
        self.sight = Sight()
        self.sight.updateView(self.__head, self.__navigator.getOri(), world)
        self.__currentView = self.sight.getView()
        self.hasBody = True
        self.alive = True
        
        
        
 

    def updateView(self):
       self.sight.updateView(self.__head, self.__navigator.getOri(), self.__world)
       self.__currentView = self.sight.getView()
        
    
    def move(self, action):        
        # direction = np.random.choice(self.moves)
        direction = action
        bodyLength = len(self.__body)
        ##############################################################################
        #move body before head.
        newBody = np.copy(self.__body[-1]) #in case food is eaten.    
        if bodyLength > 1:    
            i = bodyLength-1
            while i > 0:
                # tempBody = np.copy(self.__body[i-1]) 
                self.__body[i] = self.__body[i-1]
                i -= 1                      
        self.__body[0] = self.__head 
        ##############################################################################
        #move head.
        self.__navigator.update(self.__legalMoves[direction])
        self.__head = self.__navigator.getPos()
        for b in self.__body:
            if np.array_equal(self.__head, b): #if crash in tail, die.
                self.alive = False
     
        ##############################################################################
        self.calcReward(newBody, self.__world.getTile(self.__head[0], self.__head[1]))  
            
        if self.__health <= 0:
            self.alive = False
        else:
            self.updateView()
        ##############################################################################
        # print(self.__currentView)
       
        
    def calcReward(self, bodyPart, tile):
        # print(self.bodyParts)
        if tile == self.__world.getBlock('food'): #+100 on food.
            self.lastReward = 100
            self.foodEaten += 1
            self.__health += 100
            self.__world.addFood(1)
            
        elif tile == self.__world.getBlock('mouse'): #+500 on mouse.
            self.lastReward = 500
            self.miceEaten += 1
            self.__health += 500
            self.__world.addFood(1, 'mouse')
            
        elif tile == self.__world.getBlock('pit'): #death on pit.
            self.lastReward = self.__health*(-1)
            self.__health = 0
        elif tile == self.__world.getBlock('stone'): #-100 on stone
            self.lastReward = -200
            self.__health -= 200
        else:
            self.lastReward = -5
            self.__health -= 5 #punish each step without food.
        
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
   
    def printView(self, world):
        cv = self.getView()
        for row in cv:
            print()
            for tile in row:
                print(self.__world.blockVisual[tile], end=' ')
            print(end=' ')
        
    
        


class Position():
    def __init__(self, sx=1, sy=1):
        self.__legalMoves = {'left':3, 'forward':0, 'right':1}
        
        self.__direction = {'North':np.array([0, -1]), 
                            'East':np.array([1, 0]), 
                            'South':np.array([0, 1]), 
                            'West':np.array([-1, 0])}
        
        self.__dirList = ['North', 'East', 'South', 'West']
        self.__curDir = 0    
        self.__curPos = np.array([sx, sy], dtype=np.int32)
        self.__orientation = self.__direction['North']
 
    def update(self, move):
        self.__reorientate(move) 
        self.__curPos += self.__orientation
        
    def __reorientate(self, move):
        self.__curDir = (self.__curDir + self.__legalMoves[move]) % 4
        self.__orientation = self.__direction[self.__dirList[self.__curDir]]
            

    def getPos(self):
        return self.__curPos
    

    def getOri(self):
        return self.__orientation
        
    
  
    

class SnakeSim():
    def __init__(self, x=40, y=40, sc = 0.01, fc = 0.02):
        self.sc = sc
        self.mapX = x
        self.mapY = y
        self.world = GameMap(x=self.mapX, y=self.mapY, stoneChance=self.sc)
        self.snake = Snake(16, 16, self.world)
        self.world.spawnAnimal(self.snake)
        self.world.addFood(10)
        self.world.addFood(3, 'mouse')
        self.foodChance = fc
        # self.world.printWorld()

        
    
    def gameTick(self, action):     
        if np.random.random() < self.foodChance:
            self.world.addFood(3)
        self.world.updateWorld(action)
        
    def alive(self):
        return self.snake.alive
    
    def step(self, action):
        self.gameTick(action)
        reward = self.snake.lastReward
        alive = self.snake.alive
        state = self.getState()
        return reward, state, alive
    
    def getFoodEaten(self):
        return self.snake.foodEaten
    def getMiceEaten(self):
        return self.snake.miceEaten
    
    def getScore(self):
        return self.snake.score
    
    
    def getState(self):
         
        inputHealth = self.snake.score
        inputVision = self.snake.getView()
        
        state = np.zeros(22) 
        
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
        self.world.spawnAnimal(self.snake)
        self.world.addFood(20)
        self.world.addFood(2, 'mouse')
        # self.world.printWorld()
        
   
        

    
    
    
    
    
