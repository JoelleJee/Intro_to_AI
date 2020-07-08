# Intro_to_AI
Coursework for CSC384: Introduction to Artificial Intelligence

## LunarLockout.py
Implemented a heuristic search that make moves that will overall decrease the collective distance of all the xanadus in the given state.
* heuristic function returns the summation of the minimum Manhattan distances to the escape hatch achieved by moving the each xanadus once.

## PacmanAgents.py
Implemented search methods for different agents in the game of Pacman:

### Reflex agent
A reflex agent chooses an action at each choice point by examining its alternatives via a state evaluation function.
* implemented the evaluation function that grades each game state's through various variables (number of remaining food, Pacman's position, and number of moves that each ghost will remain immobile) 

### Minimax and AlphaBeta agents
A minimax and a alphabeta agent uses a minimax search with and without pruning, respectively, to win the game. 
* implemented the minimax search tree and alpha-beta pruning

### Expectimax 
A expectimax agent doesn't assume optimal moves of the adversary. It still uses the minmax search, but instead at min nodes, it calculates the average of the successor game states. 

### Better Evaluation Function
Implemented a evaluation function for grading game states using a linear combination of features/variables.

## KenKen
### prop_FC
A propagator function that propagates according to the forward checking algorithm that check constraints that have exactly one uninstantiated variable in their scope, and prune appropriately. 

### prop_GAC 
A propagator function that propagates according to the generalized arc consistence algorithm.

### ord_mrv 
A variable ordering heuristic that chooses the next variable to be assigned according to the Minimum- Remaining-Value (MRV) heuristic. ord mrv returns the variable with the most constrained current domain (i.e., the variable with the fewest legal values).

### val_lcv
A value heuristic that, given a variable, chooses the value to be assigned according to the Least- Constraining-Value (LCV) heuristic. val lcv returns a list of values. The list is ordered by the value that rules out the fewest values in the remaining variables (i.e., the variable that gives the most flexibility later on) to the value that rules out the most.

### binary_ne_grid
A model of a KenKen grid (without cage constraints) built using only binary not-equal constraints for both the row and column constraints.

### nary_ad_grid
A model of a KenKen grid (without cage constraints) built using only n-ary all-different constraints for both the row and column constraints.

### kenken_csp_model
A model built using n-ary all-different constraints for the grid together with KenKen cage constraints. 
