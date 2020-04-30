# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 19:47:04 2020

@author: mberutti
"""

from control import Control

# Set these values according to experimental values
# Volume in mL capture in each image
ml_per_image = 0.01
# Volume desired to be captured
ml_total = 2.0
# Volume required in reservoir to actuate urine sensor
ml_to_trigger_sensor = 10 
# Number of images taken inbetween running pump
images_per_step = 3
# Pump runtime per step
pump_runtime = 0.1
# Pump volumetric flow
pump_q = 0.5
# Rest time after running pump
rest_time = 0.1

# Total images and steps will be calculated as follows:
# total_images = ml_total / ml_per_image
# total_steps = total_images / images_per_step
# samps_after_sensor_off = ml_to_trigger_sensor / (pump_q * pump_runtime)

# Connect the following components to the GPIO pins listed below:
#
# PIN | Component            | Schematic Location
#   7 | Power Switch         | Port 1
#  11 | Fluid Sensor         | Port 2
#  12 | Fluid Indicator      | Switch 3
#  13 | Force Wash Button    | Switch 4
#  15 | Pump Control         | Switch 6
#  16 | Wash Valve Control   | Port 3
#  29 | Wash Cycle Indicator | Switch 7
#  31 | Camera Indicator     | Switch 8
#  32 | Analysis Indicator G | Switch 9
#  33 | Analysis Indicator R | Switch 10
#  35 | Data Indicator       | Switch 11
#  36 | Error Indicator      | Switch 12

Control(ml_per_image=ml_per_image,
        ml_total=ml_total,
        ml_to_trigger_sensor=ml_to_trigger_sensor,
        images_per_step=images_per_step,
        pump_runtime=pump_runtime,
        pump_q=pump_q,
        rest_time=rest_time)


