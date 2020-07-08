#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the LunarLockout  domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

#import os for time functions
from search import * #for search engines
from lunarlockout import LunarLockoutState, Direction, lockout_goal_state #for LunarLockout specific classes and problems
import time

#LunarLockout HEURISTICS
def heur_trivial(state):
    '''trivial admissible LunarLockout heuristic'''
    '''INPUT: a LunarLockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    return 0

def heur_L_distance(state):
    #OPTIONAL
    '''L distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #Write a heuristic function that uses mahnattan distance to estimate distance between the current state and the goal.
    #Your function should return a sum of the L distances between each xanadu and the escape hatch.
    esc = int(state.width / 2) + 1
    num_moves = 0

    for x in range(0,len(state.xanadus)):
      if type(state.xanadus[x]) is tuple:
        xan = state.xanadus[x]
      else:
        xan = state.xanadus
      if xan[0] != esc:
        num_moves += 1
      if xan[1] != esc:
        num_moves += 1
      if xan == state.xanadus:
        break
    return num_moves


def heur_alternate(state):
#IMPLEMENT
  '''For each xanadus in the LunarLockout state, calculate the minimum Manhattan distance achieved by moving it once.
  Return the summation of these values.
  The idea is too make moves that will overall decreases the collective distance of all the xanadus in the given state
  to the escape hatch.'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  #Your function should return a numeric value for the estimate of the distance to the goal.

  goal = int(state.width  - 1)/ 2 # escape hatch location
  # check if there's only 1 xanadus or 1 robot in the given state
  single_xan = False
  single_rob = False
  xan_num_moves = 0 # used for collective Manhattan distance of the xanadus(es) to the escape hatch
  for x in range(0, len(state.xanadus)):
    updated = [0, 0]  # update the current xanadus's location after one move
    if type(state.xanadus[x]) is tuple: # more than 1 xanadus
      x_state = [state.xanadus[x][0], state.xanadus[x][1]]
      i = 0
      num_moves = abs(x_state[0] - goal) + abs(x_state[1] - goal) # Mahattan distance of current xanadus to escape hatch
      # iterate through all other xanduses in the state to find min Mahattan distance to escape hatch
      while i < len(state.xanadus):
        if i == x:
          i += 1
          continue
        other_xan = state.xanadus[i]
        # if there's another xanadus on the same x-, or y-coordinate towards the direction of the escape hatch,
        # then make the move and update the variable, update.
        if other_xan[1] == x_state[1]:
          if goal < x_state[0] and other_xan[0] < x_state[0]:
            updated[0] = other_xan[0]  + 1
          elif goal > x_state[0] and other_xan[0] > x_state[0]:
            updated[0] = other_xan[0] - 1
          # updated[1] = x_state[1]
        elif other_xan[0] == x_state[0]:
          if x_state[1] < goal and other_xan[1] > x_state[1]:
            updated[1] = other_xan[1] + 1
          elif x_state[1] > goal and other_xan[1] < x_state[1]:
            updated[1] = other_xan[1] - 1
          # updated[0] = x_state[0]
        # calculate the Manhattan distance from this new location
        updated_moves = abs(goal - updated[0]) +  abs(goal - updated[1])
        if updated_moves < num_moves:
          num_moves = updated_moves
        updated = [0, 0]
        i += 1
    else:
      x_state = [state.xanadus[0], state.xanadus[1]]
      single_xan = True
      num_moves = abs(x_state[0] - goal) + abs(x_state[1] - goal)
    #iterate through all robots and updated to find min Manhattan distance to escape hatch
    for r in range(0, len(state.robots)):
      if type(state.robots[r]) is tuple:
        r_state = [state.robots[r][0], state.robots[r][1]]
      else:
        r_state = [state.robots[0], state.robots[1]]
        single_rob = True
      if r_state[1] == x_state[1]:
        if goal < x_state[0] and r_state[0] < x_state[0]:
          updated[0] = r_state[0] + 1
        elif r_state[0] > x_state[0] and goal > x_state[0]:
          updated[0] = r_state[0] - 1
      elif r_state[0] == x_state[0]:
        if x_state[1] < goal and r_state[1] > x_state[1]:
          updated[1] = r_state[1] + 1
        elif x_state[1] > goal and r_state[1] < x_state[1]:
          updated[1] = r_state[1] - 1
      updated_moves = abs(goal - updated[0]) + abs(goal - updated[1])
      if updated_moves< num_moves:
        num_moves = updated_moves
      if single_rob is True:
        break
      updated = [0,0]
    if single_xan is True:
      return num_moves
    xan_num_moves += num_moves
  return xan_num_moves

def fval_function(sN, weight):
#IMPLEMENT
  """
  Provide a custom formula for f-value computation for Anytime Weighted A star.
  Returns the fval of the state contained in the sNode.

  @param sNode sN: A search node (containing a LunarLockoutState)
  @param float weight: Weight given by Anytime Weighted A star
  @rtype: float
  """
  #Many searches will explore nodes (or states) that are ordered by their f-value.
  #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
  #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
  #The function must return a numeric f-value.
  #The value will determine your state's position on the Frontier list during a 'custom' search.
  #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
  fval = sN.gval + weight * heur_alternate(sN.state)
  return fval

def anytime_weighted_astar(initial_state, heur_fn, weight=4., timebound = 2):
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  # if goal is never found, variable goal_state is never updated
  # if goal is found, goal_state is updated everytime weight is iteratively reduced
  # in this case goal_state is the best solution so far
  goal_state = False
  time_left = timebound
  start = time.time()
  while weight > 0 and time_left > 0:
    state = SearchEngine("custom")
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    state.init_search(initial_state, lockout_goal_state, heur_fn, wrapped_fval_function)
    search_return = state.search(time_left)
    finished = time.time()
    if search_return is not False:
      goal_state = search_return
    time_left -= finished - start
    weight -= 1

  return goal_state


def anytime_gbfs(initial_state, heur_fn, timebound = 1):
  # OPTIONAL
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  return 0

PROBLEMS = (
  #5x5 boards: all are solveable
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 1))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 2))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 3))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 1))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 2))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 3))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 4))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 0))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 1))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (0, 2),(0,4),(2,0),(4,0)),((4, 4))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 0))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 1))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 3))),
  #7x7 BOARDS: all are solveable
  LunarLockoutState("START", 0, None, 7, ((4, 2), (1, 3), (6,3), (5,4)), ((6, 2))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (4, 2), (2,6)), ((4, 6))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (3, 1), (4, 1), (2,6), (4,6)), ((2, 0),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((1, 2), (0 ,2), (2 ,3), (4, 4), (2, 5)), ((2, 4),(3, 1),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 2), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 1), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (0 ,2), (1 ,2), (6, 4), (2, 5)), ((2, 0),(3, 0),(4, 0))),
  )

if __name__ == "__main__":

  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 7 #1 second time limit for each problem
  # print("*************************************")
  # print("Running A-star")
  #
  # for i in range(len(PROBLEMS)): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.
  #
  #   print("*************************************")
  #   print("PROBLEM {}".format(i))
  #
  #   s0 = PROBLEMS[i] #Problems will get harder as i gets bigger
  #
  #   print("*******RUNNING A STAR*******")
  #   se = SearchEngine('astar', 'full')
  #   se.init_search(s0, lockout_goal_state, heur_alternate)
  #   final = se.search(timebound)
  #
  #   if final:
  #     final.print_path()
  #     solved += 1
  #   else:
  #     unsolved.append(i)
  #   counter += 1
  #
  # if counter > 0:
  #   percent = (solved/counter)*100
  #
  # print("*************************************")
  # print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  # print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  # print("*************************************")

  solved = 0; unsolved = []; counter = 0; percent = 0;
  print("Running Anytime Weighted A-star")

  for i in range(len(PROBLEMS)):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]
    weight = 4
    final = anytime_weighted_astar(s0, heur_alternate, weight, timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  # solved = 0; unsolved = []; counter = 0; percent = 0;
  # print("Running Anytime GBFS")
  #
  # for i in range(len(PROBLEMS)):
  #   print("*************************************")
  #   print("PROBLEM {}".format(i))
  #
  #   s0 = PROBLEMS[i]
  #   final = anytime_gbfs(s0, heur_L_distance, timebound)
  #
  #   if final:
  #     final.print_path()
  #     solved += 1
  #   else:
  #     unsolved.append(i)
  #   counter += 1
  #
  # if counter > 0:
  #   percent = (solved/counter)*100
  #
  # print("*************************************")
  # print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  # print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  # print("*************************************")
  #
  #
  #
  #
  #
