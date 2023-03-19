import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import random

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you assign them
        Return: a tuple of a dictionary and a bool. The dictionary contains all MODIFIED variables, mapped to their MODIFIED domain.
                The bool is true if assignment is consistent, false otherwise.
    """
    def forwardChecking ( self ):
        # modified = {}

        # assignedVars = []
        # for c in self.network.constraints:
        #     for v in c.vars:
        #         if v.isAssigned():
        #             assignedVars.append(v)
        # while len(assignedVars) != 0:
        #     av = assignedVars.pop(0)
        #     for neighbor in self.network.getNeighborsOfVariable(av):
        #         if neighbor.size() == 0:
        #             return (modified, False)
        #         if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
        #             if neighbor.size() == 1:
        #                 return (modified, False)
        #             self.trail.push(neighbor)
        #             neighbor.removeValueFromDomain(av.getAssignment())
        #             modified[neighbor] = neighbor.getDomain()
        #             if neighbor.domain.size() == 1:
        #                 neighbor.assignValue(neighbor.domain.values[0])
        #                 assignedVars.append(neighbor)

        # return (modified, True)
    
        modified = {}
        
        for v in self.network.variables:
            #for v in c.vars:
            if v.isAssigned():
                for neighbor in self.network.getNeighborsOfVariable(v):
                    if neighbor.size() == 0:
                        return (modified, False)
                    if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(v.getAssignment()):
                        self.trail.push(neighbor)  
                        neighbor.removeValueFromDomain(v.getAssignment())
                        modified[neighbor] = neighbor.getDomain()  

        return (modified,True)
    
        # modified = {}
        
        # assignedVars = []
        # for c in self.network.constraints:
        #     for v in c.vars:
        #         if v.isAssigned():
        #             assignedVars.append(v)
        # for assign in assignedVars:
        #     for neighbor in self.network.getNeighborsOfVariable(assign):
        #         if neighbor.size() == 0:
        #             return (modified, False)
        #         if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(assign.getAssignment()):

        #             self.trail.push(neighbor)  
        #             neighbor.removeValueFromDomain(assign.getAssignment())
        #             modified[neighbor] = neighbor.getDomain()   

        # return (modified,True)

    # =================================================================
	# Arc Consistency
	# =================================================================
    def arcConsistency( self ):
        assignedVars = []
        for v in self.network.variables:
            # for v in c.vars:
            if v.isAssigned():
                assignedVars.append(v)
        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.domain.size() == 1:
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)

    
    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you assign them
        Return: a pair of a dictionary and a bool. The dictionary contains all variables 
		        that were ASSIGNED during the whole NorvigCheck propagation, and mapped to the values that they were assigned.
                The bool is true if assignment is consistent, false otherwise.
    """
    def norvigCheck ( self ):
        #ask about modified dictionary, whether to use the one from FC or a new one
        #do we check consistency

        modified_dict, consistency = self.forwardChecking()

        counter_array = []
        assignedVars = []

        N = self.gameboard.N

        for i in range(N):
            counter_array.append(0)

        for c in self.network.constraints:
            for i in range(N):
                counter_array[i] = 0

            for l in range(N):
                for value in c.vars[l].domain.values:
                    counter_array[value - 1] += 1
            
            for j in range(N):
                if counter_array[j] == 0:
                    return (modified_dict, False)
                if counter_array[j] == 1:
                    for v in c.vars:
                        if v.size() == 0:
                            return (modified_dict, False)
                        if v.isChangeable and not v.isAssigned() and v.getDomain().contains(j+1):
                            self.trail.push(v)
                            v.assignValue(j+1)
                            assignedVars.append(v)
                            # print("Row: {}, Col: {}, Value: {}, Depth: {}".format(v.row, v.col, j+1, v))
                            modified_dict[v] = j+1
                        
        # self.arcConsistency()


        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.domain.size() == 1:
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)

        return (modified_dict, True)

    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
        return self.norvigCheck()[1]

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        min_remain = None
        smallest_domain = None
        
        for v in self.network.variables:
            # for v in c.vars:
                if not v.isAssigned():
                    domain_size = v.size()
                    if not smallest_domain:
                        min_remain = domain_size
                        smallest_domain = v

                    else:
                        if domain_size < min_remain:
                            smallest_domain = v
                            min_remain = domain_size
        
        return smallest_domain
    
        # unassigned_vars = []
        # for c in self.network.constraints:
        #     for v in c.vars:
        #         if not v.isAssigned():
        #             unassigned_vars.append(v)

        # if len(unassigned_vars) == 0:
        #     return None
        
        # min_remain = unassigned_vars[0].domain.size()
        # smallest_domain = unassigned_vars[0]

        # for i in range(1, len(unassigned_vars)):
        #     if min_remain > unassigned_vars[i].domain.size():
        #         min_remain = unassigned_vars[i].domain.size()
        #         smallest_domain = unassigned_vars[i]
        
        # return smallest_domain

    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with the smallest domain and affecting the  most unassigned neighbors.
                If there are multiple variables that have the same smallest domain with the same number of unassigned neighbors, add them to the list of Variables.
                If there is only one variable, return the list of size 1 containing that variable.
    """
    def MRVwithTieBreaker ( self ):
        min_remain = None
        smallest_domain_variables = []
        
        for v in self.network.variables:
            # for v in c.vars:
            if not v.isAssigned():
                domain_size = v.size()

                if not min_remain:
                    min_remain = domain_size
                    smallest_domain_variables.append(v)

                else:
                    if domain_size < min_remain:
                        smallest_domain_variables = [v]
                        min_remain = domain_size
                    elif domain_size == min_remain:
                        smallest_domain_variables.append(v)

        if len(smallest_domain_variables) == 0:
            return [None]
        
        max_unassigned_neighbors = 0
        new_small_domain_vars = []

        for small_dom_var in smallest_domain_variables:
            unassign_count = 0
            for neighbor in self.network.getNeighborsOfVariable(small_dom_var):
                if neighbor.isChangeable and not neighbor.isAssigned():
                    unassign_count += 1

            if unassign_count > max_unassigned_neighbors:
                max_unassigned_neighbors = unassign_count
                new_small_domain_vars = [small_dom_var]

            elif unassign_count == max_unassigned_neighbors:
                new_small_domain_vars.append(small_dom_var)
        
        return new_small_domain_vars
        
        # unassigned_vars = []
        # for c in self.network.constraints:
        #     for v in c.vars:
        #         if not v.isAssigned():
        #             unassigned_vars.append(v)
        
        # if(len(unassigned_vars) == 0):
        #     return None
            
        # min_remain = unassigned_vars[0].domain.size()

        # smallest_domain_variables = [unassigned_vars[0]]

        # for i in range(1, len(unassigned_vars)):
        #     if min_remain > unassigned_vars[i].domain.size():
        #         smallest_domain_variables = [unassigned_vars[i]]
        #         min_remain = unassigned_vars[i].domain.size()

        #     elif min_remain == unassigned_vars[i].domain.size():
        #         smallest_domain_variables.append(unassigned_vars[i]) 


        # max_unassigned_neighbors = 0
        # new_small_domain_vars = []

        # for small_dom_var in smallest_domain_variables:
        #     unassign_count = 0
        #     for neighbor in self.network.getNeighborsOfVariable(small_dom_var):
        #         if neighbor.isChangeable and not neighbor.isAssigned():
        #             unassign_count += 1

        #     if unassign_count > max_unassigned_neighbors:
        #         max_unassigned_neighbors = unassign_count
        #         new_small_domain_vars = [small_dom_var]

        #     elif unassign_count == max_unassigned_neighbors:
        #         new_small_domain_vars.append(small_dom_var)
        
        # return new_small_domain_vars

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        # return None
        return self.getMRV()

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):

        sorted_domain_dict = {}

        for domain in v.getDomain().values:
            domain_count = 0
            for neighbor in self.network.getNeighborsOfVariable(v):
                if neighbor.getDomain().contains(domain):
                    domain_count += 1

            sorted_domain_dict[domain] = domain_count

        sorted_domain = [t for t, v in sorted(sorted_domain_dict.items(), key=lambda k: k[1])]

        return sorted_domain
    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        # return None
        return self.getValuesLCVOrder(v)

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self, time_left=600):
        if time_left <= 60:
            return -1

        start_time = time.time()
        if self.hassolution:
            return 0

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            # Success
            self.hassolution = True
            return 0

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recur
            if self.checkConsistency():
                elapsed_time = time.time() - start_time 
                new_start_time = time_left - elapsed_time
                if self.solve(time_left=new_start_time) == -1:
                    return -1
                
            # If this assignment succeeded, return
            if self.hassolution:
                return 0

            # Otherwise backtrack
            self.trail.undo()
        
        return 0

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()[1]

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()[1]

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()[0]

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)
