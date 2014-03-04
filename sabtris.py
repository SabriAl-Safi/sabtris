import time
import matris
import Tkinter
from Tkinter import *

GAMEHEIGHT = 20
GAMEWIDTH = 10
WINDOWHEIGHT = 500
WINDOWWIDTH  = 450
MOVEDELAY = 300
ENDSCREENDELAY = 2000

cellColour = {0:"white", 1:"cyan", 2:"yellow", 3:"red",
              4:"lime", 5:"blue", 6:"orange", 7:"magenta",
              -1:"violet"}

directions = {'space':'V', 'Left':'<', 'Right':'>', 'Down':'v'}

rotations = {'z':'[', 'x':']'}             

class GameBoard(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, width=WINDOWWIDTH, height=WINDOWHEIGHT,
                        background='black', highlightthickness=0)
        self.parent = parent 
        self.initGame()
        self.inGame = False
        self.pack()

    def initGame(self):
        self.delete(ALL)
        self.gameMatrix = matris.GameMatrix(GAMEHEIGHT, GAMEWIDTH)

        self.create_text(WINDOWWIDTH/2, WINDOWHEIGHT/3,
                         font = 'Helvetica 48 bold',
                         text='sabtris', fill='white', activefill='blue')
        self.create_text(WINDOWWIDTH/2, 2*WINDOWHEIGHT/3,
                         text='Press s to start', fill='white',
                         activefill='blue', font='Purisa')
        self.create_text(WINDOWWIDTH/2, 2*WINDOWHEIGHT/3 + 100,
                         text='arrow keys to move | z/x to rotate | spacebar to drop | q to quit',
                         fill='white', activefill='blue',
                         font='Helvetica 8 italic')
        self.focus_get()
        self.bind_all('<Key>', self.onKeyPress)

    def drawGameScreen(self):
        self.delete(ALL)

        #Print the main game screen.
        for col in range(GAMEWIDTH):
            xPosition = 100+(col*20)
            for row in range(GAMEHEIGHT):
                yPosition = 50+(row*20)
                block = self.gameMatrix.blocks[row][col]
                fillColour = cellColour[block]
                if block > 0:
                    blockText = 'O'
                elif block == 0:
                    blockText = '.'
                else:
                    blockText = '#'
                    self.inGame = False
                self.create_text(xPosition, yPosition, fill=fillColour,
                                 text=blockText)

        #Print the spawn piece.
        for col in range(len(self.gameMatrix.spawn[0])):
            xPosition = 350+(col*20)
            for row in range(len(self.gameMatrix.spawn)):
                yPosition = 50+(row*20)
                block = self.gameMatrix.spawn[row][col]
                fillColour = cellColour[block]
                if not block == 0:
                    blockText = 'O'
                else:
                    blockText = '.'
                self.create_text(xPosition, yPosition, fill=fillColour,
                                 text=blockText)

        #Print game data.
        scoreText = 'Score: ' + str(self.gameMatrix.score)
        linesText = 'Lines: ' + str(self.gameMatrix.totalLinesCleared)
        self.create_text(350, 150, fill='white', text=scoreText, anchor=W)
        self.create_text(350, 170, fill='white', text=linesText, anchor=W) 

    def onKeyPress(self, keyPress):
        key = keyPress.keysym
        if key == 's' and not self.inGame:
            self.delete(ALL)
            self.gameMatrix.generateSpawn()
            self.gameMatrix.spawnTetronimo()
            self.drawGameScreen()
            self.inGame = True
            self.after(MOVEDELAY, self.onTimer)

        elif key in directions and self.inGame == True:
            self.gameMatrix.receiveNudge(directions[key])
            self.drawGameScreen()

        elif key in rotations and self.inGame == True:
            self.gameMatrix.receiveRotation(rotations[key])
            self.drawGameScreen()

        elif key == 'q':
            quit()

    def onTimer(self):
        if self.inGame == False:
            self.delete(ALL)
            self.create_text(WINDOWWIDTH/2, WINDOWHEIGHT/2,
                             font = 'Helvetica 36 bold',
                             text='GAME OVER', fill='white')
            self.after(ENDSCREENDELAY, self.initGame)
        
        elif self.gameMatrix.pieceInPlay:
            self.gameMatrix.receiveNudge('v')
            self.drawGameScreen()
            self.after(MOVEDELAY, self.onTimer)
            
        elif self.gameMatrix.spawnReady:
            self.gameMatrix.spawnTetronimo()
            self.after(MOVEDELAY, self.onTimer)
            
        else:
            self.after(MOVEDELAY, self.onTimer)
        
class Sabtris(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        parent.title('Sabtris')
        self.board = GameBoard(parent)
        self.pack()

root = Tk()
sab = Sabtris(root)
root.mainloop()
