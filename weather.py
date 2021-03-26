
import os
import logging
from datetime import datetime
import pyowm
api_key = '5ee1fd485a9d1d7fe9f7e3e2039de757'

logger = logging.getLogger()

def outdoor_setup():
  owm = pyowm.OWM()
  obs = owm.three_hours_forecast('Augsburg')
  fd = obs.forecast.to_dict()
  tempdict = {}
  for i in len(fd['weathers']):
    temp = fd['weathers'][i]['temperature']['temp']
    t =    fd['weathers'][i]['reference_time']
    dt = datetime.fromtimestamp(t)
    tempdict[dt] = temp
    logger.debug(dt)



