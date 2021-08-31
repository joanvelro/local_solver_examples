#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   Simple Transport problem

   This problem finds a least cost shipping schedule that meets
    requirements at markets and supplies at factories.


    Dantzig, G B, Chapter 3.3. In Linear Programming and Extensions.
    Princeton University Press, Princeton, New Jersey, 1963.

    This formulation is described in detail in:
    Rosenthal, R E, Chapter 2: A GAMS Tutorial. In GAMS: A User's Guide.
    The Scientific Press, Redwood City, California, 1988.

    The line numbers will not match those in the book because of these
    comments.

    * Single product
    * different freights
    * multiperiod

    Keywords: linear programming, transportation problem, scheduling

"""

import localsolver
from timeit import default_timer as timer

# start time


start = timer()

with localsolver.LocalSolver() as ls:
    #
    # Declares the optimization model
    #
    model = ls.model

    # Sets
    # plants
    plants = ['seatle', 'san-diego']
    # markets
    markets = ['new-york', 'chicago', 'topeka']
    # periods
    periods = ['T1', 'T2', 'T3', 'T4']

    # ::: Parameters :::

    # capacity of plants
    capacity = {'seatle': 350,
                'san-diego': 600}

    # demand at markets
    demand = {'new-york': 325,
              'chicago': 200,
              'topeka': 375}

    # distance in  miles
    distances = {('seatle', 'new-york'): 2500,
                 ('seatle', 'chicago'): 1700,
                 ('seatle', 'topeka'): 1800,
                 ('san-diego', 'new-york'): 2500,
                 ('san-diego', 'chicago'): 1800,
                 ('san-diego', 'topeka'): 1400
                 }

    # transport cost in $/mile-ud from the plants
    freights = {'seatle': 95 / 1000,
                'san-diego': 85 / 1000}

    # =================
    # ::: Variables :::
    # =================

    # shipment quantities in cases
    x_max = 1000
    x = [[[model.int(0, x_max) for i in range(len(plants))] for j in range(len(markets))] for t in range(len(periods))]

    # ====================
    # ::: Constraints :::
    # ====================

    # # Not surpass capacity
    if 1 == 1:
        try:
            for i in range(0, len(plants)):
                model.constraint(model.sum(x[t][j][i] for j in range(len(markets)) for t in range(len(periods))) <= capacity[plants[i]])
        except Exception as exception_msg:
            print('----> (!) Error in capacity constraint: {}'.format(str(exception_msg)))

    # demand
    if 1 == 1:
        try:
            for j in range(0, len(markets)):
                model.constraint(model.sum(x[t][j][i] for i in range(len(plants)) for t in range(len(periods))) >= demand[markets[j]])
        except Exception as exception_msg:
            print('----> (!) Error in demand constraint: {}'.format(str(exception_msg)))

    # ========================
    # ::: Objective function :::
    # ========================
    try:
        OF = model.sum(x[t][j][i] * distances[(plants[i], markets[j])] * freights[plants[i]] for i in range(len(plants))
                       for j in range(len(markets))
                       for t in range(len(periods))
                       )
    except Exception as exception_msg:
        OF = 0
        print('----> (!) Error in objective function: {}'.format(str(exception_msg)))

    model.minimize(OF)

    model.close()

    # ::: model params :::

    # ls.param.time_limit = 5
    ls.param.iteration_limit = 300000

    # vervosity
    ls.param.verbosity = 1

    # ::: Solve model :::
    ls.solve()

    # ::: get solution  :::
    x_sol = {(plants[i], markets[j], periods[t]): x[t][j][i].value for i in range(0, len(plants))
             for j in range(0, len(markets))
             for t in range(0, len(periods))
             }
    total_cost = OF.value
    total_demand = sum([demand[i] for i in demand.keys()])
    total_supply = sum([x_sol[(i, j, t)] for i, j, t in x_sol.keys()])
    print('Total cost: {} $'.format(total_cost))
    print('Total demand: {} ud'.format(total_demand))
    print('Total supply: {} ud'.format(total_supply))
    print('Marginal cost: {} $/ud'.format(total_cost/total_supply))
    print('Optimal solution')
    for i, j, t in x_sol.keys():
        print(' {}--{}--{} : {} Tm'.format(i, j, t, x_sol[(i, j, t)]))

end = timer()
print('\nExecution time: {} s'.format(round(end - start, 4)))
