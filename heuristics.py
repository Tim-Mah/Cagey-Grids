# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    # IMPLEMENT
    all_vars = csp.get_all_vars()
    degree = 0
    r_var = ''
    for var in all_vars:
        #get contraints that have var
        l_con = csp.get_cons_with_var(var)
        l_con_2 = []
  
        #remove constraints that don't have other unassigned variables
        for con in l_con:
            if con.get_n_unasgn() != 0:
                l_con_2.append(con)
  
        #find variable with the largest degree
        if len(l_con_2) > degree:
            degree = len(l_con_2)
            r_var = var
    return r_var

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    all_vars = csp.get_all_vars()
    mrv = 100
    r_var = ''
    for var in all_vars:
      #get the current domain for the variable
      c_domain = var.cur_domain_size()
  
      #find the variable with the lowest domain that is not 0
      if ((c_domain < mrv) and (c_domain != 0)):
        mrv = c_domain
        r_var = var
    
    return r_var
  