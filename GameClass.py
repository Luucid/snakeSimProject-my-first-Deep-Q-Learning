import numpy as np
from os import system



#make game work as step by step from main.
track = np.array([])
winTrack = {'draw': 0, 'red':0, 'green':0, 'dot':0, 'circle':0, 'triangle':0, 'square':0, 'cross':0}


class Game():
    def __init__(self, enableHuman = False):
        
        self.__gameBoard = np.zeros((4,4))
        self.__pieceDict = {0:' ', 1:'ro', 2:'rx', 3:'rt', 4:'rs', 5:'ro*', 6:'rx*', 7:'rt*', 8:'rs*',9:'go', 10:'gx', 11:'gt', 12:'gs', 13:'go*', 14:'gx*', 15:'gt*', 16:'gs*'}
        
        self.__availablePieces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

        
        self.__winScenario = {'red':[1, 2, 3, 4, 5, 6, 7, 8],
                            'green':[9, 10, 11, 12, 13, 14, 15, 16],
                            'dot':[5, 6, 7, 8, 13, 14, 15, 16],
                            'circle':[1, 5, 9, 13],
                            'triangle':[3, 7, 11, 15],
                            'square':[4, 8, 12, 16],
                            'cross':[2, 6, 10, 14]}
        
        self.exp = {'st':0, 'pt':0,'mt':[0,0], 'rt':0, 'sn':0}
        self.__enableHuman = enableHuman
        self.__currentPlayer = 0
        self.__running = False
        self.__lim = [0,1,2,3]
        self.__initScore = 16


        
    
    def getStatus(self):
        return self.__running
    def nextMove(self):
        return self.__gameLoop()
        
    def startGame(self):
        self.__running = True
        self.__gameLoop()
        
    def __gameLoop(self):
    # while(self.__running):   
        self.exp = {'st':0, 'pt':0,'mt':[0,0], 'rt':0, 'sn':0}
        self.__selectPiece()
        self.__currentPlayer = (self.__currentPlayer + 1) % 2  
        self.__checkForWin()
        return np.array([self.exp['st'], self.exp['pt'],self.exp['mt'],self.exp['rt']])
            
        
           
  
    
    def __printBoard(self):
        system('cls')
        print("\n\n\n")
        print("current player: %i"% self.__currentPlayer, end='')
        print("\n\n\n")
              
        
        for y in self.__gameBoard:
            for x in y:
                
                print("[ %s ]" % self.__pieceDict[int(x)], end='')
            print("\n")
            
    
    
    def __check(self, val, limit):        
      while(True):
          if(val.isdigit()):
              if(int(val) in limit):
                  break
          val = input("error, try again: ")
      return int(val)        

    

    def __checkAI(self, val, limit):        
        while(True):
            
            if(val in limit):
                break
        val = np.random.choice(self.__availablePieces)
        return val
                    
      
    
        
         
    def __selectPiece(self):
        piece = 0
        
        if(self.__currentPlayer == 1 and self.__enableHuman):
            print("available pieces: ")
            for x in self.__availablePieces: 
                print("%i. " % x, self.__pieceDict[x])             
           
            piece = self.__check(input("select piece from available(1-16): "), self.__availablePieces)
        else: 
            # if(len(self.__availablePieces) > 0):
            piece = np.random.choice(self.__availablePieces)
            # else:
                
            
        
        if(len(self.__availablePieces) <= 0):
            self.__running = False
            
        self.exp['pt'] = piece
        self.__availablePieces.remove(piece)
        self.__movePiece(piece)
        
        
       

    
    def __movePiece(self, piece):
        
        x = 0
        y = 0
        
        if(self.__currentPlayer == 1 and self.__enableHuman):
        
            x = self.__check(input("select x-coordinate: "), self.__lim)
            y = self.__check(input("select y-coordinate: "), self.__lim)
            
            while(self.__gameBoard[y][x] != 0): #add try, except.
                print("that spot is taken! Please select new coordinates. ")
                x = self.__check(input("select x-coordinate: "), self.__lim)
                y = self.__check(input("select y-coordinate: "), self.__lim)
         
        
        else:
            
            while(self.__gameBoard[y][x] != 0):
                x = np.random.randint(0, 4)
                y = np.random.randint(0, 4)
            
            
        self.exp['mt'] = [x, y]
        self.__gameBoard[y][x] = piece
        
        
        
        
    
        
    def __checkForWin(self):
        
        
            
        for y in range(len(self.__gameBoard)): 
            vertPoints = {'red':0, 'green':0, 'square':0, 'circle':0, 'triangle':0, 'cross':0, 'dot':0}
            horiPoints = {'red':0, 'green':0, 'square':0, 'circle':0, 'triangle':0, 'cross':0, 'dot':0}    
              
            
            for x in range(len(self.__gameBoard[y])):
                 
                for scenario in self.__winScenario:
                    if(self.__gameBoard[y][x] in self.__winScenario[scenario]):    #horizontal checks
                        horiPoints[scenario] += 1
                        if(horiPoints[scenario] > 3):
                            self.__printBoard()
                            # print("%s horizontal win" % scenario)
                            # trainPack['win'].append(np.copy(self.__gameBoard))
                            self.__running = False
                        
                    if(self.__gameBoard.T[y][x] in self.__winScenario[scenario]):  #vertical checks
                        vertPoints[scenario] += 1
                        if(vertPoints[scenario] > 3):
                            self.__printBoard()
                            # print("player %s wins with a %s vertical play!" % (self.__currentPlayer, scenario))
                            # trainPack['win'].append(np.copy(self.__gameBoard))
                            self.__running = False
        
            
                   
        
        for scenario in self.__winScenario: 
            
            diagPoints = {'red':0, 'green':0, 'square':0, 'circle':0, 'triangle':0, 'cross':0, 'dot':0}   
            for d in self.__gameBoard.diagonal():                                #diagonal check one      
                if(d in self.__winScenario[scenario]):  
                    diagPoints[scenario] += 1
                    if(diagPoints[scenario] > 3):
                        self.__printBoard()
                        # print("player %s wins with a %s diagonal play!" % (self.__currentPlayer, scenario))
                        # trainPack['win'].append(np.copy(self.__gameBoard))
                        winTrack[scenario] += 1
                        self.__running = False
            
            diagPoints = {'red':0, 'green':0, 'square':0, 'circle':0, 'triangle':0, 'cross':0, 'dot':0}  
            for d in np.fliplr(self.__gameBoard).diagonal():                     #diagonal check two
                if(d in self.__winScenario[scenario]):  
                    diagPoints[scenario] += 1
                    if(diagPoints[scenario] > 3):
                        self.__printBoard()
                        # print("player %s wins with a %s diagonal play!" % (self.__currentPlayer, scenario))
                        # trainPack['win'].append(np.copy(self.__gameBoard))
                        winTrack[scenario] += 1
                        self.__running = False
                        
       
                
  
            
                
        if(len(self.__availablePieces) < 1 and self.__running):
            self.__printBoard()
            # print("DRAW!")
            # trainPack['win'].append(np.copy(self.__gameBoard))
            winTrack['draw'] += 1
            self.__running = False   
        
        if(self.__running == False):
            self.exp['rt'] = self.__initScore
        else:
            self.__initScore -= 1
            
            
            
                    
                
                
                    
                
                
        
        
        
        
        

        

