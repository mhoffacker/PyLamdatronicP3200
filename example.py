#!/usr/bin/python

from lamdatronicp3200 import LamdatronicP3200Touch

#Connect on /dev/ttyUSB0, id=2 with ModBus RTU
p = LamdatronicP3200Touch(port='/dev/ttyUSB0', ModBusID=2, mode='RTU')

#Connect
p.connect()

#Disable debug messages
p.show_debug(False)

#Display current outside temperature
print("Outside temperature: "+str(p.get_outside_temperatur()))


