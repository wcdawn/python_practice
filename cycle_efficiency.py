import pint
from iapws import IAPWS97
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

# TO-DO: get rid of this
unit = pint.UnitRegistry()
qty = 3 * unit.meter + 4 * unit.cm
print(qty)

# This was originally written in MATLAB for a NE 500 project
# it is rewritten herein for practice
# This uses the IAPWS and pint modules. Should be fun!

# conversion factor for english units
# TO-DO: do I need this?
k = 144.0 / 778.0
# initializing variables for mass flow error
# TO-DO: do I need this?
m_error = 0

class eta_type(object):
  def __init__(self):
    self.hpt = 0.0
    self.lpt = 0.0
    self.cp  = 0.0
    self.fwp = 0.0

class prop_type(object):
  def __init__(self):
    self.P = 0.0
    self.h = 0.0
    self.s = 0.0
    self.T = 0.0
    self.hs = 0.0
    self.prop = 0.0

state = []
for i in range(11):
  state.append(prop_type())

# chosen values for turbine and pump efficiency
# these values are chosen to make an interesting total efficiency distribution
eta = eta_type()
eta.hpt = 0.9
eta.lpt = 0.6
eta.cp  = 0.8
eta.fwp = 0.8

# vary P0 from 110 to 3200 psia in increments of 100 psia
pressure_mesh_s0 = (np.arange(110.0,3200.0,500.0)) * unit.psi

# preallocate eta_total array
eta_total = np.zeros((len(pressure_mesh_s0),len(np.arange(2.0,pressure_mesh_s0[-1].to(unit.psi).magnitude,50.0))),dtype=float)
xarr = np.zeros((len(pressure_mesh_s0),len(np.arange(2.0,pressure_mesh_s0[-1].to(unit.psi).magnitude,50.0))),dtype=float)
yarr = np.zeros((len(pressure_mesh_s0),len(np.arange(2.0,pressure_mesh_s0[-1].to(unit.psi).magnitude,50.0))),dtype=float)

for i in range(len(pressure_mesh_s0)):

  # define P0 for this iteration
  state[0].P = pressure_mesh_s0[i]
  # the turbine tap is assumed to be at 100 psia below the reactor pressure
  state[2].P = state[0].P - 100.0 * unit.psi

  # P3 ranges from 2 to P2 psia in increments of 1 psia
  pressure_mesh_s3 = (np.arange(2.0,state[2].P.to(unit.psi).magnitude,50.0)) * unit.psi

  for j in range(len(pressure_mesh_s3)):
    # STATE 0
    state[0].prop = IAPWS97(P=state[0].P.to(unit.MPa).magnitude,x=1.0)
    state[0].h = state[0].prop.h * (unit.kJ/unit.kg)
    state[0].s = state[0].prop.s * (unit.kJ/(unit.kg*unit.degK))

    # STATE 1
    state[1].P = state[0].P
    state[1].h = state[0].h

    # STATE 2
    state[2].prop = IAPWS97(P=state[2].P.to(unit.MPa).magnitude,
      s=state[0].s.to(unit.kJ/(unit.kg*unit.degK)).magnitude)
    state[2].hs = state[2].prop.h * (unit.kJ/unit.kg)
    state[2].h = state[0].h - eta.hpt * (state[0].h - state[2].hs)
    state[2].prop = IAPWS97(P=state[2].P.to(unit.MPa).magnitude,
      h=state[2].h.to(unit.kJ/unit.kg).magnitude)
    state[2].T = state[2].prop.T * unit.degK

    # STATE 3
    state[3].P = pressure_mesh_s3[j]
    state[3].prop = IAPWS97(P=state[3].P.to(unit.MPa).magnitude,
      s=state[0].s.to(unit.kJ/(unit.kg*unit.degR)).magnitude)
    state[3].hs = state[3].prop.h * (unit.kJ/unit.kg)
    state[3].h = state[0].h - eta.hpt * (state[0].h - state[3].hs)

    # STATE 4
    # assume fully condensed
    state[4].P = state[2].P
    state[4].prop = IAPWS97(P=state[4].P.to(unit.MPa).magnitude,x=0.0)
    state[4].h = state[4].prop.h * (unit.kJ/unit.kg)

    # STATE 5
    # good thermal conductivity
    # the 5 deg difference is due to numerical calculation
    # if the difference is 0, the values are too close and results equal 1.0
    state[5].P = state[3].P
    state[5].T = state[2].T - 5.0 * unit.degR
    state[5].prop = IAPWS97(P=state[5].P.to(unit.MPa).magnitude,
      T=state[5].T.to(unit.degK).magnitude)
    state[5].h = state[5].prop.h * (unit.kJ/unit.kg)
    state[5].s = state[5].prop.s * (unit.kJ/(unit.kg*unit.degK))

    # STATE 6
    state[6].P = 1.0 * unit.psi
    state[6].prop = IAPWS97(P=state[6].P.to(unit.MPa).magnitude,
      s=state[5].s.to(unit.kJ/(unit.kg*unit.degK)).magnitude)
    state[6].hs = state[6].prop.h * (unit.kJ/unit.kg)
    state[6].h = state[5].h - eta.lpt * (state[5].h - state[6].hs)

    # STATE 7
    state[7].P = state[6].P
    state[7].prop = IAPWS97(P=state[7].P.to(unit.MPa).magnitude,x=0.0)
    state[7].h = state[7].prop.h * (unit.kJ/unit.kg)
    state[7].nu = state[7].prop.v * (unit.m**3/unit.kg)

    # STATE 8
    state[8].P = state[4].P
    w_cps = (-1.0) * state[7].nu * (state[8].P - state[7].P)
    w_cp = w_cps / eta.cp
    state[8].h = state[7].h - w_cp

    # STATE 9
    # assume fully condensed
    state[9].P = state[4].P
    state[9].prop = IAPWS97(P=state[9].P.to(unit.MPa).magnitude,x=0.0)
    state[9].h = state[9].prop.h * (unit.kJ/unit.kg)
    state[9].nu = state[9].prop.v * (unit.m**3/unit.kg)

    # STATE 10
    state[10].P = state[0].P
    w_fwps = (-1) * state[9].nu * (state[10].P - state[9].P)
    w_fwp = w_fwps / eta.fwp
    state[10].h = state[9].h - w_fwp

    # build matrix to solve for relative mass flow rates
    A = np.array([[(state[5].h.magnitude - state[3].h.magnitude),
      (state[2].h.magnitude - state[3].h.magnitude - state[4].h.magnitude + state[5].h.magnitude)],
      [(state[1].h.magnitude - state[8].h.magnitude),
      (state[4].h.magnitude - state[8].h.magnitude)]])
    B = np.array([(state[5].h.magnitude - state[3].h.magnitude),
      (state[9].h.magnitude - state[8].h.magnitude)])
    X = np.linalg.solve(A,B)
    m21 = X[0]
    m31 = X[1]
    if not(m21 > 0) or not(m31 > 0):
      m_error += 1
      print(m21,m31)
      print('m_error')
    
    # calculate works relative to mass flow rates
    work_hpt = (state[0].h - state[1].h) + \
      (1 - m21) * (state[1].h - state[2].h) + \
      (1 - m21 - m31) * (state[2].h - state[3].h)
    work_lpt = (1 - m21 - m31) * (state[5].h - state[6].h)
    work_cp  = (1 - m21 - m31) * w_cps
    work_fwp = w_fwp
    Q = (state[0].h - state[10].h)
    
    # calculate total efficiency
    eta_total[i,j] = (work_hpt + work_lpt + work_cp + work_fwp) / (Q)
    xarr[i,j] = pressure_mesh_s0[i].to(unit.psi).magnitude
    yarr[i,j] = pressure_mesh_s3[j].to(unit.psi).magnitude
    if not(0.0 < eta_total[i,j] < 1.0):
      print('eta error ',eta_total[i,j])

# this plot could use a lot of help but it works
surf = ax.plot_surface(xarr,yarr,eta_total)
plt.show()