"""""""""    NOTES BELOW
Maximize 3x + 4y subject to the following constraints:
x + 2y	≤	14
3x – y	≥	0
x – y	≤	2
The objective function in this example is f(x, y) = 3x + 4y. 
Both the objective function and the constraints are given by linear expressions, which makes this a linear problem.

Main steps in solving the problem
For each language, the basic steps for setting up and solving a problem are the same:

Create the variables.
Define the constraints.
Define the objective function.
Declare the solver—the method that implements an algorithm for finding the optimal solution.
Invoke the solver and display the results.
"""
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver(name='SolveLP', problem_type=pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# Create 2 variables and let them take any value
x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

# Constraint 1: x + 2y	≤	14
constraint1 = solver.Constraint(-solver.infinity(), 14)
constraint1.SetCoefficient(x, 1)
constraint1.SetCoefficient(y, 2)

# Constraint 2: 3x - y >= 0.
constraint2 = solver.Constraint(0, solver.infinity())
constraint2.SetCoefficient(x, 3)
constraint2.SetCoefficient(y, -1)

# Constraint 3: x - y <= 2.
constraint3 = solver.Constraint(-solver.infinity(), 2)
constraint3.SetCoefficient(x, 1)
constraint3.SetCoefficient(y, -1)

# Objective Function: 3x + 4y
objective = solver.Objective()
objective.SetCoefficient(x, 3)
objective.SetCoefficient(y, 4)
objective.SetMaximization()

# Solve the system
solver.Solve()
opt_solution = 3 * x.solution_value() + 4 * y.solution_value()
print('Number of vars =', solver.NumVariables())
print('Number of constraints =', solver.NumConstraints())

print('Solution is x=', x.solution_value(),'y =', y.solution_value())
print('Optimal objective value=', opt_solution)


"""
In any linear optimization problem at least one vertex of the feasible region must be an optimal solution.
As a result, you can find an optimal solution by traversing the vertices of the feasible region until there is no more
improvement in the objective function. 

This is the idea behind simplex algorithm, the most widely-used method for solving linear optimization problems.
"""


