import sqlite3
import sys
import os.path

print "Used to create Mushroom DB, default filename is 'db.mushroom.sqlite3'"



filename = 'db.mushroom.sqlite3'

if os.path.exists(filename):
  print "Found existing file!!!"
  s = raw_input('This WILL DELETE EXISTING DB, type "YES" to continue: ')
  if s == "YES":
    print "Deleting File"
    os.remove(filename)
  else:
    print "\nFile left unchanged, exiting\n"
    sys.exit(0)


conn = sqlite3.connect(filename)


curs = conn.cursor()

print "Creating Time, Temp1, temp2, hum1, hum2, C02  table"
# Create table
curs.execute('''CREATE TABLE readings
             (date text, temp1 real, temp2 real, hum1 real, hum2 real, c02 integer)''')

curs.execute('''CREATE TABLE triggers
             (temp real, hum real, c02 integer)''')
         
curs.execute('''CREATE TABLE states
             (date text, temp real, trelay real,  hum real, hrelay real, c02 integer, c02relay real)''')             
             
##### creat initial trigger values
curs.execute('''INSERT INTO triggers VALUES ('20', '80', '4000')''')

             
conn.commit()             
             
print "\n\nDatabase created, and contains:\n\n"

for line in conn.iterdump():
  print line

conn.close()