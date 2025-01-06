# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools
from itertools import permutations

def binary_ne_grid(cagey_grid):
    ##IMPLEMENT
    #Get size of grid
    size = cagey_grid[0]
    i = 0
    dom = []
    for i in range(size):
        dom.append(i+1)

    #Get variables
    vars = []
    for x in dom:
        for y in dom: 
            vars.append(Variable("Cell({},{})".format(x,y), dom))

    #Get row constraints
    cons = []
    for x in dom:
        scope_row = []
        for i in range(len(dom)):
            if (vars[((x-1)*len(dom)) + (i)] not in scope_row):
                scope_row.append(vars[((x-1)*len(dom)) + (i)])
        con = Constraint("Row{}".format(x),scope_row)

        #Set up binary NE constraints
        sat_tuples = []
        comb = [[o, x] for (o, x) in itertools.product(dom, dom) if o != x]
        for i in comb:
            t= tuple(i)
            sat_tuples.append(t)
        # left_idx = 0
        # [[o, x] for (o, x) in itertools.product(dom, repeat=2) if o != x]
        # for var in scope_row:
        # for var2 in scope_row[left_idx:]:
        #     if var != var2:
        #         t = (var, var2)
        #         sat_tuples.append(t)
        # left_idx += 1

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)


    #Get column constraints
    for y in dom:
      scope_col = []
      for i in range(len(dom)):
          if (vars[((x-1)*len(dom)) + (y-1)] not in scope_col):
            scope_col.append(vars[((y-1)*len(dom)) + (i-1)])
      con = Constraint("Row{}".format(y),scope_col)

      #Set up binary NE constraints
      comb = [[o, x] for (o, x) in itertools.product(dom, dom) if o != x]
      for i in comb:
        t= tuple(i)
        sat_tuples.append(t)
    #   left_idx = 0
    #   for var in scope_col:
    #     for var2 in scope_col[left_idx:]:
    #         if var.get_assigned_value() != var2.get_assigned_value():
    #             scope_col.append(vars[((y-1)*len(dom)) + (x-1)])
    #             sat_tuples.append(t)
    #     left_idx += 1

      con.add_satisfying_tuples(sat_tuples)
      cons.append(con)

    #Create CSP
    csp = CSP("Binary-NE-Grid-Size-{}".format(size), vars)
    for c in cons:
        csp.add_constraint(c)
    return csp, vars


def nary_ad_grid(cagey_grid):
    ## IMPLEMENT
    #Get size of grid
    size = cagey_grid[0]
    i = 0
    dom = []
    for i in range(size):
        dom.append(i+1)

    #Get variables
    vars = []
    for x in dom:
        for y in dom: 
            vars.append(Variable("Cell({},{})".format(x,y), dom))

    #Get row constraints
    cons = []
    for x in dom:
        scope_row = []
        for i in range(len(dom)):
            if (vars[((x-1)*len(dom)) + (i)] not in scope_row):
                scope_row.append(vars[((x-1)*len(dom)) + (i)])
        con = Constraint("Row{}".format(x),scope_row)

        #Set up n-ary AD constraints

        sat_tuples = []
        comb = list(permutations(range(1, 1+len(dom))))
        for i in comb:
          t= tuple(i)
          sat_tuples.append(t)

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)



    #Get column constraints
    for y in dom:
      scope_col = []
      for i in range(len(dom)):
          if (vars[((x-1)*len(dom)) + (y-1)] not in scope_col):
            scope_col.append(vars[((y-1)*len(dom)) + (i-1)])
      con = Constraint("Row{}".format(y),scope_col)

      #Set up n-ary AD constraints
      sat_tuples = []
      comb = list(permutations(range(1, 1+len(dom))))
      for i in comb:
        t= tuple(i)
        sat_tuples.append(t)

      con.add_satisfying_tuples(sat_tuples)
      cons.append(con)

    #Create CSP
    csp = CSP("Binary-NE-Grid-Size-{}".format(size), vars)
    for c in cons:
        csp.add_constraint(c)
    return csp, vars

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass
