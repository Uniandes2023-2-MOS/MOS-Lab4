from pyomo.environ import *

model = ConcreteModel()

pueblos = range(6)

model.x = Var(pueblos, within=Binary)

model.obj = Objective(expr=sum(model.x[i] for i in pueblos), sense=minimize)

model.coverage = ConstraintList()
for i in pueblos:
    model.coverage.add(sum(model.x[j] for j in pueblos) >= 1)

solver = SolverFactory('glpk')
solver.solve(model)
cantidad = 0
print("Ubicación óptima de estaciones de bomberos:")
for i in pueblos:
    if model.x[i].value == 1:
        print(f"Estación en pueblo {i + 1}")
        cantidad += 1
        
print("Cantidad de estaciones de bomberos: " + str(cantidad)) 
