from math import log10
import logging

logger = logging.getLogger()

def c2k(c): return c+273
def k2c(k): return k-273



class Thermistor:

  def __init__(self):
    pass

  def set_RTvalues(self, measured=None):
    """ set measured values for init and calc of abc """
    if not measured:
      measured = self.measured
    num = len(measured)

    # init vars
    TCvalues  = [0]*num
    TKvalues  = [0]*num
    Rvalues   = [0]*num

    for i in range(num):
      ind = i
      #print(ind, measured[ind])
      TCvalues[i] = measured[ind][0]
      Rvalues[i]  = measured[ind][1]

      TKvalues[i] = c2k(TCvalues[i])

    self.TKvalues = TKvalues
    self.Rvalues = Rvalues

    self.num = num
    #self.steinh = self.prep_abc()


  def prep_abc(self):
    """ param are 3 resistor values
      and 3 temperature values
    """
    # preparing calculations
    L = [0]*self.num
    y = [0]*self.num

    for i in range(self.num):
      L[i] = log10(self.Rvalues[i])
      y[i] = 1 / self.TKvalues[i]

    L1 = L[0]
    L2 = L[1]
    L3 = L[2]

    y1 = y[0]
    y2 = y[1]
    y3 = y[2]

    gam2 = (y2-y1) / (L2-L1)
    gam3 = (y3-y1) / (L3-L1)

    c = ((gam3-gam2) / (L3-L2)) * (L1+L2+L3)**-1
    b = gam2 - c * (L1**2 + L1*L2 + L2**2)
    a = y1 - (b + L1**2*c) * L1

    #print(a, b, c)
    self.steinh = (a,b,c)


  def resistance_to_temp(self, r):
    a,b,c = self.steinh
    if r < 0:
      logger.error('resistance negative !!! MAKE IT ABS')
      r = abs(r)
    logger.info('resistance : %s', r)
    
    try:
      kelvin = 1 / (a + b*log10(r) + c*(log10(r)**3))
    except:
      logger.error('resistance_to_temp MATH ERROR')
      kelvin = 273.0
    #logger.debug('calc kelvin: %s', kelvin)
    #print(kelvin, "KELVIN")
    celsius = k2c(kelvin)
    return celsius



class ThermistorNT10(Thermistor):
  measured = [
    [-50.0, 667830],
    [25, 10000],
    [150, 180],
  ]
class ThermistorNT20(Thermistor):
  measured = [
    [-50.0, 1667570],
    [25, 20000],
    [150, 270],
  ]

class ThermistorVF20(Thermistor):
  measured = [
    [0, 71120],
    [32, 14491],
    [60, 4473.9],
  ]
  """ ALT
  measured = [
    [-20.0, 220000],
    [25.0, 20000],
    [100.0, 1100],
  ]
  """
