"""""""""

Problems that require some, but not all, of the variables to be integers can be solved using Mixed Integer Programming 
(MIP), which is also referred to as Mixed Integer Linear Programming (MILP). 

Here are a couple of examples:

1) A company that sells various consumer items needs to decide how many of each to manufacture per month in order to 
maximize profit. In this type of problem, the variables represent quantities of discrete items, such as cars or 
television sets, which must be integers.

2) A package delivery company needs to assign trucks to various routes in order to meet their delivery schedule while 
minimizing cost. Sometimes the best way to set up a problem like this is to let the variables represent binary (0-1) 
decisions of which trucks to assign to which routes. The variable is 1 if a given truck is assigned to a specific route, 
and 0 otherwise. Since the variables can only take on the values 0 or 1, this is also an integer optimization problem. 
(In particular, it's a Boolean optimization problem, which OR-Tools has specialized techniques for solving.)

"""