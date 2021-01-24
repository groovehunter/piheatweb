from Thermistor import *


# example NT10  
measured = [
    [-40.0, 327344],
    [25.0, 10000],
    [110.0, 509],
]


if __name__ == '__main__':

  # one time   
  thermi = ThermistorNT10()
  #thermi = ThermistorVF20()
  thermi.set_RTvalues() 
  thermi.prep_abc()
  
  # every measured value
  rmes = 10000
  thermi.resistance_to_temp(rmes)

