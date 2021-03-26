#!/usr/bin/python3

import os
import logging
import sys
from time import sleep
fn = os.environ['HOME'] + '/log/pi_sim.log'
logging.basicConfig(
  filename=fn,
  #level=logging.INFO,
  level=logging.DEBUG,
)
# create console handler and set level to debug
logger = logging.getLogger()

import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()
from django.utils import timezone
from sensors.models import *
from sensors.TempCalc import TempCalc
from cntrl.models import ControlEvent

from random import randint
import pickle

stoer_max = 50
stoer_term = '-((2*t_cur)**2) + 400'

class Sim:
  def __init__(self):
    self.tz_now = timezone.now()
    self.basedir = os.environ['HOME']+'/git-github/piheatweb/tmp'

  def setup(self):
    self.last = ControlEvent.objects.all().order_by('-id')[:4]
    self.last_ce     = self.last[0]
    self.readingevent = ReadingEvent(dtime=self.tz_now)
    logger.debug(self.last_ce)

  def all(self):
    for s in range(4):
      sid = s+1
      latest = self.load_latest_adc(sid)      
      sensor_val = self.s1(sid, latest)
      #if not sensor_val:
      self.save(sid, sensor_val)

  def will_continue_normal(self):
    r = bool(randint(0, 4))
    logger.debug('will_continue_normal? : random says: %s', r)
    return r

  def s1(self, sid, latest):
    """ find out what stoered value sensor sid currently has """
    str_sid = '0'+ str(sid)
    sid = str_sid
    logger.info('=== === start %s', sid)
    steady = latest
    mark = ''
    self.p_fn   = self.basedir + '/pickle_'+sid
    self.mark_fn= self.basedir + '/state_'+sid+'.txt'
    mark_fn = self.mark_fn
    p_fn = self.p_fn

    mark = self.file_checkexists_and_read(mark_fn, name='MARK file')

    if mark and 's1' in mark:

      dt_started = self.file_checkexists_and_read(p_fn, is_pickle=True, name='dt pickle')
      if not dt_started:
        dt_started = self.tz_now
        logger.error('dt_started MISSING, set to current time')

      logger.debug('loaded start time: %s', dt_started)
      since = self.tz_now - dt_started
      stoer = self.stoerfunc(since.seconds)
      logger.info('XXX --- stoerfunc started on %s, =since: %s IS: %s', dt_started, since.seconds, stoer)
      val_res = steady + stoer

      if since.seconds > stoer_max:
        logger.debug('XXX stoerfunc meanwhile since > 100 sec --> DELETE')
        # bisherigen eintrag loeschen
        self.file_checkexists_and_truncate(p_fn)
        self.file_checkexists_and_truncate(mark_fn)

    # No Mark entry yet for this sensor - no stoerfunc currently active
    else:
      val_res = steady

      if not self.will_continue_normal():
        logger.info('NORMAL --> START NEW stoerfunc')
        self.file_checkexists_and_write(mark_fn, 's1')

        self.file_checkexists_and_write(p_fn, self.tz_now, is_pickle=True)
        #self.store(self.tz_now)
      else:
        logger.debug('KEEP things as they are...')

    logger.info('new val: %s', val_res)
    return val_res

  def file_checkexists_and_truncate(self, fn, is_pickle=False):
    if os.path.exists(fn):
      try:
        os.remove(fn)
        logger.debug('file %s deleted', fn)
      except:
        logger.error('deleting %s FAILED', fn)
    else:
      logger.error('FILE %s did not exist', fn)

  def file_checkexists_and_read(self, fn, is_pickle=False, name=''):
    """ return file content or NONE if unsuccessful """
    res = None
    if os.path.exists(fn):
      logger.debug('Checking file for %s - fn: %s', name, fn)
      if is_pickle: 
        f = open(fn, 'rb')
        res = pickle.load(f)
      else:      
        f = open(fn, 'r')
        val = f.read()
        res = val.strip()
      f.close()
    else:
      logger.error('File %s NOT existing', fn)
    return res


  def file_checkexists_and_write(self, fn, con, is_pickle=False):
    if not os.path.exists(fn):
      try:
        logger.debug('WRITING fn: %s', fn)
        if is_pickle: 
          f = open(fn, 'wb')
          pickle.dump(con, f)
        else: 
          f = open(fn, 'w')
          f.write(con)
        f.close()
      except:
        logger.error('FAILED: Writing file failed')
    else:
      logger.error('File ALREADY existing')

  def store(self, val):
    logger.debug('storing dt: %s', val)
    p_file = open(self.p_fn, 'bw')
    pickle.dump(val, p_file)
    p_file.close()


  # dependent on time going by. We need a starting time (offset)
  # and a function yst(t)
  def stoerfunc(self, t_cur):
    val = eval(stoer_term)
    logger.debug('calc:  for t_cur=%s --> %s', t_cur, val) 
    return val


  def inital_sensor_vals(self):
    startval = [4000, 6000, 8000, 10000]
    for i in range(4):
      self.save(i+1, startval.pop())

  def save(self, sid, val):
    # create new sensor data entry
    str_sid = '0'+str(sid)
    evalstr = 'SensorData_'+str_sid+'()'
    obj = eval(evalstr)
    obj.dtime = self.tz_now
    obj.temperature = 0
    obj.resistance = 0
    obj.adc_out = val

    # link key to controlevent
    obj.ctrl_event = self.last_ce
    obj.save()
    # legacy readingevent
    evalstr = 'self.readingevent.sid'+str_sid+'=obj'
    exec(evalstr)
    self.readingevent.save()

  def load_latest_adc(self, sid):
    str_sid = '0'+str(sid)
    evalstr = 'SensorData_'+str_sid+".objects.latest('-id')"
    logger.debug(evalstr)
    obj = eval(evalstr)
    return obj.adc_out




def read_adc():
#  logger.debug('-----------------------------')
  sim = Sim()
  sim.setup()
  #sim.inital_sensor_vals()
  #sys.exit()

  sim.all()
#  sensor_1 = sim.s1('01')
#  sim.save(1, sensor_1)

# cron version
from calc_temp_latest_daemon import tempcalc
if __name__ == '__main__':
  logger.debug('START READER ======================')
  read_adc()
  tempcalc()
