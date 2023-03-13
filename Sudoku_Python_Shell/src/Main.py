#!/usr/bin/env python3

import sys
import os
import math
import SudokuBoard
import Constraint
import ConstraintNetwork
import BTSolver
import Trail
import time

"""
    Main driver file, which is responsible for interfacing with the
    command line and properly starting the backtrack solver.
"""

def main ( ):
    args = sys.argv

    # Important Variables
    file   = "";
    var_sh = "";
    val_sh = "";
    cc     = "";

    for arg in [args[i] for i in range(1, len(args))]:
        if arg == "MRV":
            var_sh = "MinimumRemainingValue"

        elif arg == "MAD":
            var_sh = "MRVwithTieBreaker"

        elif arg == "LCV":
            val_sh = "LeastConstrainingValue"

        elif arg == "FC":
            cc = "forwardChecking"

        elif arg == "NOR":
            cc = "norvigCheck"

        elif arg == "TOURN":
            var_sh = "tournVar"
            val_sh = "tournVal"
            cc     = "tournCC"

        else:
            file = arg;

    trail = Trail.Trail();

    if file == "":
        # board = [[5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,10],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        
        board = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 2, 0, 0, 0, 5],
                    [0, 0, 0, 0, 7, 1, 0, 0, 0],
                    [0, 0, 0, 3, 0, 0, 0, 0, 2],
                    [0, 0, 0, 0, 0, 0, 3, 0, 0],
                    [5, 0, 2, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        sudokudata = SudokuBoard.SudokuBoard( 3, 3, 7, board=board)
        # sudokudata = SudokuBoard.SudokuBoard(3, 3, 7)
        # sudokudata = SudokuBoard.SudokuBoard(4, 4, 4, board=board)

        print(sudokudata)

        solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, cc )
        #solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, "forwardChecking")
        if cc in ["forwardChecking","norvigCheck","tournCC"]:
            solver.checkConsistency()
        solver.solve()

        if solver.hassolution:
            print( solver.getSolution() )
            print( "Trail Pushes: " + str(trail.getPushCount()) )
            print( "Backtracks: " + str(trail.getUndoCount()) )

        else:
            print( "Failed to find a solution" )

        return

    if os.path.isdir(file):
        listOfBoards = None

        try:
            listOfBoards = os.listdir ( file )
        except:
            print ( "[ERROR] Failed to open directory." )
            return

        numSolutions = 0
        for f in listOfBoards:
            print ( "Running board: " + str(f) )
            sudokudata = SudokuBoard.SudokuBoard( filepath=os.path.join( file, f ) )

            #solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, "forwardChecking")
            solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, cc )
            if cc in ["forwardChecking","norvigCheck","tournCC"]:
                solver.checkConsistency()
            solver.solve()

            if solver.hassolution:
                numSolutions += 1;

        print ( "Solutions Found: " + str(numSolutions) )
        print ( "Trail Pushes: " + str(trail.getPushCount()) )
        print ( "Backtracks: "  + str(trail.getUndoCount()) )

        return

    sudokudata =  SudokuBoard.SudokuBoard( filepath=os.path.abspath( file ) )
    print(sudokudata)

    solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, cc )
    #solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, "forwardChecking")
    if cc in ["forwardChecking","norvigCheck","tournCC"]:
        solver.checkConsistency()
    solver.solve()

    if solver.hassolution:
        print( solver.getSolution() )
        print( "Trail Pushes: " + str(trail.getPushCount()) )
        print( "Backtracks: " + str(trail.getUndoCount()) )

    else:
        print( "Failed to find a solution" )

main()
