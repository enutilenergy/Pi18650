import smbus
import time
from smbus import SMBus	


DEVICE_BUS = 1 #device bus number
DEVICE_ADDR = 0x64

#Fuel Gas Guage Monitor Registers
FUELGUAGE_ADDR = 0x64		#0b01100100
FUELGUAGE_REG_ADDR_00 = 0X00	#status				(R) default()
FUELGUAGE_REG_ADDR_01 = 0X01	#control	 		(R/W) default(3C)
FUELGUAGE_REG_ADDR_02 = 0X02	#acc charge MSB 		(R/W) default(7F)
FUELGUAGE_REG_ADDR_03 = 0X03	#acc charte LSB 		(R/W) default(FF)
FUELGUAGE_REG_ADDR_04 = 0X04	#charge threshold high MSB 	(R/W) default(FF)
FUELGUAGE_REG_ADDR_05 = 0X05	#charge threshold high LSB 	(R/W) default(FF)
FUELGUAGE_REG_ADDR_06 = 0X06	#charge threshold low MSB 	(R/W) default(00)
FUELGUAGE_REG_ADDR_07 = 0X07	#charge threshold low LSB 	(R/W) default(00)
FUELGUAGE_REG_ADDR_08 = 0x08	#voltage MSB 			(R) default(XX) unknown
FUELGUAGE_REG_ADDR_09 = 0x09	#voltage LSB 			(R) default(XX)
FUELGUAGE_REG_ADDR_0A = 0X0A	#voltage threshold high 	(R/W) default(FF)
FUELGUAGE_REG_ADDR_0B = 0X0B	#voltage threshold low 		(R/W) default(00)
FUELGUAGE_REG_ADDR_0C = 0X0C	#temperature MSB 		(R) default(XX)
FUELGUAGE_REG_ADDR_0D = 0X0D	#temperature LSB 		(R) default(XX)
FUELGUAGE_REG_ADDR_0E = 0X0E	#temperature threshold high 	(R/W) default(FF)
FUELGUAGE_REG_ADDR_0F = 0X0F	#temperature threshold low 	(R/W) default(00)


bus = smbus.SMBus(DEVICE_BUS)

class i2cCommand:

	def __init__(self):

		global bus
		global DEVICE_ADDR
		global FUELGUAGE_ADDR
		global DEVICE_REG_ADDR_ID
		global DEVICE_REG_ADDR_08
		global DEVICE_REG_ADDR_09
		global DEVICE_REG_ADDR_0A
		global DEVICE_REG_ADDR_45

		global FUELGUAGE_REG_ADDR_00 #= 0X00 #(reg name A)
		global FUELGUAGE_REG_ADDR_01 #= 0X01 #(reg name B)
		global FUELGUAGE_REG_ADDR_02 #= 0X02 #(reg name C)
		global FUELGUAGE_REG_ADDR_03 #= 0X03 #(reg name D)
		global FUELGUAGE_REG_ADDR_04 #= 0X04 #(reg name E)
		global FUELGUAGE_REG_ADDR_05 #= 0X05 #(reg name F)
		global FUELGUAGE_REG_ADDR_06 #= 0X06 #(reg name G)
		global FUELGUAGE_REG_ADDR_07 #= 0X07 #(reg name H)
		global FUELGUAGE_REG_ADDR_08 #= 0X08 #(reg name I)
		global FUELGUAGE_REG_ADDR_09 #= 0X09 #(reg name J)
		global FUELGUAGE_REG_ADDR_0A #= 0X0A #(reg name K)
		global FUELGUAGE_REG_ADDR_0B #= 0X0B #(reg name L)
		global FUELGUAGE_REG_ADDR_0C #= 0X0C #(reg name M)
		global FUELGUAGE_REG_ADDR_0D #= 0X0D #(reg name N)
		global FUELGUAGE_REG_ADDR_0E #= 0X0E #(reg name O)
		global FUELGUAGE_REG_ADDR_0F #= 0X0F #(reg name P)

		#return init_value

	
	def soft_shutdown(self):
		try:
			os.system('sudo shutdown -h now')
			###print 'SHUTTING DOWN THE Os SYSTEM NOW*******************************!!!!'
		except:
			print 'Exception in soft shutdown------------------>>>>>'
			
			

	def 	set_fuelguage_control_reg(self, adc_mode_bit7_6, prescaler_bit5_3, al_cc_bit2_1, shutdown_bit0):

		#set bit7_6-11 (0xC0) for auto mode temp and volt convertion every 1 second
		#bit7_6-10 (0x80) for manual volt mode
		#bit7_6-01 (0x40) for manual temp mode
		#bit7_6-00 (0x00) for sleep mode

		#leave bit5_3-111 for prescaler default 128
		#equation 2^(4*B5 + 2*B4 + B3) ie. 2^(4*1 + 2*1 + 1) = 2^7 = 128

		#leave bit2_1-10 for output alert mode (can connect to pin on rasp pi compute module


		#leave bit0-0 as the 3V3 power will be turned off by user, but current drain will not be monitored when 3V3 off

		#hardcode for now	
		adc_mode_bit7_6 = 0xC0
		prescaler_bit5_3 = 0x38
		al_cc_bit2_1 = 0x04
		shutdown_bit0 = 0x00
		

		value = adc_mode_bit7_6 | prescaler_bit5_3 | al_cc_bit2_1 | shutdown_bit0

		print "set_fuel_gauage_control_reg value: ", hex(value)

		bus.write_byte_data(FUELGUAGE_ADDR, FUELGUAGE_REG_ADDR_01, value)

		'''
		print "checking fuel_gauage_control_reg value: "
		
		(device_str_ctrl) = bus.read_byte_data(FUELGUAGE_ADDR, FUELGUAGE_REG_ADDR_01)

		print "ctrl reg: ", hex(device_str_ctrl)	
		'''

		time.sleep(0.1)	

		return 0

	def 	fuelguage_check_volt(self):

		#voltage is 14bit (reg's I and J) and temperature 10bit (reg's M and N)resolution 
		#convert I and J to 16bit variable, then (value / 65535) x 6V = Voltage 

		#read registers I and J (8 and 9 sequentially)
		voltage_msb = float(0.0)
		voltage_lsb = float(0.0)
		temp_msb = float(0.0)
		temp_lsb = float(0.0)		


		voltage_msb = SMBus(1).read_byte_data(DEVICE_ADDR, FUELGUAGE_REG_ADDR_08)
		voltage_lsb = SMBus(1).read_byte_data(DEVICE_ADDR, FUELGUAGE_REG_ADDR_09)
		#print "voltage_msb: ", voltage_msb
		#print "voltage_lsb: ", voltage_lsb

		temp_msb = SMBus(1).read_byte_data(DEVICE_ADDR, FUELGUAGE_REG_ADDR_0C)
		temp_lsb = SMBus(1).read_byte_data(DEVICE_ADDR, FUELGUAGE_REG_ADDR_0D)
		#print "temp_msb: ", temp_msb
		#print "temp_lsb: ", temp_lsb
		

		voltage_16bit = float(0.0)
		voltage_msb = voltage_msb << 8
		#print "voltage_msb: ", hex(voltage_msb)
		#print "voltage_lsb: ", hex(voltage_lsb)
		
		voltage_16bit = float(voltage_msb | voltage_lsb)		
		#print "voltage_16bit: ", voltage_16bit


		#voltage at battery
		battery_volt = float(0.0)
		divisor = float(65535.0)
		multiplier = float(6.0)
		battery_volt = ( voltage_16bit / divisor ) * multiplier		

		print "battery_volt: ", battery_volt

		battery_capacity_percent = 0
		

		#battery capacity reference table
		if battery_volt >= 4.20:
			battery_capacity_percent = 100

		elif  battery_volt < 4.20 and battery_volt >= 4.15:
			battery_capacity_percent = 98

		elif  battery_volt < 4.15 and battery_volt >= 4.10:
			battery_capacity_percent = 95

		elif  battery_volt < 4.10 and battery_volt >= 4.00:
			battery_capacity_percent = 85

		elif  battery_volt < 4.00 and battery_volt >= 3.95:
			battery_capacity_percent = 75

		elif  battery_volt < 3.95 and battery_volt >= 3.90:
			battery_capacity_percent = 65

		elif  battery_volt < 3.90 and battery_volt >= 3.85:
			battery_capacity_percent = 55

		elif  battery_volt < 3.85 and battery_volt >= 3.80:
			battery_capacity_percent = 50

		elif  battery_volt < 3.80 and battery_volt >= 3.75:
			battery_capacity_percent = 48

		elif  battery_volt < 3.75 and battery_volt >= 3.70:
			battery_capacity_percent = 44

		elif  battery_volt < 3.70 and battery_volt >= 3.65:
			battery_capacity_percent = 38

		elif  battery_volt < 3.65 and battery_volt >= 3.60:
			battery_capacity_percent = 36

		elif  battery_volt < 3.60 and battery_volt >= 3.55:
			battery_capacity_percent = 34

		elif  battery_volt < 3.55 and battery_volt >= 3.50:
			battery_capacity_percent = 31

		elif  battery_volt < 3.50 and battery_volt >= 3.45:
			battery_capacity_percent = 29

		elif  battery_volt < 3.45 and battery_volt >= 3.40:
			battery_capacity_percent = 26

		elif  battery_volt < 3.40 and battery_volt >= 3.35:
			battery_capacity_percent = 24

		elif  battery_volt < 3.35 and battery_volt >= 3.30:
			battery_capacity_percent = 23

		elif  battery_volt < 3.30 and battery_volt >= 3.25:
			battery_capacity_percent = 21

		elif  battery_volt < 3.25 and battery_volt >= 3.20:
			battery_capacity_percent = 18

		elif  battery_volt < 3.20 and battery_volt >= 3.15:
			battery_capacity_percent = 16

		elif  battery_volt < 3.15 and battery_volt >= 3.10:
			battery_capacity_percent = 15

		elif  battery_volt < 3.10 and battery_volt >= 3.05:
			battery_capacity_percent = 11

		elif  battery_volt < 3.05 and battery_volt >= 3.00:
			battery_capacity_percent = 10
		else:
		      battery_capacity_percent = 0
		

		print "battery_capacity_percent: ", battery_capacity_percent


		#temperature conversion to celcius ------------------------------------------------

		#print "temp_msb: ", temp_msb

		#print "temp_lsb: ", temp_lsb

		temperature_16bit = float(0.0)
		temp_msb = temp_msb << 8

		#print "temp_msb: ", hex(temp_msb)

		temperature_16bit = float(temp_msb | temp_lsb)	

		#print "temperature_16bit: ", temperature_16bit

		#voltage at battery
		temperature_kelvin = float(0.0)
		temperature_multiplier = float(600.0)
		temperature_kelvin = ( temperature_16bit / divisor ) * temperature_multiplier	

		print "temperature_kelvin: ", temperature_kelvin

		temperature_celcius = float(0.0)

		temperature_celcius = temperature_kelvin - 273.0

		print "temperature_celcius: ", temperature_celcius

		

		return battery_capacity_percent, temperature_celcius, battery_volt




		


testpoll = i2cCommand()
 
testpoll.set_fuelguage_control_reg(0xC0, 0x80, 0x10, 0x00)

while 1:
	print "-------------------------------------------------------------------------"
	battery_temperature = testpoll.fuelguage_check_volt()
	battery_capacity, fuel_guage_temperature, battery_voltage = battery_temperature
	#print "Battery Capacity Percent: ", battery_capacity
	#print "Fuel Guage Temperature: ", fuel_guage_temperature
	#print "Battery Voltage: ", battery_voltage
	time.sleep(1.5)
	print "-------------------------------------------------------------------------"


		 	
