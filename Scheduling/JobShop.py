"""""""""
One common scheduling problem is the job shop, in which multiple jobs are processed on several machines. 
Each job consists of a sequence of tasks, which must be performed in a given order, and each task must be processed on 
a specific machine. 

There are several constraints for the job shop problem:

No task for a job can be started until the previous task for that job is completed.
A machine can only work on one task at a time.
A task, once started, must run to completion.

Each task is labeled by a pair of numbers (m, p) where m is the number of the machine the task must be processed on 
and p is the processing time of the task — the amount of time it requires. (The numbering of jobs and machines starts at 0.)

job 0 = [(0, 3), (1, 2), (2, 2)]
job 1 = [(0, 2), (2, 1), (1, 4)]
job 2 = [(1, 4), (2, 3)]
In the example, job 0 has three tasks. The first, (0, 3), must be processed on machine 0 in 3 units of time. 
The second, (1, 2), must be processed on machine 1 in 2 units of time, and so on. Altogether, there are eight tasks.
"""


import collections

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model

"""Minimal jobshop problem."""
# Create the model.
model = cp_model.CpModel()

jobs_data = [  # task = (machine_id, processing_time).
    [(0, 3), (1, 2), (2, 2)],  # Job0
    [(0, 2), (2, 1), (1, 4)],  # Job1
    [(1, 4), (2, 3)]  # Job2
]

machines_count = 1 + max(task[0] for job in jobs_data for task in job)
all_machines = range(machines_count)
jobs_count = len(jobs_data)
all_jobs = range(jobs_count)

# Compute horizon.
horizon = sum(task[1] for job in jobs_data for task in job)

task_type = collections.namedtuple('task_type', 'start end interval')
assigned_task_type = collections.namedtuple('assigned_task_type',
                                            'start job index')

# Create jobs.
all_tasks = {}
for job in all_jobs:
    for task_id, task in enumerate(jobs_data[job]):
        start_var = model.NewIntVar(0, horizon,
                                    'start_%i_%i' % (job, task_id))
        duration = task[1]
        end_var = model.NewIntVar(0, horizon, 'end_%i_%i' % (job, task_id))
        interval_var = model.NewIntervalVar(
            start_var, duration, end_var, 'interval_%i_%i' % (job, task_id))
        all_tasks[job, task_id] = task_type(
            start=start_var, end=end_var, interval=interval_var)

# Create and add disjunctive constraints.
for machine in all_machines:
    intervals = []
    for job in all_jobs:
        for task_id, task in enumerate(jobs_data[job]):
            if task[0] == machine:
                intervals.append(all_tasks[job, task_id].interval)
    model.AddNoOverlap(intervals)

# Add precedence contraints.
for job in all_jobs:
    for task_id in range(0, len(jobs_data[job]) - 1):
        model.Add(all_tasks[job, task_id +
                            1].start >= all_tasks[job, task_id].end)

# Makespan objective.
obj_var = model.NewIntVar(0, horizon, 'makespan')
model.AddMaxEquality(
    obj_var,
    [all_tasks[(job, len(jobs_data[job]) - 1)].end for job in all_jobs])
model.Minimize(obj_var)

# Solve model.
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    # Print out makespan.
    print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
    print()

    # Create one list of assigned tasks per machine.
    assigned_jobs = [[] for _ in all_machines]
    for job in all_jobs:
        for task_id, task in enumerate(jobs_data[job]):
            machine = task[0]
            assigned_jobs[machine].append(
                assigned_task_type(
                    start=solver.Value(all_tasks[job, task_id].start),
                    job=job,
                    index=task_id))

    disp_col_width = 10
    sol_line = ''
    sol_line_tasks = ''

    print('Optimal Schedule', '\n')

    for machine in all_machines:
        # Sort by starting time.
        assigned_jobs[machine].sort()
        sol_line += 'Machine ' + str(machine) + ': '
        sol_line_tasks += 'Machine ' + str(machine) + ': '

        for assigned_task in assigned_jobs[machine]:
            name = 'job_%i_%i' % (assigned_task.job, assigned_task.index)
            # Add spaces to output to align columns.
            sol_line_tasks += name + ' ' * (disp_col_width - len(name))
            start = assigned_task.start
            duration = jobs_data[assigned_task.job][assigned_task.index][1]

            sol_tmp = '[%i,%i]' % (start, start + duration)
            # Add spaces to output to align columns.
            sol_line += sol_tmp + ' ' * (disp_col_width - len(sol_tmp))

        sol_line += '\n'
        sol_line_tasks += '\n'

    print(sol_line_tasks)
    print('Task Time Intervals\n')
    print(sol_line)
