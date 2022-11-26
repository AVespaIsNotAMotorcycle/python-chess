from opponents.opponent import Opponent
from opponents.boardstate_heuristic import OppBoardStateHeuristic

def create_opponent(team, name = 'random'):
  if name == 'boardstate_heuristic':
    # print('initializing "boardstate_heuristic" opponent')
    return OppBoardStateHeuristic(team)
  # print('initializing "random" opponent')
  return Opponent(team)
