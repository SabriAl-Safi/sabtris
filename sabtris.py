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
FLASHTEXTONDELAY = 1000
FLASHTEXTOFFDELAY = 700

cellColour = {0:"white", 1:"cyan", 2:"yellow", 3:"red",
              4:"green", 5:"blue", 6:"orange", 7:"magenta",
              -1:"violet"}

directions = {'space':'V', 'Left':'<', 'Right':'>', 'Down':'v'}

rotations = {'z':'[', 'x':']'}             

class GameBoard(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, width=WINDOWWIDTH, height=WINDOWHEIGHT,
                        background='black', highlightthickness=0)
        self.parent = parent 
        self.initGame()
        self.pack()

    def initGame(self):
        self.startScreen = True
        self.controlsScreen = False
        self.inGame = False
        self.controlsScreenFlashTextOn = False
        self.startScreenFlashTextOn = False
        self.drawStartScreen()
        self.focus_get()
        self.bind_all('<Key>', self.onKeyPress)
        self.startScreen = True

    def drawStartScreen(self):
        '''
        Draw the game's start screen.
        '''
        if self.startScreen:
            self.delete(ALL)
            self.create_text(WINDOWWIDTH/2, WINDOWHEIGHT/3,
                             font = 'Helvetica 48 bold',
                             text='sabtris',
                             fill='white',
                             activefill='blue')

            if self.startScreenFlashTextOn == True:
                self.create_text(WINDOWWIDTH/2, 400,
                                 text='s to start, c for controls',
                                 fill='white',
                                 activefill='blue',
                                 font='Purisa')
                self.startScreenFlashTextOn = False
                self.after(FLASHTEXTONDELAY, self.drawStartScreen)
            else:
                self.startScreenFlashTextOn = True
                self.after(FLASHTEXTOFFDELAY, self.drawStartScreen)
    

    def drawControlsScreen(self):
        '''
        Draw the game's controls info screen.
        '''
        if self.controlsScreen:
            self.delete(ALL)
            self.create_text(150, 200,
                             text='arrows ------------------------ move\n' +
                                  'z/x ---------------------------- rotate\n' +
                                  'spacebar --------------------- drop\n' +
                                  'q -------------------------------- quit\n' +
                                  'p ----------------------------- pause\n' +
                                  'r ---------------------------- restart\n',
                             fill='white',
                             activefill='blue',
                             font='Helvetica 8 italic',
                             anchor=W)

            if self.controlsScreenFlashTextOn == True:
                self.create_text(WINDOWWIDTH/2, 400,
                                 text='Hit enter to return',
                                 fill='white',
                                 activefill='blue',
                                 font='Helvetica',
                                 tags='flashText')
                self.controlsScreenFlashTextOn = False
                self.after(FLASHTEXTONDELAY, self.drawControlsScreen)
            else:
                self.controlsScreenFlashTextOn = True
                self.after(FLASHTEXTOFFDELAY, self.drawControlsScreen)

    def drawGameScreen(self):
        '''
        Delete and redraw the main game screen.
        '''      
        self.delete('gameScreen')
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
                self.create_text(xPosition, yPosition,
                                 fill=fillColour,
                                 text=blockText,
                                 tags='gameScreen')

    def drawSpawnPiece(self):
        '''
        Delete and redraw the piece next to be spawned.
        '''
        self.delete('spawnPiece')
        for col in range(len(self.gameMatrix.spawn[0])):
            xPosition = 350+(col*20)
            for row in range(len(self.gameMatrix.spawn)):
                yPosition = 50+(row*20)
                block = self.gameMatrix.spawn[row][col]
                fillColour = cellColour[block]
                if not block == 0:
                    blockText = 'O'
                    self.create_text(xPosition, yPosition,
                                     fill=fillColour,
                                     text=blockText,
                                     tags='spawnPiece')

    def drawGameData(self):
        '''
        Delete and redraw the game data.
        '''
        self.delete('gameData')
        scoreText = 'Score: ' + str(self.gameMatrix.score)
        linesText = 'Lines: ' + str(self.gameMatrix.totalLinesCleared)
        levelText = 'Level: ' + str(self.gameMatrix.level)
        self.create_text(350, 150,
                         fill='white',
                         text=scoreText,
                         anchor=W,
                         tags='gameData')
        self.create_text(350, 170,
                         fill='white',
                         text=linesText,
                         anchor=W,
                         tags='gameData')
        self.create_text(350, 190,
                         fill='white',
                         text=levelText,
                         anchor=W,
                         tags='gameData')

    def onKeyPress(self, keyPress):
        key = keyPress.keysym
        
        if self.startScreen:
            
            if key == 's':
                #Begin the game.
                self.startScreen = False
                self.inGame = True
                self.delete(ALL)
                self.gameMatrix = matris.GameMatrix(GAMEHEIGHT, GAMEWIDTH)
                self.gameMatrix.generateSpawn()
                self.gameMatrix.spawnTetronimo()
                self.drawGameScreen()
                self.drawSpawnPiece()
                self.drawGameData()
                self.after(MOVEDELAY, self.inGameTimer)

            if key == 'c':
                #Go to the controls info screen.
                self.startScreen = False
                self.controlsScreen = True
                self.drawControlsScreen()

        elif self.controlsScreen:

            if key == 'Return':
                #Return from controls info screen to start screen.
                self.controlsScreen = False
                self.startScreen = True
                self.drawStartScreen()

        elif self.inGame:

            if key in directions:
                self.gameMatrix.receiveNudge(directions[key])
                self.drawGameScreen()

            elif key in rotations:
                self.gameMatrix.receiveRotation(rotations[key])
                self.drawGameScreen()

        if key == 'q':
            quit()

    def inGameTimer(self):
        
        if not self.inGame:
            self.delete(ALL)
            self.create_text(WINDOWWIDTH/2, WINDOWHEIGHT/2,
                             font = 'Helvetica 36 bold',
                             text='GAME OVER', fill='white')
            self.after(ENDSCREENDELAY, self.initGame)
        
        elif self.gameMatrix.pieceInPlay:            
            self.gameMatrix.receiveNudge('v')
            self.drawGameScreen()
            self.after(MOVEDELAY, self.inGameTimer)
            
        elif self.gameMatrix.spawnReady:            
            self.gameMatrix.spawnTetronimo()
            self.drawSpawnPiece()
            self.drawGameData()
            self.after(MOVEDELAY, self.inGameTimer)
            
        else:            
            self.after(MOVEDELAY, self.inGameTimer)

        self.drawGameData()
        
class Sabtris(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        parent.title('Sabtris')
        self.board = GameBoard(parent)
        self.pack()

root = Tk()
sab = Sabtris(root)
root.mainloop()
