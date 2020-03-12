# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:27:51 2020

@author: mberutti
"""

import time

from gpiozero import LED

from smarttoilet.signals import SignalIn, SignalOut
from smarttoilet.data import Data, Broadcast

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
        self.data_led = LED(37)
        self.error = LED(40)
        
        # camera
        self.camera = None
        
        # other system settings
        self.pump_runtime = 1.0
        self.num_images = 1000
        self.rest_time = 0.25
        self.samps_after_sensor_off = 30
        
        self.peer_ip = None
        self.data_path = "results"
        
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
        # turn off all indicator lights
        self._stop_all()
        
        # run, but catch exceptions and abort if necessary
        try:
            # setup
            self.analysis_led[1].blink
            ims_left = self.num_images
            fluid_left = True
            
            data_session = Data(self.data_path)
            
            # run motor & imaging
            while self.power.update() and ims_left > 1:
                # run pump
                self.motor.run(self.pump_runtime)
                
                if not self.power.update():
                    break
                
                # image
                time.sleep(self.rest_time)
                self.cam_led.on
                '''CAPTURE IMAGE'''
                data_session.fetch_data()
                self.cam_led.off
                
                # subtract from remaining images every cycle
                # if the fluid sensor turns off, set remaining
                # images to the maximum possible remaining
                ims_left -= 1
                if fluid_left and \
                        not self.fluid.update() and \
                        ims_left > self.samps_after_sensor_off:
                    fluid_left = False
                    ims_left = self.samps_after_sensor_off
                    
            # change indicator lights, given complete or power off
            if ims_left == 0:
                # set analysis to green
                self.analysis_led[1].off
                self.analysis_led[0].on
            else:
                # set analysis to solid red
                self.analysis_led[1].on
            
            # transmit data whether or not power switched off
            self.data_led.blink
            data = data_session.prepare_broadcast()
            broadcast_session = Broadcast(self.peer_ip)
            broadcast_session.broadcast_data(data)
            self.data_led.off
                
        except:
            # turn on error indicator and turn off all else
            # do not transmit data
            self._stop_all()
            self.error.on
        
    def run(self):
        """ Automation system
        """        
        # run continuously after initialization
        while True:
            # run analysis if power switch is on, there is fluid in the
            # system, and there isn't a prevailing error
            # keep indicator lights on until new run or power off
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
    