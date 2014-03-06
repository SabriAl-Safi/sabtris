import random

tetronimo = {
             1: [ [0, 0, 0, 0],
                  [1, 1, 1, 1],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0] ],

             2: [ [2, 2],
                  [2, 2] ],

             3: [ [3, 3, 0],
                  [0, 3, 3],
                  [0, 0, 0] ],

             4: [ [0, 4, 4],
                  [4, 4, 0],
                  [0, 0, 0] ],

             5: [ [5, 0, 0],
                  [5, 5, 5],
                  [0, 0, 0] ],

             6: [ [0, 0, 6],
                  [6, 6, 6],
                  [0, 0, 0] ],

             7: [ [0, 7, 0],
                  [7, 7, 7],
                  [0, 0, 0] ]
             }

numLinesScore = { 1:40, 2:100, 3:300, 4:1200 }

class GameMatrix:
    """
    Matrix representing current state of play.
    """

    #-------- Initialisation constructor -----------------------------------
    
    def __init__(self, height, width, initLevel):
        self.blocks = [ [ 0
                          for col in range(width) ]
                        for row in range(height) ]

        #Game stats.
        self.height = height
        self.width = width
        self.score = 0
        self.totalLinesCleared = 0
        self.level = initLevel

        #Control of piece currently in play.
        self.pieceInPlay = False
        self.activeCells = []
        self.activeType = 0
        self.activeOrientation = 0
        self.activeTopLeftCorner = []
        self.dropDelay = 300 - (self.level*20)
        
        #Control of piece ready to be spawned.
        self.spawn = []
        self.spawnType = 0
        self.spawnOrientation = 0
        self.spawnReady = False

    #-------- External functions -------------------------------------------

    def generateSpawn(self):
        """
        Randomly generate new tetronimo piece to be spawned.
        """
        tetNum = random.randint(1,7)
        self.spawn = tetronimo[tetNum]
        self.spawnType = tetNum
        self.spawnReady = True
        self.spawnOrientation = 0

    def receiveNudge(self, key):
        """
        If a piece is in play, move it according to key.
        """
        if self.pieceInPlay:
            if key == 'V':
                while self.pieceInPlay:
                    self.nudgePlayPiece('v')
            else:
                self.nudgePlayPiece(key)

    def receiveRotation(self,key):
        """
        Rotate the spawn piece or the piece in play, accoridng to key.
        """
        if self.pieceInPlay:
            self.rotatePlayPiece(key)

    #-------- Internal Functions--------------------------------------------

    def clearLines(self):
        """
        Clear any complete lines in the matrix. If there are lines to clear,
        return list of row numbers of cleared lines, else return False.
        """
        rowsCleared = []
        for rowNum, blockRow in enumerate(self.blocks):
            if not 0 in blockRow:
                self.blocks[rowNum] = [ 0 for col in range(self.width) ]
                rowsCleared.append(rowNum)
        if len(rowsCleared) > 0:
            return rowsCleared
        else:
            return False

    def updateGameStats(self, numRowsCleared):
        """
        Update game statistics after some rows have been cleared.
        """
        self.score += (self.level+1)*numLinesScore[numRowsCleared]
        self.totalLinesCleared += numRowsCleared
        if (self.level+1) * 10 < self.totalLinesCleared:
            self.level += 1
            if self.level <= 10:
                self.dropDelay = 300 - 20*(self.level)

    def reshiftRows(self, rowsCleared):
        """
        Shift rows down after some rows have been cleared.
        """
        numShifts = 0
        for row in rowsCleared:
            #Starting from the top line cleared, proceed up every row and
            #shift it down once. Repeat for the next top line cleared.
            rowNum = row
            while rowNum > 0:
                self.blocks[rowNum] = self.blocks[rowNum-1]
                rowNum -= 1
            self.blocks[0] = [ 0 for col in range(self.width) ]
            numShifts += 1

    def spawnTetronimo(self):
        """
        Send the spawn piece into the fray.
        """
        spawnSize = len(self.spawn[0])
        insertFrom = int((self.width/2) - ((spawnSize+1)/2))
        
        for row in range(spawnSize):
            for col in range(spawnSize):
                #Insert spawn shape into matrix.
                spawnBlock = self.spawn[row][col]
                if not spawnBlock == 0:
                    if self.blocks[row][insertFrom + col] == 0:
                        #Okay to spawn this cell.
                        self.blocks[row][insertFrom + col] = spawnBlock
                        #Update the list of active cells.
                        self.activeCells.append([row, insertFrom + col])
                    else:
                        #Spawn cell clashes with a settled piece. Game over!
                        self.blocks[row][insertFrom + col] = -1

        #Update control data.
        self.pieceInPlay = True
        self.activeType = self.spawnType
        self.activeOrientation = self.spawnOrientation
        self.activeTopLeftCorner = [0, insertFrom]
        self.spawn = []
        self.spawnReady = False
        self.spawnType = 0
        self.spawnOrientation = 0
        self.generateSpawn()

    def rotatePlayPiece(self, direction):
        """
        Rotate the active piece once in the given direction, if possible.
        """
        #If the play piece is 'O', don't do anything.
        if not self.activeType == 2:
            #Identify list of future active cells. 
            newPiece = tetronimo[self.activeType]
            newActiveCells = []
            if direction == ']':
                #Clockwise rotation.
                for rotation in range((self.activeOrientation + 1)%4):
                    newPiece = zip(*newPiece[::-1])
                newOrientation = (self.activeOrientation+1)%4
            elif direction == '[':
                #Counter-clockwise rotation.
                for rotation in range((self.activeOrientation - 1)%4):
                    newPiece = zip(*newPiece[::-1])
                newOrientation = (self.activeOrientation-1)%4
            for row in range(len(newPiece)):
                for col in range(len(newPiece[0])):
                    if not newPiece[row][col] == 0:
                        newRow = self.activeTopLeftCorner[0]+row
                        newCol = self.activeTopLeftCorner[1]+col
                        newActiveCells.append([newRow, newCol])
                        
            #First, figure out the obstructive cells of the original
            #tetronimo active area (e.g. 3x3 spawn matrix), assuming
            #tetronimo hasn't been rotated.
            obstructiveCells = []
            rotationObstructed = False
            if self.activeType == 1:
                if direction == ']':
                    obstructiveCells = [ [0, 0],
                                         [0, 1],
                                         [2, 3],
                                         [3, 3] ]
                elif direction == '[':
                    obstructiveCells = [ [0, 2],
                                         [0, 3],
                                         [2, 0],
                                         [3, 0] ]
                #Rotate the obstructive cells to be in alignment with
                #actual play piece.
                for rotation in range(self.activeOrientation):
                    for index, cell in enumerate(obstructiveCells): 
                        obstructiveCells[index] = [cell[1], 3-cell[0]]
            else:
                if direction == ']':
                    obstructiveCells = [ [0, 0],
                                         [2, 2] ]
                elif direction == '[':
                    obstructiveCells = [ [0, 2],
                                         [2, 0] ]
                #Rotate the obstructive cells to be in alignment with
                #actual play piece.
                for rotation in range(self.activeOrientation):
                    for index, cell in enumerate(obstructiveCells): 
                        obstructiveCells[index] = [cell[1], 2-cell[0]]

            #Now embed these values into the actual matrix.
            TLRow = self.activeTopLeftCorner[0]
            TLCol = self.activeTopLeftCorner[1]
            for index, cell in enumerate(obstructiveCells):
                obstructiveCells[index] = [TLRow + cell[0], TLCol + cell[1]]
                
            #Determine whether the obstructive cells or new active cells
            #clash with any settled blocks. If not, proceed with rotation.
            if (self.checkMovementPossible(obstructiveCells)
                and self.checkMovementPossible(newActiveCells)):
                self.movePlayPiece(newActiveCells)
                #Update control data.
                self.activeOrientation = newOrientation

    def nudgePlayPiece(self, direction):
        """
        Move the active piece once in the given direction, if possible.
        """
        #Determine list of future active cells.
        newTopLeftCorner = [self.activeTopLeftCorner[0],
                            self.activeTopLeftCorner[1]]
        if direction == '<':
            newActiveCells = [ [cell[0], cell[1]-1] 
                               for cell in self.activeCells ]
            newTopLeftCorner[1] -= 1
        elif direction == '>':
            newActiveCells = [ [cell[0], cell[1]+1] 
                               for cell in self.activeCells ]
            newTopLeftCorner[1] += 1
        elif direction == 'v':
            newActiveCells = [ [cell[0]+1, cell[1]] 
                               for cell in self.activeCells ]
            newTopLeftCorner[0] += 1
            
        #Check whether new cells constitute an allowed movement. If so,
        #move play piece.
        if self.checkMovementPossible(newActiveCells):
            self.movePlayPiece(newActiveCells)
            #Update control data.
            self.activeTopLeftCorner = newTopLeftCorner
            
        elif direction == 'v':
            #If the requested move is downwards but not possible, lock the
            #piece.
            self.lockPlayPiece()

    def checkMovementPossible(self, newActiveCells):
        """
        Return False if list of new active cells clashes with settled
        blocks, or lies outside the matrix. Return True otherwise.
        """
        for cell in newActiveCells:
            if (cell[1] < 0 or
                cell[1] > self.width-1 or
                cell[0] > self.height-1):
                return False
            elif (not cell in self.activeCells and
                  not self.blocks[cell[0]][cell[1]] == 0):
                return False
        return True

    def movePlayPiece(self, newActiveCells):
        """
        Rewrite play piece into the new list of active cells. It is
        assumed that the movement is valid.
        """
        #Write new active cells to matrix.
        for cell in newActiveCells:
            self.blocks[cell[0]][cell[1]] = self.activeType
        #Kill the cells that need to die.
        for cell in self.activeCells:
            if cell not in newActiveCells:
                self.blocks[cell[0]][cell[1]] = 0
        #Re-assign list of active cells.
        self.activeCells = newActiveCells

    def lockPlayPiece(self):
        """
        Reset control data and clear any lines that need to be cleared.
        """
        self.pieceInPlay = False
        self.activeCells = []
        self.activeType = 0
        self.activeOrientation = 0
        self.activeTopLeftCorner = []
        
        rowsCleared = self.clearLines()
        if rowsCleared:
            self.updateGameStats(len(rowsCleared))
            self.reshiftRows(rowsCleared)
