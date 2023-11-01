from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

# M = model
M = ConcreteModel()

origen = 3
destino = 2

M.N = RangeSet(1,origen)

M.L = RangeSet(1,destino )

costo = {
    (1,1): 300, (1,2): 500,\
    (2,1): 200, (2,2): 300,\
    (3,1): 600, (3,2): 300}

M.su = Param(M.N, mutable=True) #Cantidad de procesos a suministrar para usuario

M.su[1]=80
M.su[2]=50
M.su[3]=50

M.du = Param(M.L, mutable=True) #Cantidad de procesos demandada para usuario

M.du[1]=60
M.du[2]=120

M.sk = Param(M.N, mutable=True) #Cantidad de procesos a suministrar para los kernel

M.sk[1]=60
M.sk[2]=80
M.sk[3]=50

M.dk = Param(M.L, mutable=True) #Cantidad de procesos demandada para los kernel

M.dk[1]=100
M.dk[2]=90

M.x = Var(M.N,M.L, domain=PositiveReals) #procesos de procesador usuario
 
M.xk = Var(M.N,M.L, domain=PositiveReals) # procesos de procesador kernel

M.obj = Objective(expr=sum(costo[i,j]*M.x[i,j] for i in M.N for j in M.L)+sum(costo[i,j]*M.xk[i,j] for i in M.N for j in M.L), sense=minimize)

def res1(M,j):      # En GAMS se ve asi:  enviadosU(j)  .. sum((i), x(i,j)) =e= m(j)
    return sum(M.x[i,j] for i in M.N) == M.du[j]

M.res1 = Constraint(M.L, rule=res1)

def res2(M,i):      # En GAMS se ve asi:  recibidosU(i) .. sum((j), x(i,j)) =e= n(i)
    return sum(M.x[i,j] for j in M.L) == M.su[i]

M.res2 = Constraint(M.N, rule=res2)

def res3(M,j):      # En GAMS se ve asi:  enviadosK(j) .. sum((i), xk(i,j)) =e= mk(j)
    return sum(M.xk[i,j] for i in M.N) == M.dk[j]

M.res3 = Constraint(M.L, rule=res3)

def res4(M,i):      # En GAMS se ve asi:  recibidosK(i) .. sum((j), xk(i,j)) =e= nk(i)
    return sum(M.xk[i,j] for j in M.L) == M.sk[i]

M.res4 = Constraint(M.N, rule=res4)

SolverFactory('glpk').solve(M)

M.display()