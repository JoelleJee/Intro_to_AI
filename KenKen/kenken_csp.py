'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. kenken_csp_model (worth 20/100 marks)
    - A model built using your choice of (1) binary binary not-equal, or (2)
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools


def verify_add(vals, target_val):
    '''
    Returns True if the values in vals adds up to target_val
    '''
    sum = 0
    for val in vals:
        sum += val
    return sum == target_val


def verify_sub(vals, target_val):
    '''
    Returns True if the values in vals subtract to target_val
    '''
    for p in itertools.permutations(vals):
        sub = p[0]
        i = 1
        while (i < len(vals)):
            sub -= p[i]
            i += 1
        if sub == target_val:
            return True
    return False


def verify_div(vals, target_val):
    '''
    Returns True if the values vals divide to target_val
    '''
    for p in itertools.permutations(vals):
        div = p[0]
        i = 1
        while (i < len(vals)):
            div //= p[i]
            i += 1
        if div == target_val:
            return True
    return False


def verify_mult(vals, target_val):
    '''
    Returns True if the values in vals multiply to target_val
    '''
    prod = 1
    for val in vals:
        prod *= val
    return prod == target_val


def init_vars(domain):
    '''
    Helper function for binary_ne_grid and nary_ad_grid:
    Returns the game board with all the variables for a KenKen board with given the domain.
    '''
    size = len(domain)
    board = []

    # initialize variables and add to board
    for row in range(1, size + 1):
        row_vars = []
        for col in range(1, size + 1):
            row_vars.append(Variable('V{0}{1}'.format(row, col), domain))
        board.append(row_vars)

    return board

def get_c_name(vars):
    '''
    Helper function for nary_ad_grid:
    Generates the name of a constraint given its scope in list vars
    '''

    name = "C("
    for i in range(0, len(vars)):
        if type(vars[i]) is str:
            name += "V" + vars[i]
        if type(vars[i]) is int:
            name += "V" + str(vars[i])
        else:
            name += vars[i].name
        if i < len(vars) - 1:
            name += ","
    name += ")"

    return name


def binary_ne_grid(kenken_grid):
    '''
    A model of a KenKen grid (without cage constraints) built using only
    binary-not-equal constraints for both the row and column constraints.
    '''

    size = kenken_grid[0][0]  #board size

    #Starting domain; used to initialize variables
    domain = []
    for i in range(1, size + 1):
        domain.append(i)

    #Initialize Variables and store them in an size*size board
    board = init_vars(domain)

    #Initialize Contraints and store them in list constraints
    constraints = []
    #Store row constraints to constraints
    for row in board:
        #initialize row constraints
        for pair in itertools.combinations(row, 2):
            c = Constraint("C({0},{1})".format(pair[0].name, pair[1].name),
                           [pair[0], pair[1]])
            #pairs that satisfy the constraints:
            sat_pairs = []
            for sat_pair in itertools.permutations(domain, 2):
                sat_pairs.append(sat_pair)
            c.add_satisfying_tuples(sat_pairs)
            constraints.append(c)

    #Store column constraints to constraints
    for col in range(len(domain)):
        column = []
        for row in range(len(domain)):
            column.append(board[row][col])
        for pair in itertools.combinations(column, 2):
            #initialize column constraints
            c = Constraint("C({0},{1})".format(pair[0].name, pair[1].name),
                           [pair[0], pair[1]])
            #pairs that satisfy the constraints:
            sat_pairs = []
            for sat_pair in itertools.permutations(domain, 2):
                sat_pairs.append(sat_pair)
            c.add_satisfying_tuples(sat_pairs)
            constraints.append(c)

    #Initialize CSP
    csp = CSP("{0}-BinaryKenKen".format(size))
    #add every variable to csp
    for row in board:
        for var in row:
            csp.add_var(var)
    #add every onstraint to csp
    for c in constraints:
        csp.add_constraint(c)

    return csp, board


def nary_ad_grid(kenken_grid):
    '''
    A model of a KenKen grid (without cage constraints) built using only
    n-ary all-different constraints for both the row and column constraints.
    '''
    size = kenken_grid[0][0] #board size

    #Starting domain; used to initialize variables
    domain = []
    for i in range(1, size + 1):
        domain.append(i)
    # init variables
    board = init_vars(domain)


    # Initialize Contraints and store them in list constraints
    constraints = []
    # Store row constraints to constraints
    for row in board:
        #initialize constraint c with with all variables in row row
        c_name = get_c_name(row)
        c = Constraint(c_name, row)
        #combinations of values that satisfy the constraints
        sat_combs = []
        for diff_comb in itertools.permutations(domain, size):
            sat_combs.append(diff_comb)
        c.add_satisfying_tuples(sat_combs)
        constraints.append(c)

    # add column constraints
    # build columns
    for col in range(len(domain)):  # column num from 0 to n-1
        column = []
        for row in range(len(domain)):  # num of rows
            column.append(board[row][col])
        #initialize constraint c with scope of all variables column col
        c_name = get_c_name(column)
        c = Constraint(c_name, column)
        #combinations of values that satisfy the constraints
        sat_combs = []
        for diff_comb in itertools.permutations(domain, size):
            sat_combs.append(diff_comb)
        c.add_satisfying_tuples(sat_combs)
        constraints.append(c)

    #Initialize CSP
    csp = CSP("{0}-aryKenKen".format(size))
    #add every variable to csp
    for row in board:
        for var in row:
            csp.add_var(var)
    #add all the n-ary row and column constraints to csp
    for c in constraints:
        csp.add_constraint(c)

    return csp, board


def kenken_csp_model(kenken_grid):
    '''
    A model built using n-ary all-different constraints for the grid and
    KenKen cage constraints.
    '''

    #Get the board the n-ary csp's using nary_ad_grid(kenken_grid)
    n_ary = nary_ad_grid(kenken_grid)
    n_ary_csp = n_ary[0]
    board = n_ary[1]

    size = kenken_grid[0][0]  # board size

    #Starting domain; used to initialize variables
    domain = []
    for i in range(1, size + 1):
        domain.append(i)

    #Store all the cage constraints in constarints
    constraints = []

    #Initizlie cage constraints
    for cage in kenken_grid[1:len(kenken_grid)]:
        c_scope = []
        if len(cage) == 2:
            row = (cage[0] // 10)
            col = (cage[0] % 10)
            c_scope.append(board[row - 1][col - 1])
            target_value = cage[1]

            c = Constraint("Cage: " + "C(V{0}{1})".format(row, col), c_scope)
            c.add_satisfying_tuples([(target_value)])
            constraints.append(c)
            continue  #move onto the next cage

        #if len(cage) > 2
        for cell in range(0, len(cage) - 2):
            row = (cage[cell] // 10)
            col = (cage[cell] % 10)
            c_scope.append(board[row - 1][col - 1])
        op = cage[-1]
        target_value = cage[-2]

        c_name = get_c_name(c_scope)
        c = Constraint("Cage: " + c_name, c_scope)

        #Verify if each combination satisfies the constraint and add to sat_combs
        sat_combs = []
        for t in itertools.product(domain, repeat=len(c_scope)):
            if op == 0:  #addition
                if verify_add(t, target_value):
                    sat_combs.append(t)
            elif op == 1:  #subtraction
                if verify_sub(t, target_value):
                    sat_combs.append(t)
            elif op == 2:  #division
                if verify_div(t, target_value):
                    sat_combs.append(t)
            elif op == 3:  #multiplication
                if verify_mult(t, target_value):
                    sat_combs.append(t)
        c.add_satisfying_tuples(sat_combs)
        constraints.append(c)


    #Initialize CSP
    csp = CSP("{0}-KenKen".format(size))

    #add all variables to csp
    for row in board:
        for var in row:
            csp.add_var(var)

    #add cage constraints to csp
    for c in constraints:
        csp.add_constraint(c)
    #add row and column constraints to csp
    for c in n_ary_csp.get_all_cons():
        csp.add_constraint(c)

    return csp, board
