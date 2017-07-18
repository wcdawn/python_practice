import pint
from iapws import IAPWS97

def iapws_units(**kwargs):
  unit = pint.UnitRegistry()
  for key,value in kwargs.items():
    if key == 'T':
      kwargs[key] = value.to(unit.degK).magnitude
    elif key == 'P':
      kwargs[key] = value.to(unit.MPa).magnitude
    elif key == 'h':
      kwargs[key] = value.to(unit.kJ / unit.kg).magnitude
    elif key == 's':
      kwargs[key] = value.to(unit.kJ / (unit.kg * unit.degK)).magnitude
    elif key == 'x':
      # it should already be a float
      kwargs[key] = value
  prop = IAPWS97(**kwargs)
  prop.P *= unit.MPa
  prop.T *= unit.degK
  prop.g *= (unit.kJ / unit.kg)
  prop.a *= (unit.kJ / unit.kg)
  prop.v *= (unit.m**3 / unit.kg)
  prop.rho *= (unit.kg / unit.m**3)
  prop.h *= (unit.kJ / unit.kg)
  prop.u *= (unit.kJ / unit.kg)
  prop.s *= (unit.kJ / (unit.kg * unit.degK))
  prop.cp *= (unit.kJ / (unit.kg * unit.degK))
  prop.cv *= (unit.kJ / (unit.kg * unit.degK))
  prop.f *= unit.MPa
  prop.alfav *= 1 / unit.degK
  prop.xkappa *= 1 / unit.MPa
  prop.kappas *= 1 / unit.MPa
  prop.alfap *= 1 / unit.degK
  prop.betap *= (unit.kg / unit.m**3)
  prop.joule *= (unit.degK / unit.MPa)
  prop.deltat *= (unit.kJ / (unit.kg * unit.MPa))
  prop.v0 *= (unit.m**3 / unit.kg)
  prop.u0 *= (unit.kJ / unit.kg)
  prop.h0 *= (unit.kJ / unit.kg)
  prop.s0 *= (unit.kJ / (unit.kg * unit.degK))
  prop.a0 *= (unit.kJ / unit.kg)
  prop.g0 *= (unit.kJ / unit.kg)
  prop.cp0 *= (unit.kJ / (unit.kg * unit.degK))
  prop.cv0 *= (unit.kJ / (unit.kg * unit.degK))
  prop.w0 *= (unit.m / unit.s)
  prop.w *= (unit.m / unit.s)
  prop.mu *= (unit.Pa * unit.s)
  prop.nu *= (unit.m**2 / unit.s)
  prop.k *= (unit.W / (unit.m * unit.degK))
  prop.alfa *= (unit.m**2 / unit.s)
  # prop.sigma *= (unit.N / unit.m)
  return prop