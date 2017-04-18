The Pi18650 Python script uses Python 2.7 to read the battery voltage on the Pi18650 HAT. 

This code is easily run from the command line using sudo python i2c_comms.py. It can be
added to other scripts, called from a class by importing the i2c_comms.py as a class in 
your other Python code. If you are adding the class to your own code, comment out the line "testpoll.set.."
and everything below so functions are called and returned to your code. To run standalone, these lines
must be uncommented.  

In order for this script to work, you must have installed Python, I2C enabled, Python SMBus. Here is a 
good tutorial but seems like it is for the earlier Pi's as the Blacklist is not used on the newer versions.

http://skpang.co.uk/blog/archives/575

Use the i2cdetect -y 0 or 1 to find which bus your Pi is using for the I2C communication. If it is not 1, 
then you will have to change the number for "DEVICE_BUS = 0" in the i2c_comms.py script and save. 

The i2c_comms.py script provides Battery Voltage, Chip Die Temperature (LTC2942) and a Battery Percent 
which can be modified to add more resolution in the readings. The battery capacity vs voltage is not exactly
linear but close enough to provide a good measurement on the status.  


