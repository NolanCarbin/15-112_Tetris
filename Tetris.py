#################################################
# Tetris
#
# Your name: Nolan Carbin   
# 
#################################################

import pygame
import math, copy, random 
from cmu_112_graphics import *


#Default Dimensions: 15,10,20,25
def gameDimensions():
    rows = 15 
    cols = 10 
    cellSize = 35 
    margin = 25
    return (rows, cols, cellSize, margin)

def playTetris():
    pygame.mixer.init()
    pygame.mixer.music.load('tetris.mid')
    rows, cols, cellSize, margin = gameDimensions()
    width = (cols * cellSize) + 2 * margin
    height = (rows * cellSize) + 2 * margin
    runApp(width=width, height=height)

def appStarted(app):
    app.gameOver = False
    app.bonusMode = False
    playMusic(app)
    app.timerDelay = 400 #Changes the speed of the fallingBlocks
    app.score = 0
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.emptyColor = 'blue'
    app.board = [ ([app.emptyColor] * app.cols) for row in range(app.rows) ]

    iPiece = [ [True, True, True, True] ]

    jPiece = [ [True, False, False], 
               [True, True,  True] ]

    lPiece = [ [False, False, True], 
               [True,  True,  True] ]

    oPiece = [ [True, True], 
               [True, True] ]

    sPiece = [ [False, True, True], 
               [True,  True, False] ]

    tPiece = [ [False, True, False], 
               [True,  True, True] ]

    zPiece = [ [True, True, False], 
               [False, True, True] ] 

    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    app.tetrisColors = ['red', 'yellow', 'magenta', 'pink', 
                        'cyan', 'green', 'orange']
    newFallingPiece(app) #Starts the first fallingPiece
    app.bonusMessage = '''!Bonus Mode:.
    When Bonus Mode is enabled:
    
     '''

def appStopped(app):
    pygame.mixer.music.stop() 

def playMusic(app):
    pygame.mixer.music.play(loops=6)
    
#Creates a new falling piece from app.tetrisPieces, app.tetrisColors 
#app.fallingPieceRow and app.fallingPieceCol hold the top left cell 
#of the piece.
def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisColors[randomIndex]
    numFallingPieceRows = len(app.fallingPiece) 
    numFallingPieceCols = len(app.fallingPiece[0])
    app.fallingPieceRow  = 0 #Always starts at the top row
    app.fallingPieceCol = (app.cols // 2) - (numFallingPieceCols // 2)
                          #^ This sets the pieces starting col, to be in the 
                          #  center of the board based on the boards dimensions.

#Moves the fallingPiece in the given direction.
#This moves the piece first, then checks if the movement was legal, and if not
#it reversed the movement. 
#If it return True, then we know that the piece moved, if it returns False,
#then the piece did not move.
def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    if not fallingPieceIsLegal(app):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    return True

#Determines the each row and col in the fallingPiece that is a block
#and checks if each one is in within the board and doesn't overlap a already
#filled block.
#True values represent the blocks of the fallingPiece. 
def fallingPieceIsLegal(app):
    rows, cols = len(app.fallingPiece), len(app.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if app.fallingPiece[row][col] == True: 
                cellRow = row + app.fallingPieceRow
                cellCol = col + app.fallingPieceCol
                if not inBounds(app, cellRow, cellCol): #Checks if on the board
                    return False
                if app.board[cellRow][cellCol] != app.emptyColor: 
                    return False              #Checks if cell is already filled
    return True

#Helperfunction to check if the given cell is on the board.
def inBounds(app, row, col):
    if (row < 0 or row > (app.rows - 1) or 
        col < 0 or col > (app.cols - 1)):
        return False
    return True

#When called this function will rotate the app.fallingPiece counterclockwise.
#First it sets the original values the creates a new list to copy the rotated
#piece into. It then checks if the rotation is legal, if not, it will restore
#the piece to the original values. 
def rotateFallingPiece(app):
    originalPiece = app.fallingPiece
    originalRows = len(app.fallingPiece)
    originalCols = len(app.fallingPiece[0])
    newRows = len(app.fallingPiece[0])
    newCols = len(app.fallingPiece)
    oldRow = app.fallingPieceRow
    oldCol = app.fallingPieceCol
    newRow = oldRow + originalRows // 2 - newRows // 2
    newCol = oldCol + originalCols // 2 - newCols // 2

    newRotation = [ ([None] * newCols) for row in range(newRows) ]
    for row in range(originalRows):
        for col in range(originalCols):
            rotationRow = (originalCols - 1) - col 
            rotationCol = row
            newRotation[rotationRow][rotationCol] = app.fallingPiece[row][col]
    #These set the fallingPiece to the new rotation:
    app.fallingPiece = newRotation
    app.fallingPieceRow = newRow
    app.fallingPieceCol = newCol
    if not fallingPieceIsLegal(app):
        #Reverts the piece if not legal
        app.fallingPiece = originalPiece
        app.fallingPieceRow = oldRow
        app.fallingPieceCol = oldCol

#Drops the fallingPiece all the way to the bottom.
def hardDrop(app):
    # moves the fallingPiece down by 1 until it can't go any further. 
    while moveFallingPiece(app, +1, 0):
        moveFallingPiece(app, +1, 0)

def keyPressed(app, event):
    if event.key == 'r': 
        if app.bonusMode:
            appStarted(app)
            app.bonusMode = True 
        else:
            appStarted(app)

    if event.key == 'p': 
        pygame.mixer.music.stop()
    if event.key == 's': 
        playMusic(app)
    if event.key == 'b': 
        print(app.bonusMessage)
        initializeBonus(app)
       
    if not app.gameOver:
        if event.key == 'Left': moveFallingPiece(app, 0, -1)
        if event.key == 'Right': moveFallingPiece(app, 0, +1) 
        if event.key == 'Down': moveFallingPiece(app, +1, 0) 
        if event.key == 'Up': rotateFallingPiece(app)
        if event.key == 'Space': hardDrop(app)

def initializeBonus(app):
    app.bonusMode = True
    


#If moveFallingPiece(app, +1, 0) returns False, then we know that the piece
#cannot move anymore and it then adds the piece to the app.board with 
#placeFallingPiece(app)
#If fallingPieceIsLegal returns False directly after we add a new piece then 
#we know that there is no room to add anymore pieces, which indicates the game
#is over.
def timerFired(app):
    if not app.gameOver:
        if moveFallingPiece(app, +1, 0) == False:
            placeFallingPiece(app)
            newFallingPiece(app)
            if not fallingPieceIsLegal(app):
                app.gameOver = True
    else:
        pygame.mixer.music.stop()

#Similar to drawFallingPiece(), it goes through the fallingPiece, 
#and sets the row and col of the board to the row and col of the piece.
#This function calls removeFullRows(app) after each cell is added to check
#if adding that cell creates any fullRows. 
def placeFallingPiece(app):
    rows, cols = len(app.fallingPiece), len(app.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if app.fallingPiece[row][col] == True:
                pieceRow = row + app.fallingPieceRow
                pieceCol = col + app.fallingPieceCol 
                app.board[pieceRow][pieceCol] = app.fallingPieceColor
                removeFullRows(app)

#This function checks the board for any full rows. 
#Its creates a new board list and adds every row that isn't full of pieces. 
#It keeps track of the number of fullRows and at the end, if there are more 
#than one full row it will insert a empty row of app.emptyColors to the top 
#of the new board. 
#This also keeps track of the app.score. For every fullRow that is removed. 
#The score will be squared and then added to the total score.
def removeFullRows(app):
    newBoard = []
    fullRows = 0
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        if app.emptyColor not in app.board[row]:
            fullRows += 1
        else:
            newBoard.append(app.board[row])
    if fullRows >= 1:
        for i in range(fullRows):
            newBoard.insert(0, ([app.emptyColor] * cols))
    app.board = newBoard
    app.score += (fullRows ** 2)
    

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill='orange')
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    if app.gameOver:
        drawGameOver(app, canvas)

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, canvas, row, col, color)

def drawCell(app, canvas, row, col, color):
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=4)

def getCellBounds(app, row, col):
    gridWidth = app.width - app.margin * 2
    gridHeight = app.height - app.margin * 2
    x0 = app.margin + col * app.cellSize
    y0 = app.margin + row * app.cellSize
    x1 = x0 + app.cellSize
    y1 = y0 + app.cellSize
    return x0, y0, x1, y1

def drawFallingPiece(app, canvas):
    rows, cols = len(app.fallingPiece), len(app.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if app.fallingPiece[row][col] == True:
                pieceRow = row + app.fallingPieceRow
                pieceCol = col + app.fallingPieceCol 
                drawCell(app, canvas, pieceRow, pieceCol, app.fallingPieceColor)
    
def drawGameOver(app, canvas):
    x0,y0,x1,y1 = getCellBounds(app, 1, 0)
    x2,y2,x3,y3 = getCellBounds(app, 2, app.cols - 1)
    canvas.create_rectangle(x0,y0,x3,y3, fill='black')
    textX = app.width / 2 
    textY = y1
    canvas.create_text(textX, textY, text='GAME OVER!', fill='yellow', 
        font='Arial, 24 bold')

def drawScore(app, canvas):
    x = app.width / 2
    y = app.margin / 2
    font = f'Arial {app.margin - 15} bold'
    canvas.create_text(x,y,text=f'Score: {app.score}', fill='blue', 
            font=font)



#################################################
# main
#################################################

def main():
    playTetris()

if __name__ == '__main__':
    main()
