# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:27:51 2020

@author: mberutti
"""
import time

from gpiozero import LED


from smarttoilet.signals import SignalIn, SignalOut

class Control:
    """ Class for controlling entire system
    """
    def __init__(self):
        # input signals
        self.power = SignalIn(7, led=(11, 12))
        self.fluid = SignalIn(13, led=15)
        self.force_wash = SignalIn(29)
        
        # output signals
        self.motor = SignalOut(16)
        self.wash = SignalOut(31, led=32)
        
        # other indicators
        self.cam_led = LED(33)
        self.analysis_led = (LED(35), LED(36))
        self.error = LED(40)
        
        self.run()
            
    
    def __exit__(self):
        """ Turn off LEDs and outputs when exiting
        """
        self._stop_all()
        
    def _stop_all(self):
        """ Turn off all outputs and LEDs
        """
        # LEDs
        self.cam_led.off
        self.analysis_led[0].off
        self.analysis_led[1].off
        self.error.off
        
        # motors
        self.motor.off()
        self.wash.off()
        
    def analyze(self):
        """ Control method for analyzing the sample.
            Runs until complete or an error occurs.
        """
        self._stop_all()
        # run the following while the power switch is on
        try:
            while True:
                if not self.power.update():
                    break
        except:
            # turn on error indicator and turn off else
            self._stop_all()
            self.error.on
        
    def run(self):
        """ Automation system
        """        
        # run continuously after initialization
        while True:
            # run analysis if power switch is on, there is fluid in the
            # system, and there isn't a prevailing error
            if self.power.update() and \
                    self.fluid.update() and \
                    not self.error.is_active:
                self.analyze()
            
            # if the power switch is off, turn off everything
            # resets the error light
            elif not self.power.update():
                self._stop_all()
                
            time.sleep(5)
        

Control()
    