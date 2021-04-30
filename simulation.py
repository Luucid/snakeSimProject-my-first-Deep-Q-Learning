import numpy as np
from time import sleep




class GameMap():
    def __init__(self, x=16, y=16, stoneChance=0.0):
        self.__worldBlocks = {'ground':0, 'stone':1, 'food':8, 'snakeHead':16, 'snakeTail':17, 'eye':20}
        self.blockVisual = {0:' ', 1:'#', 8:'@', 16:'O', 17:'o', 20:'-'}
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
                    
        
    
    def addFood(self):
        xFood = np.random.randint(1, self.__width-1)
        yFood = np.random.randint(1, self.__height-1)
        
        if self.__map[yFood][xFood] == self.__worldBlocks['ground']:
            self.__map[yFood][xFood] = self.__worldBlocks['food']
        else:
            xFood = np.random.randint(1, self.__width-1)
            yFood = np.random.randint(1, self.__height-1)
            
        
    def printWorld(self):
        
        for row in self.__map:
            print()
            for tile in row:
                print(self.blockVisual[tile], end=' ')
                
          
                
                
    def getTile(self, x, y):
        return self.__map[y][x]
    
    def setTile(self, pos, tile):
        # print("pos:", pos, " | tile: ", tile)
        self.__map[pos[1]][pos[0]] = self.__worldBlocks[tile]
        
    def updateWorld(self):
        # self.printWorld()
        
        for animal in self.__animalList:
            self.moveAnimal(animal, True)
            animal.move()
            self.moveAnimal(animal)
            
            
        self.printWorld()




class Sight():
    def __init__(self, sFov=3, sRange=7):
        self.__sFov = sFov   #increase width of vision with per n rangeStep
        self.__sRange = sRange #n tiles visible forward
        self.__view = np.zeros((sRange, sFov))
 
        
    
    def getView(self):
        return self.__view
        
    def updateView(self, pos, ori, world):
        
        getDir = [True, True, True]
        
        vision = 1 if(ori[1] == 0) else 0
        # leftMidRight = np.array([0, 0, 0])
        leftMidRight = np.zeros(self.__sFov)
        
        for i in range(self.__sFov):
            leftMidRight[i] = 
        
        # leftMidRight[0] = pos[vision] - ori[vision-1]
        # leftMidRight[1] = pos[vision]
        # leftMidRight[2] = pos[vision] + ori[vision-1] #if horizontal, vision == 1, else vision == 0.  0-1 = -1, since only two pos in pos, -1 == last element.
        
        tmpMid = pos[vision-1]
         
        print("ori: ", ori)
        print("pos: ", pos)
        print("leftMidRight: ", leftMidRight)
        print("vision: ", vision)
        print("tmpMid: ", tmpMid)
        
        
        for y, row in enumerate(self.__view):
            for i in range(3):
                if getDir[i]:
                    # self.__view[y][i] = world.getTile(tmpMid, leftMidRight[i])
                    
                    if vision == 1:
                        self.__view[y][i] = world.getTile(tmpMid, leftMidRight[i])
                        world.setTile([tmpMid, leftMidRight[i]], 'eye')
                    else:
                        self.__view[y][i] = world.getTile(leftMidRight[i], tmpMid)
                        world.setTile([leftMidRight[i], tmpMid], 'eye')
                    
                    if self.__view[y][i] == 1:
                        getDir[i] = False
                else:
                    self.__view[y][i] = world.getBlock('stone')
                    
            tmpMid += ori[vision-1]           
            
            # if(len(row[row == 1]) == len(row)):
                
        
              
           
          
            
        
                     

        



class Snake():
    def __init__(self, x, y, world):
        self.__moves = np.array([3, 0, 1])
        self.__legalMoves = {3:'left', 0:'forward', 1:'right'}
        self.__navigator = Position(x, y)
     
        self.__head = self.__navigator.getPos()
        self.__body = np.array([self.__navigator.getPos() - self.__navigator.getOri()])
        self.sight = Sight()
        self.sight.updateView(self.__head, self.__navigator.getOri(), world)
        self.__currentView = self.sight.getView()
        self.__world = world
        self.hasBody = True
        print(self.__currentView)
        
 

    def updateView(self):
       self.sight.updateView(self.__head, self.__navigator.getOri(), self.__world)
       self.__currentView = self.sight.getView()
        
    
    def move(self):        
        direction = np.random.choice(self.__moves)
        bodyLength = len(self.__body)
        
        #move body before head.
        if bodyLength > 1:       
            for i in range(1, bodyLength):
                self.__body[i] = self.__body[i-1] 
                
        self.__body[0] = self.__head  
        
        #move head.
        self.__navigator.update(self.__legalMoves[direction])
        self.__head = self.__navigator.getPos()
        self.updateView()
        print(self.__currentView)
       
        
        

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
        
        self.__x = sx
        self.__y = sy 
        self.__curPos = np.array([self.__x, self.__y], dtype=np.int32)
        self.__prevPos = np.array([self.__x, self.__y], dtype=np.int32)
        self.__orientation = self.__direction['North']
        # self.__reorientate('forward')
        
        
        
    def update(self, move):
        self.__prevPos = self.__curPos
        self.__reorientate(move)
     
        self.__curPos += self.__orientation
        
    def __reorientate(self, move):
        self.__curDir = (self.__curDir + self.__legalMoves[move]) % 4
        self.__orientation = self.__direction[self.__dirList[self.__curDir]]
            
    def getX(self):
        return self.__x
   
    def getY(self):
        return self.__y
    
    def getPos(self):
        return self.__curPos
    
    def getPrevPos(self):
        return self.__prevPos
    
    def getOri(self):
        return self.__orientation
        
    
  
    

class SnakeSim():
    def __init__(self):
        self.world = GameMap()
        self.world.spawnAnimal(Snake(5, 5, self.world))
        self.world.addFood()
        self.world.addFood()
        self.world.addFood()
        self.world.addFood()
        self.world.addFood()
        self.world.addFood()
        self.world.addFood()
        self.world.printWorld()
        
    
    def gameTick(self):   
        self.world.updateWorld()
        
        
        
       
    
sim = SnakeSim()


sim.gameTick()


    
    
    
    
    
    
    
    
    
