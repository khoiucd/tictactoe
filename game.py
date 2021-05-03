from graphics import *
import numpy as np

GRID_SIZE = 30
PLAY_SIZE = 26

dxdyChecks = [[(_,_) for _ in range(3)], [(_,-_) for _ in range(3)], [(_,0) for _ in range(3)], [(0,_) for _ in range(3)]]

class Game:
    def __init__(self, board_size):
        self.board = np.zeros((5, board_size, board_size))
        self.board_size = board_size
        self.GRID_SIZE = GRID_SIZE
        self.turn = False
        self.win = self.drawGrid()
        self.PLAY_SIZE = PLAY_SIZE
        self.movesPlayed = [{}, {}]
        self.text = Text(Point(self.win_size // 2, self.win_size - GRID_SIZE // 2), "Red")
        self.setText()
        self.text.draw(self.win)

    def drawGrid(self):
        self.win_size = GRID_SIZE * (self.board_size + 2)
        win = GraphWin("Board", self.win_size , self.win_size)
        for col in range(self.board_size + 1):
            l = Line(Point((col+1) * GRID_SIZE, GRID_SIZE), Point((col+1) * GRID_SIZE, (self.board_size + 1) * GRID_SIZE))
            l.draw(win)
            l.setWidth(2)
            l.setFill("black")

        for row in range(self.board_size + 1):
            l = Line(Point(GRID_SIZE, (row+1) * GRID_SIZE), Point((self.board_size + 1) * GRID_SIZE, (row+1) * GRID_SIZE))
            l.draw(win)
            l.setWidth(2)
            l.setFill("black")

        return win

    def makeMove(self, move):
        if move in self.movesPlayed[0] or move in self.movesPlayed[1]:
            return

        self.fillCheck(move)

        center = self.getCenter(move)
        self.board[0, move[0], move[1]] = (-1) ** self.turn

        if self.turn:
            self.movesPlayed[self.turn][move] = self.drawCross(center)
        else:
            self.movesPlayed[self.turn][move] = self.drawCircle(center)


    def drawCross(self, center):
        c = Circle(Point(center[0], center[1]), PLAY_SIZE // 2)
        c.setWidth(2)
        c.setOutline("blue")
        c.draw(self.win)
        return c

    def drawCircle(self, center):
        c = Circle(Point(center[0], center[1]), PLAY_SIZE // 2)
        c.setWidth(2)
        c.setOutline("red")
        c.draw(self.win)
        return c

    def getCenter(self, move):
        centerX = (move[0] + 1) * self.GRID_SIZE + self.GRID_SIZE // 2
        centerY = (move[1] + 1) * self.GRID_SIZE + self.GRID_SIZE // 2
        return (centerX, centerY)

    def drawBefore(self, move):
        x, y = move
        for dx, dy in diaLeft:
            nextX = x + dx
            nextY = y + dy
            if nextX in range(self.board_size) and nextY in range(self.board_size):
                self.makeMove((nextX, nextY))

    def fillCheck(self, move):
        x, y = move

        for i in range(4):
            for dx, dy in dxdyChecks[i]:
                nextX = x + dx
                nextY = y + dy
                if nextX in range(self.board_size) and nextY in range(self.board_size):
                    self.board[i+1, nextX, nextY] += (-1) ** self.turn

    def isFinished(self):
        if self.board[1:].min() == -3:
            self.text.setText("Blue wins")
            self.text.setOutline("blue")
            return True

        if self.board[1:].max() == 3:
            self.text.setText("Red wins")
            self.text.setOutline("red")
            return True

        if (self.board[0] != 0).prod() != 0:
            return True

        return False

    def setText(self):
        if not self.turn:
            self.text.setText("Red")
            self.text.setOutline("red")
        else:
            self.text.setText("Blue")
            self.text.setOutline("blue")

    def switchTurn(self):
        self.turn = not self.turn
        self.setText()

class offlineGame:
    def __init__(self, game):
        self.board = np.copy(game.board)
        self.turn = game.turn
        self.board_size = game.board_size

    def getLegalMoves(self):
        moves = []
        for r in np.argwhere(self.board[0] == 0):
            moves.append(r.tolist())
        return moves

    def getSuccessor(self, move):
        game = offlineGame(self)
        game.makeMove(move)
        game.switchTurn()
        return game

    def isFinished(self):
        if self.board[1:].min() == -3:
            return -1
        if self.board[1:].max() == 3:
            return 1
        if (self.board[0] != 0).prod() != 0:
            return 2
        return 0

    def makeMove(self, move):
        if self.board[0, move[0], move[1]] != 0:
            return
        self.fillCheck(move)
        self.board[0, move[0], move[1]] = (-1) ** self.turn

    def fillCheck(self, move):
        x, y = move
        for i in range(4):
            for dx, dy in dxdyChecks[i]:
                nextX = x + dx
                nextY = y + dy
                if nextX in range(self.board_size) and nextY in range(self.board_size):
                    self.board[i+1, nextX, nextY] += (-1) ** self.turn

    def switchTurn(self):
        self.turn = not self.turn