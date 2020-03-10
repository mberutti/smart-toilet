# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:05:33 2020

@author: mberutti
"""

from gpiozero import Button, LED

class SignalIn:
    """ Class to manage GPIO input signals (buttons)
    """
    def __init__(self, pin, **kwargs):
        self.signal = Button(pin)
        
        self.led_t = None
        self.led_f = None
        if "led" in kwargs.keys():
            paired_pins = kwargs["led"]
            if isinstance(paired_pins, int):
                self.led_t = LED(paired_pins)
            elif isinstance(paired_pins, tuple):
                self.led_t = LED(paired_pins[0])
                self.led_f = LED(paired_pins[1])
            else:
                raise ValueError("Incorrect value for 'pairedled' kwarg: {}"
                                 .format(paired_pins))
                
    def __exit__(self):
        """ Turn off LEDs when exiting
        """
        if self.led_t is not None:
            self.led_t.off
        if self.led_f is not None:
            self.led_f.off
            
    def update(self):
        """ Adjusts LEDS if applicable and returns signal state
        """
        if self.signal.is_pressed:
            if self.led_t is not None:
                self.led_t.on
            if self.led_f is not None:
                self.led_f.off        
    
            return True
        
        else:
            if self.led_t is not None:
                self.led_t.off
            if self.led_f is not None:
                self.led_f.blink
                
            return False
        

class SignalOut:
    """ Class to manage GPIO output signals (motors)
    """
    def __init__(self, pin, **kwargs):
        pass
