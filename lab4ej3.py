from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

# M = model
M = ConcreteModel()

numBaldosas = 20

numTubos = 7

M.N = RangeSet(1,numBaldosas)

M.L = RangeSet(1,numTubos)

M.c = Param(M.N,M.L,mutable=True)

for r in M.N:
    for t in M.L:
        M.c[r,t] = 0

M.c[1,1] = 1
M.c[2,2] = 1
M.c[3,2] = 1
M.c[5,1] = 1
M.c[5,3] = 1
M.c[6,2] = 1
M.c[7,2] = 1
M.c[8,4] = 1
M.c[9,3] = 1
M.c[9,5] = 1
M.c[10,5] = 1
M.c[10,6] = 1
M.c[11,6] = 1
M.c[12,4] = 1
M.c[13,5] = 1
M.c[13,7] = 1
M.c[14,5] = 1
M.c[14,6] = 1
M.c[15,6] = 1
M.c[16,4] = 1
M.c[17,7] = 1
M.c[19,4] = 1
M.c[20,4] = 1

M.x = Var(M.N, domain=Binary)

M.obj = Objective(expr = sum(M.x[i] for i in M.N))

def restriccion1(M,j):

    return sum(M.c[i,j] * M.x[i] for i in M.N) >= 1

M.res1 = Constraint(M.L, rule=restriccion1)

SolverFactory('glpk').solve(M)

M.display()