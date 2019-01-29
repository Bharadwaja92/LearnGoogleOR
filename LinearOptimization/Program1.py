""""""
"""
To solve a very simple optimization problem: find the maximum value of the objective function x + y, 
subject to the constraints 0 ≤ x ≤ 1 and 0 ≤ y ≤ 2.
"""

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver('SolveSimpleLinearProgram', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# Create variables x and y
x = solver.NumVar(lb=0, ub=1, name='x')
y = solver.NumVar(lb=0, ub=2, name='y')

# Create an Objective Function x+y
objective = solver.Objective()
objective.SetCoefficient(x, 1)
objective.SetCoefficient(y, 1)
objective.SetMaximization()

# Call the solver and display the results
solver.Solve()
print('x = ', x.solution_value())
print('y = ', y.solution_value())



