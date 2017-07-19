import numpy as np
import matplotlib.pyplot as plt
import pint
unit = pint.UnitRegistry()
# Euler Method for Point Kinetics

# beta values for delayed neutron precursor groups
beta = np.array([0.00021,0.00142,0.00128,0.00257,0.00075,0.00027],dtype=float)
# half-lives for delayed neutron precursor groups (in seconds)
pre_t12 = np.array([56.0,23.0,6.2,2.3,0.61,0.23],dtype=float) # * unit.s
# neutron generation time (in seconds)
gen_time = 0.0001 # * unit.s
# step reactivity change (rho) (in k)
rho = 200.0e-5
# transient end-time (in seconds)
end_time = 4.0
# number of timesteps
nStep = 1000

neut = np.zeros(nStep)
time = np.zeros(nStep)
c = np.zeros((nStep,len(beta)))

# sum beta and calculate precursor decay constants
sum_beta = np.sum(beta)
pre_lam = np.log(2.0) / pre_t12

# initializations
dt = end_time / nStep
neut[0] = 1.0
time = np.linspace(0.0,end_time,num=nStep)
# initialize precursor populations
c[0,:] = (beta[:] / (gen_time * pre_lam[:])) * neut[0]

for i in range(nStep):
  if i == 0:
    continue
  c[i,:] = c[(i - 1),:] + (beta[:] / gen_time) * neut[i - 1] * dt - \
    pre_lam[:] * c[(i - 1),:] * dt
  production_term = np.sum(pre_lam[:] * c[(i - 1),:] * dt)
  neut[i] = neut[(i - 1)] + ((rho - sum_beta) / gen_time) * neut[(i - 1)] * \
    dt + production_term

plt.plot(time,neut)
plt.show()