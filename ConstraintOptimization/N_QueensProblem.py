"""""""""
constraint programming (CP) by a combinatorial problem based on the game of chess. In chess, a queen can attack 
horizontally, vertically, and diagonally. The N-queens problem asks:

How can N queens be placed on an NxN chessboard so that no two of them attack each other?

Note that this isn't an optimization problem: we want to find all possible solutions, rather than one optimal solution, 
which makes it a natural candidate for constraint programming. The following sections describe the CP approach to the 
N-queens problem, and present Python programs that solve it using both the CP-SAT solver and the original CP solver.


There are two key elements to a constraint programming search:

Propagation — Each time the solver assigns a value to a variable, the constraints add restrictions on the possible 
            values of the unassigned variables. These restrictions propagate to future variable assignments. 
            For example, in the 4-queens problem, each time the solver places a queen, it can't place any other queens 
            on the row and diagonals the current queen is on. Propagation can speed up the search significantly by 
            reducing the set of variable values the solver must explore.
Backtracking-  occurs when either the solver can't assign a value to the next variable, due to the constraints, or 
            it finds a solution. In either case, the solver backtracks to a previous stage and changes the value of the 
            variable at that stage to a value that hasn't already been tried. In the 4-queens example, this means 
            moving a queen to a new square on the current column.
"""

from ortools.constraint_solver import pywrapcp

board_size = 8

solver = pywrapcp.Solver('n-queens')

queens = [solver.IntVar(0, board_size-1, "x%i" % i) for i in range(board_size)]

# All rows must be different.
solver.Add(solver.AllDifferent(queens))

# All columns must be different because the indices of queens are all different.
# No two queens can be on the same diagonal.
solver.Add(solver.AllDifferent([queens[i] + i for i in range(board_size)]))
solver.Add(solver.AllDifferent([queens[i] - i for i in range(board_size)]))

db = solver.Phase(queens, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
solver.NewSearch(db)

num_solutions = 0

while solver.NextSolution():
    for i in range(board_size):
        for j in range(board_size):
            if queens[j].Value() == i:      # Implies There is a Queen in column j, row i
                print('Q', end=' ')
            else:
                print('_', end=' ')
        print()
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
    num_solutions += 1


print("Solutions found:", num_solutions)
print("Time:", solver.WallTime(), "ms")
