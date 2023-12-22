# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

pacmanIndex = 0

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
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # Расстояние до ближайшей еды
    minFoodDistance = min([util.manhattanDistance(newPos, food) for food in oldFood.asList()])

    # Оценка призраков и режима испуга
    ghostEval = 0
    for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
      ghostPos = ghostState.getPosition()
      if scaredTime == 0 and util.manhattanDistance(newPos, ghostPos) < 3:
        # Если призрак не в режиме испуга и близко к пакману, уменьшаем оценку
        ghostEval -= 100
      elif scaredTime > 0 and util.manhattanDistance(newPos, ghostPos) < scaredTime:
        # Если призрак в режиме испуга и близко к пакману, увеличиваем оценку
        ghostEval += 50


    minFoodDistanceScore = 2 if minFoodDistance == 0 else 1/minFoodDistance

    # Суммарная оценка, учитывающая расстояние до еды и состояние призраков
    evaluation = successorGameState.getScore() + minFoodDistanceScore + ghostEval
    return evaluation

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

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = pacmanIndex # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    legalActions = gameState.getLegalActions(pacmanIndex)
    scores = [self.minimax(gameState.generateSuccessor(pacmanIndex, action), 1, pacmanIndex) for action in legalActions]
    bestAction = legalActions[scores.index(max(scores))]
    return bestAction

  def minimax(self, state, depth, agentIndex):
    if depth == self.depth or state.isWin() or state.isLose():
      return self.evaluationFunction(state)

    legalActions = state.getLegalActions(agentIndex)
    nextAgent = (agentIndex + 1) % state.getNumAgents()

    if agentIndex == pacmanIndex:  # Ход Pacman (слой Max)
      return max(self.minimax(state.generateSuccessor(agentIndex, action), depth, nextAgent) for action in legalActions)
    else:  # Ход призраков (слой Min)
      return min(self.minimax(state.generateSuccessor(agentIndex, action), depth + 1, nextAgent) for action in legalActions)

class AlphaBetaAgent(MultiAgentSearchAgent):
  def getAction(self, gameState):
    legalActions = gameState.getLegalActions(pacmanIndex)  # 0 - индекс Pacman
    alpha = float("-inf")
    beta = float("inf")
    bestScore = float("-inf")
    bestAction = None

    for action in legalActions:
      score = self.alphabeta(gameState.generateSuccessor(pacmanIndex, action), 1, pacmanIndex, alpha, beta)
      if score > bestScore:
        bestScore = score
        bestAction = action
      alpha = max(alpha, bestScore)

    return bestAction

  def alphabeta(self, state, depth, agentIndex, alpha, beta):
    stack = [(state, depth, agentIndex, alpha, beta)]
    while stack:
      state, depth, agentIndex, alpha, beta = stack.pop()
      if depth == self.depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)

      legalActions = state.getLegalActions(agentIndex)
      nextAgent = (agentIndex + 1) % state.getNumAgents()

      if agentIndex == 0:  # Ход Pacman (слой Max)
        value = float("-inf")
        for action in legalActions:
          successor = state.generateSuccessor(agentIndex, action)
          value = max(value, self.evaluationFunction(successor))
          alpha = max(alpha, value)
          if value >= beta:
            break
        stack.append((state, depth, nextAgent, alpha, beta))
      else:  # Ход призраков (слой Min)
        value = float("inf")
        for action in legalActions:
          successor = state.generateSuccessor(agentIndex, action)
          value = min(value, self.evaluationFunction(successor))
          beta = min(beta, value)
          if value <= alpha:
            break
        stack.append((state, depth + 1, nextAgent, alpha, beta))

    return value

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

