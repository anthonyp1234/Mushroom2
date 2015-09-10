#!/usr/bin/env python2.7  
####Define Database being used
import datetime
import sqlite3
import os

class database:
  def __init__(self, name, size):
    self.filename = name
    self.size = size  # How many lines for the table to store data.
    
    if not os.path.exists(self.filename):
      print "db File not found, please run \n>python create_mushroom_db.py"
      exit(0)
    
    self.conn = sqlite3.connect(self.filename) ##open file when starting instance
  
  def addreadings(self, time, temp1, temp2, hum1, hum2,c02):
    #print '''INSERT INTO readings VALUES ("{0}",{1},{2}, {3}, {4}, {5})'''.format(time, temp1, temp2, hum1, hum2,c02)
    self.conn.execute('''INSERT INTO readings VALUES ("{0}",{1},{2}, {3}, {4}, {5})'''.format(time, temp1, temp2, hum1, hum2,c02))
    self.conn.commit() 
    
    triggers = self.conn.execute('SELECT * FROM readings')
    tablesize = len(triggers.fetchall())
    
    if tablesize >= 2* self.size: #remove when twice the size of max, so as to not do too many table deletes.
      self.conn.execute('''DELETE FROM readings WHERE NOT EXISTS in (SELECT id FROM readings ORDER BY id LIMIT self.size );''') ###Remove first line of table.
      conn.commit()

  def addstates(self, time, tempavg, trelay, humavg, humrelay, c02avg,c02relay):    
    self.conn.execute('''INSERT INTO states VALUES ("{0}",{1},{2}, {3}, {4}, {5}, {6})'''.format(time, tempavg, trelay, humavg, humrelay, c02avg,c02relay))
    self.conn.commit()  
    
    triggers = self.conn.execute('SELECT * FROM states')
    tablesize = len(triggers.fetchall())
    
    if tablesize >= 2* self.size: #remove when twice the size of max, so as to not do too many table deletes.
      self.conn.execute('''DELETE FROM states WHERE NOT EXISTS in (SELECT id FROM states ORDER BY id LIMIT self.size );''') ###Remove first line of table.
      conn.commit()    
    
  def read_triggers(self):
    triggers = self.conn.execute('''SELECT * FROM triggers''')    
    return triggers.fetchone()  ###returns tuple. just index the value. [temp,humidity,c02]
       
  def connection_close(self):
    self.conn.close()    
