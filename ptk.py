import numpy as np
import pint
unit = pint.UnitRegistry()
# Euler Method for Point Kinetics

# beta values for delayed neutron precursor groups
beta = np.array([0.00021,0.00142,0.00128,0.00257,0.00075,0.00027],dtype=float)
# half-lives for delayed neutron precursor groups (in seconds)
pre_t12 = np.array([56.0,23.0,6.2,2.3,0.61,0.23],dtype=float) * unit.s
gen_time = 0.0001 * unit.s