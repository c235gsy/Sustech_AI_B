# ghostAgents.py
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


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()

class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ):
            dist[a] = 1.0
        dist.normalize()
        return dist

class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared:
            speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance(pos, pacmanPosition ) for pos in newPositions]

        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist

class MinimaxGhost(GhostAgent):

    """
      Your minimax agent (question 1)

      useage: python2 pacman.py -p ExpectimaxAgent -l newLayout -g MinimaxGhost -a depth=4
              python2 pacman.py -l newLayout -g MinimaxGhost

    """
    "*** YOUR CODE HERE ***"

    def getDistribution(self, state):

        ActionScore = []
        numAgent = 3
        depth = 2

        def rmStop(List):
            return [x for x in List if x != 'Stop']

        def evaluationFunction(state, sindex):
            dis1 = manhattanDistance(state.getPacmanPosition(),state.getGhostPosition(1))
            dis2 = manhattanDistance(state.getPacmanPosition(),state.getGhostPosition(2))

            if sindex == 1:
                dis = dis1
            else:
                dis = dis2

            if manhattanDistance(state.getGhostPosition(1), state.getGhostPosition(2)) <= 2:
                return 0

            if dis2+dis1 > dis1*dis1:
                return 1000 - dis2+dis1 - dis
            else:
                return 1000 - dis1*dis1 - dis

        def get_index(k):
            if k == 1:
                return 2
            if k == 2:
                return 1

        def miniMax(s, iterCount, sindex):

            if iterCount >= depth * numAgent or s.isWin () or s.isLose ():
                return evaluationFunction(s,sindex)

            if iterCount % numAgent == 2:  # Pacman min
                result = 1e10
                for a in rmStop(s.getLegalActions(0)):
                    sdot = s.generateSuccessor(0, a)
                    result = min(result, miniMax (sdot, iterCount + 1, sindex))
                return result

            elif iterCount % numAgent == 0:
                result = -1e10
                for a in rmStop (s.getLegalActions(sindex)):
                    sdot = s.generateSuccessor(sindex, a)
                    result = max(result, miniMax (sdot, iterCount + 1, sindex))
                    if iterCount == 0:
                        ActionScore.append (result)
                return result

            elif iterCount % numAgent == 1:
                result = -1e10
                for a in rmStop(s.getLegalActions(get_index(sindex))):
                    sdot = s.generateSuccessor(get_index(sindex), a)
                    result = max(result, miniMax(sdot, iterCount + 1, sindex))
                return result

        miniMax(state, 0, self.index)
        print ActionScore
        print state.getLegalActions (self.index)
        #while  len(state.getLegalActions(self.index))
        dre = state.getLegalActions(self.index)[ActionScore.index(max(ActionScore))]
        print dre
        dist = util.Counter ()
        for a in state.getLegalActions(self.index):
            dist[a] = 0
        dist[dre] = 1
        dist.normalize()
        return dist

def betterEvaluationFunctionGhost(currentGameState):
    """
        Ghost evaluation function
    """



# Abbreviation
ghostEval = betterEvaluationFunctionGhost

