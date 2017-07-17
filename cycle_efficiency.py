import pint

unit = pint.UnitRegistry()
qty = 3 * unit.meter + 4 * unit.cm
print(qty)

# This was originally written in MATLAB for a NE 500 project
# it is rewritten herein for practice
# This uses the IAPWS and pint modules. Should be fun!