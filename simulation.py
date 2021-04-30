import numpy as np




class GameMap():
    def __init__(self, x=16, y=16, stoneChance=0.0):
        self.__worldBlocks = {'ground':0, 'stone':1, 'food':8, 'snakeHead':16, 'snakeTail':17, 'eye':20}
        self.blockVisual = {0:' ', 1:'#', 8:'@', 16:'0', 17:'¤', 20:'-'}
        self.__stoneChance = stoneChance
        
      
        self.__animalList = []
        self.__height = y
        self.__width = x
        self.__map = np.zeros((y, x))
        self.__generateWorld()
        
        
    def __generateWorld(self):
        for y in range(self.__height):
            for x in range(self.__width):
                if y == 0 or y == self.__height-1:
                    self.__map[y][x] = self.__worldBlocks['stone']
                elif x == 0 or x == self.__width-1:
                    self.__map[y][x] = self.__worldBlocks['stone']
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
                    
        
    
    def addFood(self, n):
        for i in range(n):
            xFood = np.random.randint(1, self.__width-1)
            yFood = np.random.randint(1, self.__height-1)
            
            if self.__map[yFood][xFood] == self.__worldBlocks['ground']:
                self.__map[yFood][xFood] = self.__worldBlocks['food']
            else:
                xFood = np.random.randint(1, self.__width-1)
                yFood = np.random.randint(1, self.__height-1)
            
        
    def printWorld(self):
        
        for row in self.__map:
            for tile in row:
                print(self.blockVisual[tile], end=' ')
            print("")
             
                     
    def getTile(self, x, y):
        return self.__map[y][x]
    
    def setTile(self, pos, tile):
        self.__map[pos[1]][pos[0]] = self.__worldBlocks[tile]
        
    def updateWorld(self):
        
        
        for animal in self.__animalList:
            self.moveAnimal(animal, True)
            animal.move()
            self.moveAnimal(animal)
            print("HP: %i"%animal.getHealth())
            
        
        
        self.printWorld()
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
        
        tmpMid = pos[vision-1]
    
        for y, row in enumerate(self.__view):
            for i in range(3):
                if getDir[i]:                   
                    if vision == 1:
                        self.__view[y][i] = world.getTile(tmpMid, leftMidRight[i])
                    else:
                        self.__view[y][i] = world.getTile(leftMidRight[i], tmpMid)    
                    
                    if self.__view[y][i] == 1:
                        getDir[i] = False
                else:
                    self.__view[y][i] = world.getBlock('stone')                    
            tmpMid += ori[vision-1]           
            
                
        
              
           

class Snake():
    def __init__(self, x, y, world):
        self.moves = np.array([3, 0, 1])
        self.__legalMoves = {3:'left', 0:'forward', 1:'right'}
        self.__navigator = Position(x, y)
        self.__world = world
        self.__health = 1000 #train on achieving highest HP
        
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
        
    
    def move(self, move):        
        # direction = np.random.choice(self.moves)
        direction = move
        bodyLength = len(self.__body)
        
        #move body before head.
        newBody = np.copy(self.__body[-1]) #in case food is eaten.    
        if bodyLength > 1:    
            i = bodyLength-1
            while i > 0:
                # tempBody = np.copy(self.__body[i-1]) 
                self.__body[i] = self.__body[i-1]
                i -= 1                      
        self.__body[0] = self.__head 
        
        #move head.
        self.__navigator.update(self.__legalMoves[direction])
        self.__head = self.__navigator.getPos()
        for b in self.__body:
            if np.array_equal(self.__head, b):
                self.alive = False
                print("woopos")
                
            
            
        if self.__world.getTile(self.__head[0], self.__head[1]) == self.__world.getBlock('food'): #reward on food.
            self.addTail(newBody)
            self.__health += 100
        elif self.__world.getTile(self.__head[0], self.__head[1]) == self.__world.getBlock('stone'): #death on stone.
            self.__health = 0
            
        else:
            self.__health -= 1 #punish each step without food.
            
        if self.__health <= 0:
            self.alive = False
        self.updateView()
    
        # print(self.__currentView)
       
        
    
    def addTail(self, pos):
        self.__body = np.append(self.__body, [pos], axis=0)

    
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
        
    def getView(self, world):
        cv = self.__sight.getView(self.__navigator.getPos(), self.__navigator.getOri())
        
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
    def __init__(self, x=32, y=32, sc = 0.0):
        self.sc = sc
        self.mapX = x
        self.mapY = y
        self.world = GameMap(x=self.mapX, y=self.mapY, stoneChance=self.sc)
        self.world.spawnAnimal(Snake(5, 5, self.world))
        self.world.addFood(5)
        self.world.printWorld()
        self.memoryPack = np.array([[],0,[],0]) #st, at, r, sn
        
    
    def gameTick(self):          
        return self.world.updateWorld()
    def getMemory(self):
        return self.memoryPack
    
    def resetGame(self):
        self.world = GameMap(x=self.mapX, y=self.mapY, stoneChance=self.sc)
        self.world.spawnAnimal(Snake(5, 5, self.world))
        self.world.addFood(5)
        self.world.printWorld()
        
        
        
       
    

    
    
    
    
    
    
    
    
