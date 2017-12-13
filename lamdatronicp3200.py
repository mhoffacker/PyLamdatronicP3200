##@package lamdatronicp3200.py
#ModBUS interface to Froeling Lamdatronic P3200 touch
#
#Provides a wrapper arround minimalmodbus and the serial port for
#accessing the Froeling Lamdatronic P3200 touch via ModBUS RTU or ASCII
#
#Warning: Wrong settings may lead to damage of the component or can
#cause harm to people. This class does not contain any critical commands
#
# Changelog:
# Date  		Change
# 2017-10-01	First version

import minimalmodbus
import serial

__author__ = "Michael Hoffacker"
__copyright__ = "Copyright 2017, Michael Hoffacker"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Michael Hoffacker"
__email__ = "michael@hoffacker.bayern"
__status__ = "Alpha"

##Main class
#
#Main class for access to Lamdatronic P3200
class LamdatronicP3200Touch:

	##The constructor
	#@param port UART port for access
	#@param ModBusID ID set on Lamdatronic P3200 Touch
	#@param mode Set to string RTU or ASCII
	def __init__(self, port, ModBusID, mode):
		self.ModBusID = ModBusID
		if mode == "RTU":
			self.mode = minimalmodbus.MODE_RTU
		elif mode == "ASCII":
			self.mode = minimalmodbus.MODE_ASCII
		self.port = port
		self.debug = False
	
	##Enable debug messages
	#@param debug Enable (True) or disable (False) minimalmodbus debug messages
	def show_debug(self, debug):
		self.debug = debug
		self.instrument.debug = debug;
	
	##Connects minimalmodbus
	def connect(self):
		minimalmodbus.BAUDRATE = 57600
		minimalmodbus.PARITY = serial.PARITY_NONE
		minimalmodbus.STOPBITS = serial.STOPBITS_ONE
		minimalmodbus.BYTESIZE = serial.EIGHTBITS
		minimalmodbus.TIMEOUT = 1
		self.instrument = minimalmodbus.Instrument(self.port, self.ModBusID, self.mode)
		self.instrument.debug = self.debug;
		
	##Read the outside temperature
	#@return temperature as float
	def get_outside_temperatur(self):
		return self.instrument.read_register(1000, numberOfDecimals=0, functioncode=4, signed=True)/2.0
	
	##Reads the current preflow temperature of given heating circuit
	#@param hk Number of heating circuit (1...18)
	#@return returns the current temperatur or -1 in case of failure
	def get_preflow_temperatur_current(self, hk):
		if 1 <= hk <= 18:
			return self.instrument.read_register(1000 + hk*30, numberOfDecimals=0, functioncode=4, signed=False)/2.0 
		else:
			return -1;		

	##Reads the set preflow temperature of given heating circuit
	#@param hk Number of heating circuit (1...18)
	#@return returns the setpoint of temperatur or -1 in case of failure			
	def get_preflow_temperatur_set(self, hk):
		if 1 <= hk <= 18:
			return self.instrument.read_register(1001 + hk*30, numberOfDecimals=0, functioncode=4, signed=False)/2.0 
		else:
			return -1;
	
	##Set the preflow temperature
	#This sets the preflow temperature of a given heating circuit. 
	#After 2 minutes without a further ModBus command, the Lamdatronic
	#switches back to the internal heating curve
	#@param hk heating circuit
	#@param temp setpoint of temperature
	#@param t_max Maximum allowed temperature, as an additional precaution
	#@param t_min Minimum allowed temperature, as an additional precaution
	#@return True on success, False on failure
	def set_preflow_temperature(self, hk, temp, t_max, t_min):
		if t_min <= temp <= t_max:
			self.instrument.write_register(8000+(hk-1), temp*2, numberOfDecimals=0, functioncode=6, signed=False)
			return True
		else:
			return False
	
	##Releases/Disables the heating circuit
	#Turns on/off the pump for the heating circuit
	#@param hk Number of heating circuit
	#@param release Turn on (True) or off (False) the pump
	def release_heating_circuit(self, hk, release):
		if release:
			self.instrument.write_register(8028+(hk-1), 1, numberOfDecimals=0, functioncode=6, signed=False)
		else:
			self.instrument.write_register(8028+(hk-1), 0, numberOfDecimals=0, functioncode=6, signed=False)
		
