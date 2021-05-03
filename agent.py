from game import *

class Agent:
    def __init__(self):
        pass

    def getMove(self, game):
        pass

class keyboardAgent(Agent):
    def __init__(self):
        self.moves = [(0, 0), (1, 0), (2, 0), (2, 2)]
        self.m = 0

    def getMove(self, game):
        move = self.moves[self.m]
        self.m += 1
        return move
        while True:
            pointPlay = game.win.getMouse()
            x = pointPlay.x // game.GRID_SIZE - 1
            y = pointPlay.y // game.GRID_SIZE - 1
            if (x, y) in game.movesPlayed[0] or (x, y) in game.movesPlayed[1]:
                continue

            if x in range(game.board_size) and y in range(game.board_size):
                break
        print(x,y,'xxxx')
        return (x, y)

class minimaxAgent(Agent):
    def __init__(self):
        pass

    def getMove(self, game):
        print('Minimax is computing!')
        game = offlineGame(game)
        moves = game.getLegalMoves()
        move_score = [[], []]
        for move in game.getLegalMoves():
            move_score[1].append(self.value(game.getSuccessor(move)))
            move_score[0].append(move)

        for i in range(len(move_score[0])):
            if game.turn:
                if move_score[1][i] == min(move_score[1]):
                    return tuple(move_score[0][i])
            else:
                if move_score[1][i] == max(move_score[1]):
                    return tuple(move_score[0][i])
        return move 
    
    def value(self, game, depth=2):
        score = game.isFinished()
        if score == 0:
            if depth == 0:
                return 0
            if game.turn:
                return self.min_value(game, depth-1) * 0.99
            else:
                return self.max_value(game, depth-1) * 0.99
        elif score == 2:
            return 0
        else:
            return score

    def max_value(self, game, depth):
        v = -2
        for move in game.getLegalMoves():
            v = max(v, self.value(game.getSuccessor(move), depth))
        return v

    def min_value(self, game, depth):
        v = 2
        for move in game.getLegalMoves():
            v = min(v, self.value(game.getSuccessor(move), depth))
        return v

class alphabetaPruning(Agent):
    def __init__(self):
        pass

    def getMove(self, game):
        print('Alphabeta is computing!')
        game = offlineGame(game)
        moves = game.getLegalMoves()
        move_score = [[], []]
        for move in game.getLegalMoves():
            move_score[1].append(self.value(game.getSuccessor(move)))
            move_score[0].append(move)

        for i in range(len(move_score[0])):
            if game.turn:
                if move_score[1][i] == min(move_score[1]):
                    return tuple(move_score[0][i])
            else:
                if move_score[1][i] == max(move_score[1]):
                    return tuple(move_score[0][i])
        return move 
    
    def value(self, game, alpha=-3, beta=3, depth=1):
        score = game.isFinished()
        if score == 0:
            if depth == 0:
                return 0
            if game.turn:
                return self.min_value(game, alpha, beta, depth-1) * 0.99
            else:
                return self.max_value(game, alpha, beta, depth-1) * 0.99
        elif score == 2:
            return 0
        else:
            return score

    def max_value(self, game, alpha, beta, depth):
        v = -2
        for move in game.getLegalMoves():
            v = max(v, self.value(game.getSuccessor(move), alpha, beta, depth))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, game, alpha, beta, depth):
        v = 2
        for move in game.getLegalMoves():
            v = min(v, self.value(game.getSuccessor(move), alpha, beta, depth))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v