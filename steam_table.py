from iapws_pass import iapws_units as iapws97
import matplotlib.pyplot as plt
import numpy as np
import pint
unit = pint.UnitRegistry()
Q_ = unit.Quantity

pres = 2250.0 * unit.psi
t_mesh = Q_(np.arange(300.0,1200.0,10.0),unit.degF)
h_mesh = []
for i in range(len(t_mesh)):
  prop = iapws97(P=pres,T=t_mesh[i])
  h_mesh.append(prop.h)

for i in range(len(t_mesh)):
  h_mesh[i] = h_mesh[i].to(unit.Btu/unit.lb).magnitude
h_mesh = np.asarray(h_mesh,dtype=float)
t_mesh = t_mesh.to(unit.degF).magnitude
t_mesh = np.asarray(t_mesh,dtype=float)
plt.plot(t_mesh,h_mesh)
plt.show()