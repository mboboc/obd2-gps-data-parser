'''
ENGINE_LOAD
COOLANT_TEMP
FUEL_PRESSURE
INTAKE_PRESSUDE
RPM
SPEED
INTAKE_TEMP
MAF
THROTTLE_POS
FUEL_LEVEL
OIL_TEMP
FUEL_RATE
'''
import obd
from time import sleep

sensors = ["ENGINE_LOAD","COOLANT_TEMP","FUEL_PRESSURE","INTAKE_PRESSURE","RPM","SPEED","INTAKE_TEMP","MAF","THROTTLE_POS","FUEL_LEVEL","OIL_TEMP","FUEL_RATE"]

connection = obd.Async("/dev/ttyUSB0")

for sensor in sensors:
  connection.watch(obd.commands[sensor])

connection.start()

reading = 0
while True:
  print("\n<<<", reading)
  #print(connection.query(obd.commands.THROTTLE_POS))
  for sensor in sensors:
    print(sensor.ljust(24), connection.query(obd.commands[sensor]))
  print(">>>\n")
  reading += 1
  sleep(0.5)