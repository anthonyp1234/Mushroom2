#!/usr/bin/env python2.7  

import RPi.GPIO as GPIO


class relay:
  def __init__(self, name, pin):
    self.name = name
    self.pin = pin
    self.state = False
  

  def turn_on(self):
    if not self.state: 
      self.state = True
      GPIO.output(self.pin, GPIO.HIGH)
    
  def turn_off(self):
    if self.state: 
      self.state = False
      GPIO.output(self.pin, GPIO.LOW)  
    
    
