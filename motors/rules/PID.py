import time
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class PID:
    """PID Controller """

    def __init__(self, P=0.2, I=0.0, D=0.0, current_time=None):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = current_time if current_time is not None else timezone.now()
        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 200.0
        self.output = 0.0

    def setLastError(self, e): 
        self.last_error = e

    def setLastTime(self, t):
        self.last_time = t

    def update(self, feedback_value, current_time=None):
        """Calculates PID value for given reference feedback
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
        """
        error = self.SetPoint - feedback_value

        self.current_time = current_time if current_time is not None else timezone.now()
        logger.debug('current time: %s', self.current_time)
        delta_time = self.current_time - self.last_time
        #logger.debug('delta time: %s', delta_time)
        #logger.debug('delta time.seconds: %s', delta_time.seconds)
        delta_error = error - self.last_error
        logger.debug('error: CUR %s | DELTA %s', error, delta_error)

        if not (delta_time.seconds >= self.sample_time):
            logger.debug('DELTA smaller sample time')
        else:
            self.PTerm = error

            #self.ITerm += error * delta_time.seconds
            self.ITerm += error * (delta_time.seconds / self.sample_time)

            if (self.ITerm < -self.windup_guard):
                logger.debug('ITerm %s - windup %s', self.ITerm, self.windup_guard)
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                logger.debug('ITerm %s - windup %s', self.ITerm, self.windup_guard)
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time.seconds > 0:
                self.DTerm = delta_error / (delta_time.seconds / self.sample_time)
                #self.DTerm = delta_error / delta_time.seconds

            KpTerm = self.Kp * self.PTerm
            KiTerm = self.Ki * self.ITerm
            KdTerm = self.Kd * self.DTerm
            self.output = KpTerm + KiTerm + KdTerm
            logger.debug('Kp Ki Kd - %s | %s | %s', self.Kp, self.Ki, self.Kd)
            logger.debug('P - I - D: %s | %s | %s', self.PTerm, self.ITerm, self.DTerm)
            logger.debug('P - I - D: %s | %s | %s', KpTerm, KiTerm, KdTerm)
            logger.debug(__name__)
#            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time

