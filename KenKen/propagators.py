#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''
    Forward checking: check constraints with only one uninstantiated variable.
    '''

    pruned_vals = []

    if newVar is None:
        cons = csp.get_all_cons()
    else:
        cons = csp.get_cons_with_var(newVar)

    for c in cons:
        #if there is only 1 unassigned variable in c do FC
        if c.get_n_unasgn() == 1:
            x = c.get_unasgn_vars()[0]
            for d in x.cur_domain():
                x.assign(d)
                vars = c.get_scope()
                vals = []
                for var in vars:
                    vals.append(var.get_assigned_value())
                if not c.check(vals):
                    if (x, d) not in pruned_vals:
                        x.prune_value(d)
                        pruned_vals.append((x, d))
                #unassign x and repeat the process
                x.unassign()
                #stop when DWO reached - no valid assignment of values to satisfy the constraints
                if x.cur_domain_size() == 0:
                    return (False, pruned_vals)

    return (True, pruned_vals)


def prop_GAC(csp, newVar=None):
    '''
    GAC propagation. If newVar is None we do initial GAC enforce processing all constraints.
    Otherwise we do GAC enforce with onstraints containing newVar on GAC Queue
    '''

    pruned_vals = []

    if newVar is None:
        cons = csp.get_all_cons()
    else:
        cons = csp.get_cons_with_var(newVar)

    for c in cons:
        for x in c.get_scope():
            for d in x.cur_domain():
                #first check if c has support when x = d
                if not c.has_support(x, d):
                    if (x, d) not in pruned_vals:
                        x.prune_value(d)
                        pruned_vals.append((x, d))
                #DWO reachced - stop
                if x.cur_domain_size() == 0:
                    return (False, pruned_vals)

    return (True, pruned_vals)

