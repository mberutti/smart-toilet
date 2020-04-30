# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 19:10:55 2020

@author: mberutti
"""

class LED:
    def __init__(self, *args, **kwargs):
        self.on = 'on'
        self.off = 'off'
        self.blink = 'blink'
        self.is_active = False
        
class Button:
    def __init__(self, *args, **kwargs):
        self.is_pressed = True
    