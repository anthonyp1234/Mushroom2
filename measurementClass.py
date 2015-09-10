#!/usr/bin/env python2.7  

import datetime


class temperature:
  def __init__(self, name, max_size):
    self.name = name
    self.read_in_temperature = ""
    self.temperature_array = []
    self.temperate_time = []
    self.temperature = ""
    self.max_size = max_size


  def add_temperature(self, new_temp):
    ## ADD new temperature to the array
    if len(self.temperature_array) >= self.max_size:
      self.temperature_array.pop(0)
      self.temperate_time.pop(0)
    self.temperature_array.append(new_temp)
    self.temperate_time.append(datetime.datetime.now())


class humidity:
  def __init__(self, name, max_size):
    self.name = name
    self.read_in_humidity = ""
    self.humidity_array = []
    self.humidity_time = []
    self.humidity = ""
    self.max_size = max_size
    

  def add_humidity(self, new_humidity):
    ## ADD new temperature to the array
    if len(self.humidity_array) >= self.max_size:
      self.humidity_array.pop(0)
      self.humidity_time.pop(0)
    self.humidity_array.append(new_humidity)
    self.humidity_time.append(datetime.datetime.now())     


    