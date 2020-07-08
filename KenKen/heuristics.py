#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''

def ord_mrv(csp):
    '''
    A variable ordering heuristic that chooses the next variable to be assigned according to the
    Minimum-Remaining-Value (MRV) heuristic.
    Returns the variable with the most constrained current domain (i.e., the variable with the fewest legal values).
    '''

    min_var = None
    min_dom_size = None
    vars = csp.get_all_unasgn_vars()

    for x in vars:
        if min_var is None or x.cur_domain_size() < min_dom_size:
            min_var = x
            min_dom_size = x.cur_domain_size()

    return min_var



def val_lcv(csp,var):
    '''
    A value heuristic that, given a variable, chooses the value to be assigned according to the
    Least-Constraining-Value (LCV) heuristic.
    Returns a list of values that's ordered by the value that rules out the fewest values in the remaining variables
    (i.e., the variable that gives the most flexibility later on) to the value that rules out the most.
    '''

    ordered_vals = []
    val_to_ruledout = {}
    before = 0

    for c in csp.get_cons_with_var(var):
        if c.get_n_unasgn() > 1:
            for x in c.get_unasgn_vars():
                if x != var:
                    before += x.cur_domain_size()

    for d in var.cur_domain():
        var.assign(d)
        after = 0
        for c in csp.get_cons_with_var(var):
            if c.get_n_unasgn() > 0:
                for x in c.get_unasgn_vars():
                    after += x.cur_domain_size()

        var.unassign()

        val_to_ruledout[d] = before - after

    val_to_ruledout = sorted(val_to_ruledout.items())
    for (val, ruleout) in val_to_ruledout:
        ordered_vals.append(val)

    return ordered_vals
