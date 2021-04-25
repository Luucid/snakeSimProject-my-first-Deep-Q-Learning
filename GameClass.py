import numpy as np


class StartGame():
    def __init__(self):
        
        self.gameBoard = np.array([np.zeros(4)]*4) 
        self.pieceDict = {0:'E', 1:'ro', 2:'rx', 3:'rt', 4:'rs', 5:'ro*', 6:'rx*', 7:'rt*', 8:'rs*',9:'go', 10:'gx', 11:'gt', 12:'gs', 13:'go*', 14:'gx*', 15:'gt*', 16:'gs*'}
        self.availablePieces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        
        self.winScenario = {'red':[1, 2, 3, 4, 5, 6, 7, 8],
                            'green':[9, 10, 11, 12, 13, 14, 15, 16],
                            'dot':[5, 6, 7, 8, 13, 14, 15, 16],
                            'circle':[1, 5, 9, 13],
                            'triangle':[3, 7, 11, 15],
                            'square':[4, 8, 12, 16],
                            'cross':[2, 6, 10, 14]}
        
        
        
        
        self.player1 = 0
        self.player2 = 0
        
        self.currentPlayer = 0
      
        self.running = True
        self.gameLoop()
        
        
    def gameLoop(self):
        while(self.running):  
            self.printBoard()
            self.selectPiece()
            self.currentPlayer = (self.currentPlayer + 1) % 2
            self.checkForWin()
    
    
    
    def printBoard(self):
        print("\n\n\n")
        print("current player: %i"%self.currentPlayer, end='')
        print("\n\n\n")
        
        for y in self.gameBoard:
            for x in y:
                print("  %s  " % self.pieceDict[int(x)], end='')
            print("\n")
            
            
    
        
         
    def selectPiece(self):
        print("available pieces: ")
   
        for x in self.availablePieces: 
            print("%i. "%x, self.pieceDict[x])             
        piece = int(input("select piece from available(1-16): "))
        
        while(piece not in self.availablePieces):
            piece = int(input("select piece from available(1-16): "))
         
        self.availablePieces.remove(piece)
        self.movePiece(piece)
        
        
        
        
    def movePiece(self, piece):
        x = int(input("select x-coordinate: "))
        y = int(input("select y-coordinate: "))
             
        while(self.gameBoard[y][x] != 0): #add try, except.
            print("that spot is taken! Please select new coordinates. ")
            x = int(input("select x-coordinate: "))
            y = int(input("select y-coordinate: "))
        
        
        self.gameBoard[y][x] = piece
        
        
        
    def checkForWin(self):
        
        for y in range(len(self.gameBoard)): 
            vertPoints = {'red':0, 'green':0, 'square':0, 'circle':0, 'triangle':0, 'cross':0, 'dot':0}
            horiPoints = {'red':0, 'green':0, 'square':0, 'circle':0, 'triangle':0, 'cross':0, 'dot':0}    
              
            
            for x in range(len(self.gameBoard[y])):
                   
                for scenario in self.winScenario:
                    if(self.gameBoard[y][x] in self.winScenario[scenario]):    #horizontal checks
                        horiPoints[scenario] += 1
                        if(horiPoints[scenario] > 3):
                            self.printBoard()
                            print("%s horizontal win" % scenario)
                            self.running = False
                        
                    if(self.gameBoard.T[y][x] in self.winScenario[scenario]):  #vertical checks
                        vertPoints[scenario] += 1
                        if(vertPoints[scenario] > 3):
                            self.printBoard()
                            print("player %s wins with a %s vertical play!" % (self.currentPlayer, scenario))
                            self.running = False
        
        
                   
        
        for scenario in self.winScenario: 
            diagPoints = {'red':0, 'green':0, 'square':0, 'circle':0, 'triangle':0, 'cross':0, 'dot':0}  
            
            for d in self.gameBoard.diagonal():                                #diagonal check one
                if(d in self.winScenario[scenario]):  
                                diagPoints[scenario] += 1
                                if(diagPoints[scenario] > 3):
                                    self.printBoard()
                                    print("player %s wins with a %s diagonal play!" % (self.currentPlayer, scenario))
                                    self.running = False
            
            for d in np.fliplr(self.gameBoard).diagonal():                     #diagonal check two
                if(d in self.winScenario[scenario]):  
                                diagPoints[scenario] += 1
                                if(diagPoints[scenario] > 3):
                                    self.printBoard()
                                    print("player %s wins with a %s diagonal play!" % (self.currentPlayer, scenario))
                                    self.running = False
                        
       
                
                
                
                
                    
                
                
                    
                
                
        
        
        
        
        
        
        
           

            


StartGame()
    
        
        

