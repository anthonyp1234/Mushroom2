#!/usr/bin/env python2.7  

import datetime

##can be used for Temperature and Humidity Readings

class measurementThreshold:
  def __init__(self, name, measurement_lower, measurement_hysterysis, average_over, overall_averages_array_size, initial_temp):
    self.name = name
    self.measurement_lower = measurement_lower
    self.measurement_hysterysis = measurement_hysterysis
    self.average_over = average_over
    self.averages = [initial_temp]
    self.overall_averages = [initial_temp]
    self.overall_averages_time = []
    self.overall_averages_array_size = overall_averages_array_size
    self.overall_average = "initial_temp"

##############################
##Function to Get all the temps, and average everything
    
  def combine_measurements(self, lists): # where lists is a list of lists 
    for measurement_array in lists:
    
      if len(measurement_array) >= self.average_over:
        average = sum(measurement_array[len(measurement_array)-self.average_over:])
        average = average / self.average_over
        self.averages.append(average)
      else:
        average = sum(measurement_array) / len(measurement_array)
        self.averages.append(self.average)

    self.overall_average = sum(self.averages) / len(self.averages)
        
    if len(self.overall_averages) >= self.overall_averages_array_size:
      self.overall_average.pop(0)
      self.overall_averages_time.pop(0)
    self.overall_averages.append(average)
    self.overall_averages_time.append(datetime.datetime.now())
      


########################
##Check if temperature of averages is lower than the temperature to trigger minus the hysterisis    
  def check_if_under(self):
    if (self.measurement_lower - self.measurement_hysterysis) > self.overall_average:
      return True
    else:
      return False
      
    
    
    
    
