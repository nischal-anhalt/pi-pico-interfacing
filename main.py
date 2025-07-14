from mq2 import MQ2
from collections import deque
import utime
from stepper import StepperMotor
from micropython import const

MQ2_PIN_READ = const(26)
LPG_SAFETY_THRESHOLD = const(12)
SAMPLE_LENGTH = const(10)

# initialize stepper motor and sensor classes
stepper_motor = StepperMotor()
sensor = MQ2(pinData = MQ2_PIN_READ, baseVoltage = 3.3)
# calibrate the gas sensor
print(f"Measuring Strategy: {sensor.measuringStrategy}")
print("Calibrating")
sensor.calibrate()
print("Calibration completed")
print("Base resistance:{0}".format(sensor._ro))


lpg_readings = deque([], SAMPLE_LENGTH)
isValveOpen = False 

def gas_readings():
	return sensor.readSmoke(), sensor.readLPG(), sensor.readMethane(), sensor.readHydrogen()

def average_reading(readings):
	sum = 0
	for item in readings:
		sum += item
	return sum / len(readings)

print("Starting Measurement...")
print('lpg_reading, moving_average')
while True:
	smoke_reading, lpg_reading, methane_reading, hydrogen_reading = gas_readings()
	
	lpg_readings.append(lpg_reading)
	if len(lpg_readings) >= SAMPLE_LENGTH:
		average_lpg_reading = average_reading(lpg_readings)
		# turn the motor by 180 degrees --- right if unsafe levels --- left if safe
		if average_lpg_reading > LPG_SAFETY_THRESHOLD and not isValveOpen:  #unsafe level
			print("Valve opened =======================")
			stepper_motor.rotate_to_angle(180, -1)
			isValveOpen = True
		elif average_lpg_reading < LPG_SAFETY_THRESHOLD and isValveOpen: #safe level
			print("Valve closed =======================")
			stepper_motor.rotate_to_angle(180, 1)
			isValveOpen = False
		# print average lpg levels from last 10 readings
		print(f"Average lpg levels from last 10 reads {average_lpg_reading}")

	
    # print out readings in console
	# print("Smoke: {:.1f}".format(smoke_reading)+" - ", end="")
	# print("LPG: {:.1f}".format(lpg_reading)+" - ", end="")
	# print("Methane: {:.1f}".format(methane_reading)+" - ", end="")
	# print("Hydrogen: {:.1f}".format(hydrogen_reading))
	utime.sleep(0.5)
	

