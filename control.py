# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:27:51 2020

@author: mberutti
"""

import time

# from gpiozero import LED
from led_test import LED

from signals import SignalIn, SignalOut
from data import Data, Broadcast
from camera import Camera

class Control:
    """ Class for controlling entire system
    """
    def __init__(self,
                 ml_per_image,
                 ml_total,
                 ml_to_trigger_sensor,
                 images_per_step,
                 pump_runtime,
                 pump_q,
                 rest_time):
        
        # input signals
        self.power = SignalIn(7)
        self.fluid = SignalIn(11, led=12)
        self.force_wash = SignalIn(13)
        
        # output signals
        self.motor = SignalOut(15)
        self.wash = SignalOut(16)
        
        # other indicators
        self.wash_led = LED(29)
        self.cam_led = LED(31)
        self.analysis_led = (LED(32), LED(33))
        self.data_led = LED(35)
        self.error = LED(36)
        
        # camera
        self.camera = Camera()
        
        # other system settings
        self.pump_runtime = pump_runtime
        self.num_images = ml_total / ml_per_image
        self.rest_time = rest_time
        self.samps_after_sensor_off = ml_to_trigger_sensor / \
                                      (pump_q * pump_runtime)
        
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
        self.motor.stop()
        self.wash.stop()
        
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
            while self.power.update() and ims_left > 0:
                # run pump
                self.motor.run(self.pump_runtime)
                
                if not self.power.update():
                    break
                
                # image
                time.sleep(self.rest_time)
                self.cam_led.on
                self.camera.capture()
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
    