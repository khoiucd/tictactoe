from game import *
import agent

def main():
    agents = [agent.minimaxAgent(), agent.alphabetaPruning()]
    game = Game(6)
    while not game.isFinished():
        game.win.getMouse()
        agentInstance = agents[game.turn]
        move = agentInstance.getMove(game)
        game.makeMove(move)
        game.switchTurn()
    
    game.win.getMouse()
    game.win.close()

main()