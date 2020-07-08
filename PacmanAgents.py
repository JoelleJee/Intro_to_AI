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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        Design a better evaluation function here.

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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        i = 0
        j = 0
        foodDistance = 1
        ghostDistance = 1
        ghostFoodDistance = 1
        numFood = successorGameState.getNumFood()
        if numFood == 0:
            numFood = 1

        while i < newFood.width:
            j = 0
            while j < newFood.height:
                if newFood[i][j] == True:
                    for ghost in newGhostPositions:
                        distance = abs(i - ghost[0]) + abs(j - ghost[1])
                        if distance != 0:
                            ghostFoodDistance += distance
                        distance = abs(newPos[0] - i) + abs(newPos[1] - j)
                        if distance != 0:
                            foodDistance += distance
                j += 1
            i += 1

        ghostFoodDistance = float(ghostFoodDistance / (successorGameState.getNumAgents() - 1))

        for ghost in newGhostPositions:
            distance = abs(newPos[0] - ghost[0]) + abs(newPos[1] - ghost[1])
            if distance != 0:
                ghostDistance += distance
        ghostDistance = float(ghostDistance / (successorGameState.getNumAgents() - 1))

        avgScaredTimes = 1
        for t in newScaredTimes:
            avgScaredTimes += t

        return 2*float(ghostDistance/foodDistance)+ 9*float(1 / ghostFoodDistance) + 8 * float(1/ numFood) - float(1 / avgScaredTimes)


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

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getMini(self, gameState, totalA, agentI, d):
        """
        Return the score of the Successor gameState that produces the minimum game score.
        """
        miniScore = float("inf")
        agentScore = None

        agentMoves = gameState.getLegalActions(agentI)

        for a in agentMoves:
            agentSuccessor = gameState.generateSuccessor(agentI, a)
            # If action a leads to Pacman losing than return -1
            if agentSuccessor.isLose() is True or agentSuccessor.isWin() is True:
                agentScore = self.evaluationFunction(agentSuccessor)
            #     break
            # # If action a leads to Pacman winning, move on to the next node.
            # elif agentSuccessor.isWin() is True:
            #     miniScore = self.evaluationFunction(agentSuccessor)
            #     continue
            # If action a does not lead to a terminal node than recurse to find the minimum value of the successor
            elif agentI != totalA - 1:
                agentScore = self.getMini(agentSuccessor, totalA, agentI+1, d)
            elif agentI == totalA - 1:
                if d == 0:
                    agentScore = self.evaluationFunction(agentSuccessor)
                else:
                    agentScore = self.getMax(agentSuccessor, d)
            miniScore = min(miniScore, agentScore)

        return miniScore


    def getMax(self, gameState, d):
        """
        Return the move that generates the maximum successor game score
        """
        optScore = -float("inf")
        optMove = None

        totalA = gameState.getNumAgents()
        pacActions = gameState.getLegalActions(0)

        for a in range(0, len(pacActions)):
            pacMove = gameState.generateSuccessor(0, pacActions[a])
            if pacMove.isWin() is True or pacMove.isLose() is True:
                agentIScore = self.evaluationFunction(pacMove)
            else:
                agentIScore = self.getMini(pacMove, totalA, 1, d - 1)
            if optMove is None \
                or (optScore < agentIScore):
                optScore = agentIScore
                optMove = pacActions[a]
        if d == self.depth:
            return optMove
        else:
            return optScore

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
        """
        "*** YOUR CODE HERE ***"
        return self.getMax(gameState, self.depth)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getMiniMax(self, gameState, agentI, totalA, alpha, beta, d):
        #terminal node
        if gameState.isWin() is True or gameState.isLose() is True or d == -1:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentI)
        move = None
        maxSucScore = -float("inf")

        #pacman
        if agentI == 0:
            for a in actions:
                s = gameState.generateSuccessor(0, a)
                maxSucScore = max(maxSucScore, self.getMiniMax(s, 1, totalA, alpha, beta, d - 1))
                if maxSucScore > alpha:
                    alpha = maxSucScore
                    move = a
                if beta <= alpha:
                    break
            if d == self.depth:
                return move
            else:
                return alpha

        elif agentI != totalA - 1:
            for a in actions:
                s = gameState.generateSuccessor(agentI, a)
                beta = min(beta, self.getMiniMax(s, agentI + 1, totalA, alpha, beta, d))
                if beta <= alpha:
                    break
            return beta

        elif agentI == totalA - 1:
            for a in actions:
                s = gameState.generateSuccessor(agentI, a)
                if d != 0:
                    beta = min(beta, self.getMiniMax(s, 0, totalA, alpha, beta, d))
                else:
                    beta = min(beta, self.getMiniMax(s, agentI, totalA, alpha, beta, d - 1))
                if beta <= alpha:
                    break
            return beta


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.getMiniMax(gameState, 0, gameState.getNumAgents(), -float("inf"), float("inf"), self.depth)



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getExpectiMax(self, gameState, agentI, numAgents, d):

        #terminal nodes
        if gameState.isWin() is True or gameState.isLose() is True or d == -1:
            return self.evaluationFunction(gameState)

        if agentI == 0: #MAX
            value = -float("inf")
            optMove = None
        else: #CHANCE
            value = 0

        actions = gameState.getLegalActions(agentI)

        for a in actions:
            agentMove = gameState.generateSuccessor(agentI, a)
            if agentI != 0: #chance nodes
                if agentI == numAgents - 1: #last agent
                    if d != 0: #start another depth of search
                        value += self.getExpectiMax(agentMove, 0, numAgents, d)
                    else: #self.depth reached
                        value += self.getExpectiMax(agentMove, agentI, numAgents, d - 1)
                else: #move onto next agent
                    value += self.getExpectiMax(agentMove, agentI + 1, numAgents, d)
            else: #max node
                succScore = self.getExpectiMax(agentMove, 1, numAgents, d - 1)
                if value < succScore:
                    optMove = a
                    value = succScore

        if agentI != 0:
            return float(value / len(actions))
        elif agentI == 0:
            if d == self.depth:
                return optMove
            else:
                return value

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.getExpectiMax(gameState, 0, gameState.getNumAgents(), self.depth)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newGhostPositions = currentGameState.getGhostPositions()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    i = 0
    foodDistance = 1
    ghostDistance = 1
    ghostFoodDistance = 1
    numFood = currentGameState.getNumFood()
    if numFood == 0:
        numFood = 1

    while i < newFood.width:
        j = 0
        while j < newFood.height:
            if newFood[i][j] == True:
                for ghost in newGhostPositions:
                    distance = abs(i - ghost[0]) + abs(j - ghost[1])
                    if distance != 0:
                        ghostFoodDistance += distance
                    distance = abs(newPos[0] - i) + abs(newPos[1] - j)
                    if distance != 0:
                        foodDistance += distance
            j += 1
        i += 1

    if foodDistance != 0:
        foodDistance = float(numFood / foodDistance)

    ghostFoodDistance = float(ghostFoodDistance / (currentGameState.getNumAgents() - 1))

    for ghost in newGhostPositions:
        distance = abs(newPos[0] - ghost[0]) + abs(newPos[1] - ghost[1])
        if distance != 0:
            ghostDistance += distance
    ghostDistance = float(ghostDistance / (currentGameState.getNumAgents() - 1))

    avgScaredTimes = 0
    for t in newScaredTimes:
        avgScaredTimes += t
    if avgScaredTimes != 0:
        avgScaredTimes = float(1 / avgScaredTimes)

    return -1*float(1 / ghostDistance) + 5*foodDistance + 500 * float(1 / numFood) - 200*avgScaredTimes


# Abbreviation
better = betterEvaluationFunction
