import time
import matris
import Tkinter
from Tkinter import *

#Display dimensions.
GAMEHEIGHT = 22
GAMEWIDTH = 10
WINDOWHEIGHT = 500
WINDOWWIDTH  = 450
CELLSIZE = 18

#Timer delays.
ENDSCREENDELAY = 2000
FLASHTEXTDELAY = 500

#Colours of tetronimo pieces.
cellColour = {0:"white", 1:"cyan", 2:"yellow", 3:"red",
              4:"green", 5:"blue", 6:"orange", 7:"magenta",
              -1:"violet"}

#Key controls.
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

        #Flags for screen control.
        self.startScreen = True
        self.controlsScreen = False
        self.pauseScreen = False
        self.settingsScreen = False
        self.inGame = False

        #Flags for option selections.
        self.startSelected = True
        self.settingsSelected = False
        self.controlsSelected = False
        self.returnSelected = False
        self.defaultSelected = False
        self.gamePaused = False
        
        #Misc.
        self.flashTextFill = 'white'
        self.curLinesCleared = 0
        self.initLevel = 0

        #Draw start screen and bind keys.
        self.drawStartScreen()
        self.focus_get()
        self.bind_all('<Key>', self.onKeyPress)

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
            
            #Draw options text, with selected text flashing.
            startFill = 'white'
            controlsFill = 'white'
            settingsFill = 'white'

            if self.startSelected: startFill = self.flashTextFill
            elif self.controlsSelected: controlsFill = self.flashTextFill
            elif self.settingsSelected: settingsFill = self.flashTextFill
            
            self.create_text(WINDOWWIDTH/2, 370,
                             text='start game',
                             fill=startFill,
                             font='Purisa')

            self.create_text(WINDOWWIDTH/2, 400,
                             text='controls',
                             fill=controlsFill,
                             font='Purisa')

            self.create_text(WINDOWWIDTH/2, 430,
                             text='settings',
                             fill=settingsFill,
                             font='Purisa')

            #Change colour of flashing text next time start screen is drawn.
            if self.flashTextFill == 'white': self.flashTextFill = 'blue'
            else: self.flashTextFill = 'white'
            
            self.after(FLASHTEXTDELAY, self.drawStartScreen)

    def drawPauseScreen(self):
        '''
        Draw the game's pause screen.
        '''
        if self.pauseScreen:
            self.delete(ALL)
            self.create_text(WINDOWWIDTH/2, WINDOWHEIGHT/3,
                             font = 'Helvetica 48 bold',
                             text='| |',
                             fill='white',
                             activefill='blue')
            
            #Draw options text, with selected text flashing.
            returnFill = 'white'
            restartFill = 'white'
            controlsFill = 'white'

            if self.returnSelected: returnFill = self.flashTextFill
            elif self.startSelected: restartFill = self.flashTextFill
            elif self.controlsSelected: controlsFill = self.flashTextFill

            self.create_text(WINDOWWIDTH/2, 370,
                             text='resume',
                             fill=returnFill,
                             font='Purisa')

            self.create_text(WINDOWWIDTH/2, 400,
                             text='abandon',
                             fill=restartFill,
                             font='Purisa')

            self.create_text(WINDOWWIDTH/2, 430,
                             text='controls',
                             fill=controlsFill,
                             font='Purisa')
            
            #Change colour of flashing text next time start screen is drawn.
            if self.flashTextFill == 'white': self.flashTextFill = 'blue'
            else: self.flashTextFill = 'white'
            
            self.after(FLASHTEXTDELAY, self.drawPauseScreen)
    
    def drawControlsScreen(self):
        '''
        Draw the game's controls info screen.
        '''
        if self.controlsScreen:
            self.delete(ALL)
            self.create_text(WINDOWWIDTH/2, 200,
                             text='arrows ------------------------ move\n' +
                                  'z/x ----------------------------- rotate\n' +
                                  'spacebar --------------------- drop\n' +
                                  'q --------------------------------- quit\n' +
                                  'p ----------------------------- pause\n',
                             fill='white',
                             activefill='blue',
                             font='Helvetica 12 italic')

            #Draw flashing text.
            self.create_text(WINDOWWIDTH/2, 400,
                             text='return',
                             font='Helvetica',
                             fill=self.flashTextFill)
            
            #Change colour of flashing text next time start screen is drawn.
            if self.flashTextFill == 'white': self.flashTextFill = 'blue'
            else: self.flashTextFill = 'white'
            
            self.after(FLASHTEXTDELAY, self.drawControlsScreen)

    def drawSettingsScreen(self):
        """
        Draw the settings screen, allowing the user to alter start level.
        """
        if self.settingsScreen:
            self.delete(ALL)
            
            levelText = 'start level ------------------------ '
            levelText += str(self.initLevel)            
            levelFill = 'white'
            returnFill = 'white'
            defaultFill = 'white'

            if self.levelSelected: levelFill = self.flashTextFill
            elif self.returnSelected: returnFill = self.flashTextFill
            elif self.defaultSelected: defaultFill = self.flashTextFill
            
            self.create_text(WINDOWWIDTH/2, 200,
                             text=levelText,
                             fill=levelFill,
                             font='Helvetica 12 italic')
                             
            self.create_text(WINDOWWIDTH/2, 400,
                             text='save & return',
                             fill=returnFill,
                             font='Helvetica')

            self.create_text(WINDOWWIDTH/2, 430,
                             text='default settings',
                             fill=defaultFill,
                             font='Helvetica')

            #Change colour of flashing text next time start screen is drawn.
            if self.flashTextFill == 'white': self.flashTextFill = 'blue'
            else: self.flashTextFill = 'white'
            
            self.after(FLASHTEXTDELAY, self.drawSettingsScreen)

    def drawGameMatrix(self):
        '''
        Delete and redraw the main game screen.
        '''      
        self.delete('gameScreen')
        #Draw in cell matrix
        for col in range(GAMEWIDTH):
            xPosition = 100+(col*CELLSIZE)
            for row in range(GAMEHEIGHT):
                yPosition = 50+(row*CELLSIZE)
                block = self.gameMatrix.blocks[row][col]
                fillColour = cellColour[block]
                if block != 0:
                    if block > 0:
                        blockText = 'O'
                    else:
                        #Negative entry in game matrix indicates spawn piece
                        #clashing with settled block - game over!
                        blockText = '#'
                        self.inGame = False
                    self.create_text(xPosition, yPosition,
                                     fill=fillColour,
                                     text=blockText,
                                     tags='gameScreen')

                
        #Draw in walls.
        leftWallPosition = 90
        rightWallPosition = 95 + (GAMEWIDTH)*CELLSIZE
        for row in range(GAMEHEIGHT):
            yPosition = 45+(row*CELLSIZE)
            self.create_text(leftWallPosition, yPosition,
                             fill='white',
                             text='|',
                             font='Helvetica 24',
                             tags='gameScreen')
            self.create_text(rightWallPosition, yPosition,
                             fill='white',
                             text='|',
                             font='Helvetica 24',
                             tags='gameScreen')

        #Draw in floor.
        floorPosition = 45+((GAMEHEIGHT-1)*CELLSIZE)
        for col in range(GAMEWIDTH):
            xPosition = 101+(col*CELLSIZE)
            self.create_text(xPosition, floorPosition,
                             font='Helvetica 28',
                             fill='white',
                             text='_',
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

        #If number of lines cleared has increased by 4, flash 'TETRIS'
        if self.gameMatrix.totalLinesCleared == self.curLinesCleared + 4:
            self.create_text(350, 240,
                             fill='white',
                             font='Helvetica 16 bold',
                             text='TETRIS',
                             anchor=W,
                             tags='gameData')

        self.curLinesCleared = self.gameMatrix.totalLinesCleared

    def onKeyPress(self, keyPress):
        key = keyPress.keysym
        
        if self.startScreen:
            
            if key == 'Return':
                if self.startSelected:
                    #Begin the game by drawing entire game screen and
                    #triggering the in-game timer.
                    self.startScreen = False
                    self.inGame = True
                    self.delete(ALL)
                    self.gameMatrix = matris.GameMatrix(GAMEHEIGHT,
                                                        GAMEWIDTH,
                                                        self.initLevel)
                    self.gameMatrix.generateSpawn()
                    self.gameMatrix.spawnTetronimo()
                    self.drawGameMatrix()
                    self.drawSpawnPiece()
                    self.drawGameData()
                    self.after(self.gameMatrix.dropDelay, self.inGameTimer)

                elif self.controlsSelected:
                    #Go from start screen to the controls info screen.
                    self.startScreen = False
                    self.controlsScreen = True
                    self.flashTextFill = 'white'
                    self.drawControlsScreen()

                elif self.settingsSelected:
                    #Go from start screen to settings screen.
                    self.startScreen = False
                    self.settingsScreen = True
                    self.flashTextFill = 'white'
                    self.levelSelected = True
                    self.returnSelected = False
                    self.drawSettingsScreen()

            elif key == 'Down':
                #Traverse options.
                if self.startSelected:
                    self.startSelected = False
                    self.controlsSelected = True
                elif self.controlsSelected:
                    self.controlsSelected = False
                    self.settingsSelected = True
                elif self.settingsSelected:
                    self.settingsSelected= False
                    self.startSelected = True

            elif key == 'Up':
                #Traverse options.
                if self.startSelected:
                    self.startSelected = False
                    self.settingsSelected = True
                elif self.controlsSelected:
                    self.controlsSelected = False
                    self.startSelected = True
                elif self.settingsSelected:
                    self.settingsSelected= False
                    self.controlsSelected = True
                

        elif self.controlsScreen:

            if key == 'Return':
                if self.gamePaused:
                    #Return from controls info screen to pause screen.
                    self.pauseScreen = True
                    self.controlsScreen = False
                    self.flashTextFill = 'white'
                    self.drawPauseScreen()

                else:
                    #Return from controls info screen to start screen.
                    self.controlsScreen = False
                    self.startScreen = True
                    self.flashTextFill = 'white'
                    self.drawStartScreen()

        elif self.settingsScreen:

            if key == 'Down':
                #Traverse options.
                if self.levelSelected:
                    self.levelSelected = False
                    self.returnSelected = True
                elif self.returnSelected:
                    self.returnSelected = False
                    self.defaultSelected = True
                elif self.defaultSelected:
                    self.defaultSelected = False
                    self.levelSelected = True
                    
            elif key == 'Up':
                #Traverse options.
                if self.levelSelected:
                    self.levelSelected = False
                    self.defaultSelected = True
                elif self.returnSelected:
                    self.returnSelected = False
                    self.levelSelected = True
                elif self.defaultSelected:
                    self.defaultSelected= False
                    self.returnSelected = True

            if key == 'Right' and self.levelSelected:
                #Increase start level.
                if self.initLevel < 10: self.initLevel += 1

            if key == 'Left' and self.levelSelected:
                #Decrease start level.
                if self.initLevel > 0: self.interval -= 1

            if key == 'Return':
                if self.returnSelected:
                    #Return from settings screen to start screen.
                    self.settingsScreen = False
                    self.startScreen = True
                    self.flashTextFill = 'white'
                    self.drawStartScreen()

                elif self.defaultSelected:
                    #Apply default settings.
                    self.initLevel = 0

        elif self.pauseScreen:

            if key == 'Return':
                if self.returnSelected:
                    #Unpause the game by redrawing entire game screen and
                    #restarting the in-game timer.
                    self.pauseScreen = False
                    self.gamePaused = False
                    self.inGame = True
                    self.delete(ALL)
                    self.drawGameMatrix()
                    self.drawSpawnPiece()
                    self.drawGameData()
                    self.after(self.gameMatrix.dropDelay, self.inGameTimer)

                if self.startSelected:
                    #Restart the game.
                    self.initGame()

                elif self.controlsSelected:
                    #Go from pause screen to the controls info screen.
                    self.pauseScreen = False
                    self.controlsScreen = True
                    self.flashTextFill = 'white'
                    self.drawControlsScreen()

            elif key == 'Down':
                #Traverse options.
                if self.returnSelected:
                    self.returnSelected = False
                    self.startSelected = True
                elif self.startSelected:
                    self.startSelected = False
                    self.controlsSelected = True
                elif self.controlsSelected:
                    self.controlsSelected= False
                    self.returnSelected = True

            elif key == 'Up':
                #Traverse options.
                if self.returnSelected:
                    self.returnSelected = False
                    self.controlsSelected = True
                elif self.controlsSelected:
                    self.controlsSelected = False
                    self.startSelected = True
                elif self.startSelected:
                    self.startSelected= False
                    self.returnSelected = True

        elif self.inGame:

            if key in directions:
                #Send the nudge request to the matrix.
                self.gameMatrix.receiveNudge(directions[key])
                self.drawGameMatrix()

            elif key in rotations:
                #Send the rotation request to the matrix.
                self.gameMatrix.receiveRotation(rotations[key])
                self.drawGameMatrix()

            elif key == 'p':
                #Draw the pause screen and set pause screen flag so that the
                #in-game timer is ignored.
                self.gamePaused = True
                self.pauseScreen = True
                self.inGame = False
                self.returnSelected = True
                self.startSelected = False
                self.controlsSelected = False
                self.flashTextFill = 'white'
                self.drawPauseScreen()

        if key == 'q':
            quit()

    def inGameTimer(self):

        if self.gamePaused:
            #User has paused the game, so ignore timer call and do not
            #continue to trigger timer.
            pass
        
        elif not self.inGame:
            #Draw game over screen, then re-initialise game.
            self.delete(ALL)
            scoreText = 'Score: ' + str(self.gameMatrix.score)
            self.create_text(WINDOWWIDTH/2, WINDOWHEIGHT/3,
                             font = 'Helvetica 36 bold',
                             text='GAME OVER',
                             fill='white')
            self.create_text(WINDOWWIDTH/2, 400,
                             font = 'Helvetica 12',
                             text=scoreText,
                             fill='white')
            self.after(ENDSCREENDELAY, self.initGame)

        elif self.gameMatrix.pieceInPlay:
            #There is a falling piece, so send it a downwards nudge.
            self.gameMatrix.receiveNudge('v')
            self.drawGameMatrix()
            self.after(self.gameMatrix.dropDelay, self.inGameTimer)
            
            #Redraw game data in case it's changed due to the nudge.
            self.drawGameData()
            
        elif self.gameMatrix.spawnReady:
            #No falling piece, so spawn the next tetronimo (this
            #also tells matrix to generate a new spawn).
            self.gameMatrix.spawnTetronimo()
            self.drawSpawnPiece()
            self.drawGameData()
            self.after(self.gameMatrix.dropDelay, self.inGameTimer)
            
        else:
            #In game but no falling piece or spawn ready - wait
            #until next timer pop and hope something has changed!
            self.after(self.gameMatrix.dropDelay, self.inGameTimer)

        
class Sabtris(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        parent.title('Sabtris')
        self.board = GameBoard(parent)
        self.pack()

root = Tk()
sab = Sabtris(root)
root.mainloop()
