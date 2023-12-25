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

    # Add more of your code here if you want to

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

    # Считаем оценку расстояния до еды
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
    self.index = pacmanIndex
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
    legalActions = gameState.getLegalActions(pacmanIndex)
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

      if agentIndex == pacmanIndex:  # Ход Pacman (слой Max)
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
  def getAction(self, gameState):
    legalActions = gameState.getLegalActions(pacmanIndex)
    scores = [self.expectimax(gameState.generateSuccessor(pacmanIndex, action), 1, pacmanIndex) for action in legalActions]
    bestAction = legalActions[scores.index(max(scores))]
    return bestAction

  def expectimax(self, state, depth, agentIndex):
    if depth == self.depth or state.isWin() or state.isLose():
      return self.evaluationFunction(state)

    legalActions = state.getLegalActions(agentIndex)
    nextAgent = (agentIndex + 1) % state.getNumAgents()

    if agentIndex == 0:  # Ход Pacman (слой Max)
      return max(self.expectimax(state.generateSuccessor(agentIndex, action), depth, nextAgent) for action in legalActions)
    else:  # Ход призраков (слой Expectation)
      return sum(self.expectimax(state.generateSuccessor(agentIndex, action), depth + 1, nextAgent) for action in legalActions) / len(legalActions)

def betterEvaluationFunction(currentGameState):
  pacmanPosition = currentGameState.getPacmanPosition()
  currentScore = currentGameState.getScore()
  ghostPositions = currentGameState.getGhostPositions()
  remainingFood = currentGameState.getFood().asList()
  capsules = currentGameState.getCapsules()

  minGhostDistance = min([manhattanDistance(pacmanPosition, ghostPos) for ghostPos in ghostPositions]) if ghostPositions else 0
  minFoodDistance = min([manhattanDistance(pacmanPosition, food) for food in remainingFood]) if remainingFood else 0
  minCapsuleDistance = min([manhattanDistance(pacmanPosition, capsule) for capsule in capsules]) if capsules else 0

  scoreWeight = 10 * currentScore
  ghostWeight = 100 * minGhostDistance
  foodWeight = -10 * minFoodDistance
  capsuleWeight = 15 * minCapsuleDistance

  addBonus = 0

  if minCapsuleDistance < minGhostDistance / 2:
    addBonus += 10000 * 1/(minCapsuleDistance + 1)

  if currentGameState.getPacmanState().scaredTimer > 0:
    addBonus += 1000

  return scoreWeight + ghostWeight + foodWeight + capsuleWeight + addBonus

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  def getAction(self, gameState):
    legalActions = gameState.getLegalActions(pacmanIndex)
    scores = [self.expectimax(gameState.generateSuccessor(pacmanIndex, action), 1, pacmanIndex) for action in legalActions]

    # Проверяем, не окружен ли пакман призраками
    if self.isPacmanTrapped(gameState):
      # Если окружен, выбираем лучшее действие из всех доступных
      bestAction = legalActions[scores.index(max(scores))]
    else:
      # Иначе, применяем стратегии избегания призраков, приближения к капсулам, предпочтения дорог с едой и избегания тупиков
      filteredActions = self.filterActions(gameState, legalActions)
      if len(filteredActions) > 0:
        scores = [self.expectimax(gameState.generateSuccessor(pacmanIndex, action), 1, pacmanIndex) for action in filteredActions]
        bestAction = filteredActions[scores.index(max(scores))]
      else:
        bestAction = legalActions[scores.index(max(scores))]

    return bestAction

  def expectimax(self, state, depth, agentIndex):
    if depth == self.depth or state.isWin() or state.isLose():
      return self.evaluationFunction(state)

    legalActions = state.getLegalActions(agentIndex)
    nextAgent = (agentIndex + 1) % state.getNumAgents()

    if agentIndex == 0:  # Ход Pacman (слой Max)
      return max(self.expectimax(state.generateSuccessor(agentIndex, action), depth, nextAgent) for action in legalActions)
    else:  # Ход призраков (слой Expectation)
      return sum(self.expectimax(state.generateSuccessor(agentIndex, action), depth + 1, nextAgent) for action in legalActions) / len(legalActions)

  def isPacmanTrapped(self, gameState):
    pacmanPosition = gameState.getPacmanPosition()
    legalActions = gameState.getLegalActions(0)  # Действия для пакмана

    # Пакман окружен, если у него меньше вариантов движения, чем у призраков
    return len(legalActions) <= gameState.getNumAgents() - 1

  def filterActions(self, gameState, legalActions):
    pacmanPosition = gameState.getPacmanPosition()

    # Избегание близких призраков
    filteredActions = [action for action in legalActions if self.isSafeFromGhosts(gameState.generateSuccessor(0, action))]

    # Приближение к капсулам
    filteredActions = self.moveToCapsules(gameState, filteredActions)

    # Предпочтение дорог с едой
    if gameState.getNumFood() > 0:
      filteredActions = self.moveToFood(gameState, filteredActions)

    # Избегание тупиков
    filteredActions = self.avoidDeadEnds(gameState, filteredActions)

    return filteredActions

  def isSafeFromGhosts(self, gameState):
    ghostPositions = [ghost.getPosition() for ghost in gameState.getGhostStates() if not ghost.scaredTimer > 0]
    return all(manhattanDistance(gameState.getPacmanPosition(), ghost) >= 2 for ghost in ghostPositions)

  def moveToCapsules(self, gameState, legalActions):
    capsulePositions = gameState.getCapsules()
    return sorted(legalActions, key=lambda action: min(manhattanDistance(gameState.getPacmanPosition(), capsule) for capsule in capsulePositions)) if len(capsulePositions) > 0 else legalActions

  def moveToFood(self, gameState, legalActions):
    foodPositions = gameState.getFood().asList()
    return sorted(legalActions, key=lambda action: min(manhattanDistance(gameState.getPacmanPosition(), food) for food in foodPositions))

  def avoidDeadEnds(self, gameState, legalActions):
    pacmanPosition = gameState.getPacmanPosition()
    ghostPositions = [ghost.getPosition() for ghost in gameState.getGhostStates()]

    # Фильтруем действия, чтобы оставить только те, где у пакмана больше вариантов движения, чем у призраков в пределах 5 клеток
    filteredActions = [action for action in legalActions if self.countPossiblePacmanMoves(gameState.generateSuccessor(0, action)) > len(gameState.getGhostStates())
                       or any(manhattanDistance(pacmanPosition, ghost) <= 5 for ghost in ghostPositions)]

    return filteredActions

  def countPossiblePacmanMoves(self, gameState):
    pacmanPosition = gameState.getPacmanPosition()
    legalActions = gameState.getLegalActions(0)  # Действия для пакмана
    possibleMoves = 0

    for action in legalActions:
      successorGameState = gameState.generateSuccessor(0, action)
      successorPacmanPosition = successorGameState.getPacmanPosition()

      # Проверяем, что пакман на следующем шаге не стоит на месте
      if successorPacmanPosition != pacmanPosition:
        possibleMoves += 1

    return possibleMoves