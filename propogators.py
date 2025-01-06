# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#

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
      if not c.check_tuple(vals):
        return False, []
  return True, []


'''
@return bool a, list b
a: whether or not to continue or back track
b: list of pruned (Var, Value)
'''


def prop_FC(csp, newVar=None):
  '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''

  # we look for unary constraints of the csp (constraints whose scope contains only one variable)
  # and we forward_check these constraints.
  vals = []
  # Get all constraints if new variable is None, otherwise get all related constraints
  cons = csp.get_all_cons() if not newVar else csp.get_cons_with_var(newVar)

  for c in cons:
    # Check for unary constraints
    if c.get_n_unasgn() == 1:
      unasgn_var = c.get_unasgn_vars()[0]

      for value in unasgn_var.cur_domain():
        asgn = [(unasgn_var, value)]

        # Check if the variable and value pair fail the constraints,
        # Prune if it does fail
        if not c.check_tuple(asgn):
          unasgn_var.prune_value(value)

          vals.append((unasgn_var, value))
          # If it has no valid path forward, return false and pruned
          if unasgn_var.cur_domain_size() == 0:
            return False, vals
  return True, vals


def prop_GAC(csp, newVar=None):
  '''Do GAC propagation. If newVar is None we do initial GAC enforce
     processing all constraints. Otherwise we do GAC enforce with
     constraints containing newVar on GAC Queue'''
  #IMPLEMENT
  cons = csp.get_all_cons() if not newVar else csp.get_cons_with_var(newVar)
  # Initialize GAC Queue
  queue = []
  pruned = []
  # Fill queue with all the hyper arcs
  for c in cons:
    for i in range(c.get_n_unasgn()):
      allVars = c.get_unasgn_vars()
      head = allVars[i]
      del(allVars[i])
      tail = allVars
      queue.append((c, head, tail))

  while queue is not None:
  #  remove first element from queue
    arc = queue.pop(0)
    c = arc[0]
    x_i = arc[1]
    x = arc[2]
  # Prune inconsistent values
    for v in x_i.cur_domain():
      for x_vars in x:
        for y in x_vars.cur_domain():
          if not c.check_tuple((v, y)):
            x_i.prune_value(v)
            pruned.append((x_i, v))
            # for all neighbours of x_i, x_k
            cons = csp.get_cons_with_var(x_i)
            for c in cons:
              for i in range(c.get_n_unasgn()):
                allVars = c.get_unasgn_vars()
                x_k = allVars[i]
                del(allVars[i])
                tail = allVars
                queue.append((c, x_k, tail))

