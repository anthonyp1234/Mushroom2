#!/usr/bin/env python2.7  
import sys
import re
import time
import datetime

from measurementClass import *
from thresholdsClass import *
from relaysClass import *
from db_class import *
import RPi.GPIO as GPIO

import Adafruit_DHT

###Import GPI Library
# sudo apt-get install python-dev python-rpi.gpio

###SETUP GPIO
GPIO.setmode(GPIO.BCM)

HEAT_RELAY_PIN =  18
HUMIDITY_RELAY_PIN = 23
AIR_RELAY_PIN = 24


sensors_pins = [27,22] #used to specify nubmer of sensors and what pin they are. Should equal the number of temp, and should equal number of hum class



#humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 27)
#print "Hum: {0}. Temp {1}".format(humidity, temperature)

GPIO.setup(HEAT_RELAY_PIN, GPIO.OUT)
GPIO.setup(HUMIDITY_RELAY_PIN, GPIO.OUT)
GPIO.setup(AIR_RELAY_PIN, GPIO.OUT)


#for pin in sensors_pins:
#  GPIO.setup(pin, GPIO.IN)

  
#GPIO.output(HEAT_RELAY_PIN, GPIO.LOW)
#GPIO.output(HUMIDITY_RELAY_PIN, GPIO.LOW)
#GPIO.output(AIR_RELAY_PIN, GPIO.LOW)

###
#SETUP RELAY
heat_relay = relay("Heat",HEAT_RELAY_PIN)
humidity_relay = relay("Humidity",HUMIDITY_RELAY_PIN)
air_relay = relay("Air",AIR_RELAY_PIN)

MEASUREMENT_TIME = 10 #time in seconds between measurement
RELAY_TIME = 60 # time in seconds between triggering relay

##### Create th DB
DATABASE_SIZE = 113568   # 1 DAY worth of 
mushroom_db = database("db.mushroom.sqlite3", DATABASE_SIZE)

#import Adafruit_DHT
#import this library and buld it:
#https://github.com/adafruit/Adafruit_Python_DHT.git
#git clone https://github.com/adafruit/Adafruit_Python_DHT.git
# apt-get update
# sudo apt-get install build-essential python-dev
#python setup.py build
# import dhtreader


MEASUREMENT_ARRAY_SIZE = 10000  # MEASUREMENT_ARRAY_SIZE x MEASUREMENT_TIME /(60*60)  = time in hours of measurements


#####
##SET UP Temperature Measurements class
temp1 = temperature("Temp1",MEASUREMENT_ARRAY_SIZE) ## Name and size of the array. Set up temperature class1 
temp2 = temperature("Temp2",MEASUREMENT_ARRAY_SIZE) ## Name and size of the array. Set up temperature class2
temp_classes = [temp1,temp2]

#####
##SET UP Humidity Measurements class
hum1 = humidity("Hum1",MEASUREMENT_ARRAY_SIZE) ## Name and size of the array. Set up temperature class1 
hum2 = humidity("Hum2",MEASUREMENT_ARRAY_SIZE) ## Name and size of the array. Set up temperature class2
hum_classes = [hum1,hum2]

###########################
##SET UP Thresholds#########
temperature_threshold = measurementThreshold("Temperature_threshold", 22, 2, 2, MEASUREMENT_ARRAY_SIZE,25)
humidity_threshold = measurementThreshold("Humidity Threshold", 82, 5, 2, MEASUREMENT_ARRAY_SIZE, 90)


#####
#Setup sensor
#sensor = Adafruit_DHT.DHT22

sensor_type = [Adafruit_DHT.AM2302, Adafruit_DHT.AM2302]




####
##Code for timing
measure_time = datetime.datetime.now()
relay_time = datetime.datetime.now()


#########################
##FOR LOOP STARTS HERE###
while True:

  if (datetime.datetime.now() - measure_time).total_seconds() > MEASUREMENT_TIME:
  
    ###CHECK TRiggers to see if anything has changed?
    #import pdb; pdb.set_trace()
    #Triggers is Tuple:   20.0, 80.0, 4000
    triggers =  mushroom_db.read_triggers()
    temperature_threshold.measurement_lower = triggers[0]
    humidity_threshold.measurement_lower = triggers[1]
    
    measure_time = datetime.datetime.now()
    #######################################
    ##Check here the Lastest Readings##
    for counter, pin in enumerate(sensors_pins):
      print "Sensor is: {0}.  Pin is {1} .  Counter is {2} ".format(sensor_type[counter], sensors_pins[counter], counter)
      #import pdb; pdb.set_trace()
      
      humidity, temperature = Adafruit_DHT.read_retry(sensor_type[counter], sensors_pins[counter])
      #import pdb; pdb.set_trace()
      print "Humidity is: {0}. Temperature is {1}.".format(str(humidity), str(temperature))
      print "In Try"
      if humidity is not None and temperature is not None:
        temp_classes[counter].add_temperature(temperature)
        hum_classes[counter].add_humidity(humidity)
      else:
        print 'Failed to get reading for Sensor {0}. Try again!'.format(counter)
  ##################################
  ##END READING SENSOR CODE
  #################################
  
    ###ADD Enter info into DB here:
    mushroom_db.addreadings(time.strftime("%Y:%m:%d:%H:%M:%S"),temp_classes[0].temperature_array[-1],temp_classes[1].temperature_array[-1],hum_classes[0].humidity_array[-1],hum_classes[1].humidity_array[-1],4000)

    


  ######################################
  ##Has Trigger Time passed#############
  if (datetime.datetime.now() - relay_time).total_seconds() > RELAY_TIME:
    relay_time = datetime.datetime.now()

    ####COMBIng THE ARRAYS AND SEND TO THRESHOLD CLASS
    temperature_arrays = []
    
    try:
      for classes in temp_classes:
        temperature_arrays.append(classes.temperature_array)   
      temperature_threshold.combine_measurements(temperature_arrays)
      
      ####COMBIng THE ARRAYS AND SEND TO THRESHOLD CLASS
      humidity_arrays = []
      for classes in hum_classes:
        humidity_arrays.append(classes.humidity_array)   
      humidity_threshold.combine_measurements(humidity_arrays)  
    except:
      print "No initial reading found, could not combine measurements"

    ###################################
    ##Check if I should trigger
    if temperature_threshold:
      if temperature_threshold.check_if_under:
        heat_relay.turn_on()
        air_relay.turn_on() # Here For checking only
        print "Temperature too low"
      else:
        heat_relay.turn_off()
        print "Temperature too high"  

    if humidity_threshold:       
      if humidity_threshold.check_if_under:
        humidity_relay.turn_on()
        print "humidity too low"
      else:
        humidity_relay.turn_off()
        print "humidity too high"
    
    ##DO air intake here:

    
    #addstates(self, time, tempavg, trelay, humavg, humrelay, c02avg,c02relay): 
    mushroom_db.addstates(time.strftime("%Y:%m:%d:%H:%M:%S"),temperature_threshold.averages[-1], int(heat_relay.state), humidity_threshold.averages[-1], int(humidity_relay.state), 4000,  int(air_relay.state))   















