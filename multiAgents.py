# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import numpy as np

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
    """

    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        curPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        curFoodList = currentGameState.getFood().asList()
        ghostList = successorGameState.getGhostStates()
        foodScore = 10
        ghostScore = -10
        score = 0
        foodDist = 1000
        ghostDist = 0

        for f in curFoodList:
            if currentGameState.hasFood(newPos[0], newPos[1]):
                foodDist += foodScore
            else:
                manDist = util.manhattanDistance(newPos, f)+.001
                foodDist += foodScore * 1/manDist
        score += foodDist

        for s in ghostList:
            if newPos in s.getPosition():
                ghostDist += ghostScore
            else:
                manDist = util.manhattanDistance(newPos, s.getPosition())+.001
                ghostDist += ghostScore * 1/manDist
        score += ghostDist

        if action == Directions.STOP:
            score += ghostScore

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    This is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    # def __init__(self,):
    #     self.pacman_id = 0
    #     self.numGhosts = None

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        # def minimax(agent, depth, gameState):
        #     if gameState.isLose() or gameState.isWin() or depth == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
        #         return self.evaluationFunction(gameState)
        #     if agent == 0:  # maximize for pacman
        #         return max(minimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in
        #                    gameState.getLegalActions(agent))
        #     else:  # minize for ghosts
        #         nextAgent = agent + 1  # calculate the next agent and increase depth accordingly.
        #         if gameState.getNumAgents() == nextAgent:
        #             nextAgent = 0
        #         if nextAgent == 0:
        #             depth += 1
        #         return min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in
        #                    gameState.getLegalActions(agent))
        #
        # """Performing maximize action for the root node i.e. pacman"""
        # maximum = float("-inf")
        # action = Directions.WEST
        # for agentState in gameState.getLegalActions(0):
        #     utility = minimax(1, 0, gameState.generateSuccessor(0, agentState))
        #     if utility > maximum or maximum == float("-inf"):
        #         maximum = utility
        #         action = agentState
        # return action


        # # Collect legal moves and successor states
        # legalMoves = gameState.getLegalActions()
        # if "Stop" in legalMoves:
        #     legalMoves.remove("Stop")
        # self.numAgents = gameState.getNumAgents()
        self.pacman_idx = 0
        # self.depth = 2
        actions_list = gameState.getLegalActions(agentIndex=self.pacman_idx)
        # if "Stop" in actions_list:
        #     actions_list.remove("Stop")
        actions_list = np.random.permutation(actions_list)

        max_value = float('-inf')
        max_action = None

        for action in actions_list:  # get the max value from all successors.
            action_value = self.Min_Value(gameState.generateSuccessor(agentIndex=self.pacman_idx, action=action), agentIndex=1, depth=0)
            if ((action_value) > max_value):  # take the max of all the children.
                max_value = action_value
                max_action = action
        # print(f"max value: {max_value}, max_action: {max_action}")
        return max_action

    def Min_Value (self, gameState, agentIndex, depth):
        actions_list = gameState.getLegalActions(agentIndex=agentIndex)
        actions_list = np.random.permutation(actions_list)
        # if "Stop" in actions_list:
        #     actions_list.remove("Stop")

        if gameState.isLose() or gameState.isWin() or depth >= self.depth: # or len(actions_list) ==0:
            return self.evaluationFunction(gameState)
        numAgents = gameState.getNumAgents()
        next_agent = self.pacman_idx if agentIndex == numAgents -1 else agentIndex + 1
        if agentIndex == self.pacman_idx:
            min_value = max(self.Min_Value(gameState.generateSuccessor(agentIndex, action), next_agent, depth) for action in actions_list)
        else:
            if next_agent == self.pacman_idx:
                depth += 1
            min_value = min(self.Min_Value(gameState.generateSuccessor(agentIndex, action), next_agent, depth) for action in actions_list)

        return min_value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Expectimax agent
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function.

    """
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
