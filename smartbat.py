#!/usr/bin/env python

import io
import fcntl
import struct
import time

I2C_SLAVE=0x0703

class i2c:

   def __init__(self, device, bus):

      self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
      self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

      # set device address

      fcntl.ioctl(self.fr, I2C_SLAVE, device)
      fcntl.ioctl(self.fw, I2C_SLAVE, device)

   def write(self, bytes):
      self.fw.write(bytes)

   def read(self, bytes):
      return self.fr.read(bytes)

   def close(self):
      self.fw.close()
      self.fr.close()

   def get_int(self, var_slice):
       
      ms = memoryview(var_slice)
      var_list = map(ord,ms)
      #print("bat_list: ", bat_list)
      var_int = var_list[0]*256 + var_list[1]
      
      return var_int



testpoll = i2c(0x48,1)
samples = 10
bat_avg = 0
hum_avg = 0
temp_avg = 0
sample_delay = 0.010

for i in range(samples):
      result = testpoll.read(10)
      print("result: ", result)

      bat = result[:2]
      hum = result[2:4]
      temp = result[4:6]
      temp1 = result[6:8]
      temp2 = result[-2:]

      for j in range(3):
          if j == 0:
             res = testpoll.get_int(bat)
             bat_avg = bat_avg + res

          if j == 1:
             res1 = testpoll.get_int(hum)
             hum_avg  = hum_avg + res1

          if j == 2:
             res2 = testpoll.get_int(temp)
             temp_avg  = temp_avg + res2

      result = '0'
      res = 0
      res1 = 0
      res2 = 0
      time.sleep(sample_delay)

#m = memoryview(bat)
#bat_list = map(ord,m)
#print("bat_list: ", bat_list)

#Battery Level calculation---------------
#bat_int = bat_list[0]*256 + bat_list[1]
#print("bat_int: ", bat_int)

bat_avg_int = bat_avg / samples
battery = (float(bat_avg_int) * 0.00322) / 0.7674
print "Battery: ", battery ,"V"
#----------------------------------------

#m1 = memoryview(hum)
#hum_list = map(ord,m1)
#print("hum_list: ", hum_list)

#Humidity calculation--------------------
#hum_int = hum_list[0]*256 + hum_list[1]
#print("hum_int: ", hum_int)

humidity = 0.0
hum_avg_int = hum_avg / samples
humidity = float(-12.5) + (float(125) * (float(hum_avg_int) / float(1024)))
humidity  = round(humidity,2)
print "Humidity: ", humidity ,"%"
#----------------------------------------

#m2 = memoryview(temp)
#temp_list = map(ord,m2)
#print("temp_list: ", temp_list)

#Temperature calculation - Deg C-----------
#temp_int = temp_list[0]*256 + temp_list[1]
#print("temp_int: ", temp_int)

temperature = 0.0
temp_avg_int = temp_avg / samples
temperature = float(-66.875) + (float(218.75) * (float(temp_avg_int) / float(1024)))
temperature = round(temperature,2)
print "Temperature: ", temperature ,"C"
#-----------------------------------------

#Temperature calculation - Deg F-----------
#temp_int = temp_list[0]*256 + temp_list[1]
#print("temp_int: ", temp_int)

temperatureF = 0.0
temp_avg_int = temp_avg / samples
temperatureF = float(-88.375) + (float(393.75) * (float(temp_avg_int) / float(1024)))
temperatureF = round(temperatureF,2)
print"Temperature: ", temperatureF ,"F"
#-----------------------------------------

#dev.write("\x2D\x00") # POWER_CTL reset

testpoll.close()
