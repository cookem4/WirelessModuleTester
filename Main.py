from Cleanflight_MSP import Cleanflight_MSP
from EStop import EStop
import time

ARM = 1600; DISARM = 1000; ANGLE_MODE = 1600; NEUTRAL = 1000;
ZERO_ROLL = 1500; ZERO_PITCH = 1500; ZERO_YAW_RATE = 1500; ZERO_THROTTLE = 1000;
zeroCommands = [ZERO_ROLL, ZERO_PITCH, ZERO_THROTTLE, ZERO_YAW_RATE, ARM, ANGLE_MODE, NEUTRAL, NEUTRAL]
HZ=100
disArmCommandsToGoMSP = [ZERO_ROLL, ZERO_PITCH, ZERO_THROTTLE, ZERO_YAW_RATE, DISARM, ANGLE_MODE, NEUTRAL, NEUTRAL] # The 1600 is to enable the "Angle Mode" in clean flight.
armCommandsToGoMSP    = [ZERO_ROLL, ZERO_PITCH, ZERO_THROTTLE, ZERO_YAW_RATE,    ARM, ANGLE_MODE, NEUTRAL, NEUTRAL]
dataLength = len(disArmCommandsToGoMSP)
dataBytes = 2*dataLength
direction = '<'
h = 'h'

cleanflightMSP0 = Cleanflight_MSP('/dev/ttyUSB1', 115200)
EStop_failsafe = EStop('/dev/ttyUSB0', 115200)

print("Arming...")
for i in range(1, 50):  #command for about a second before arming
    eval('cleanflightMSP0.sendMSP(direction, dataBytes, 200, disArmCommandsToGoMSP, direction+ str(dataLength) + h)')
    time.sleep(1/HZ)
for i in range(1, 50):
    eval('cleanflightMSP0.sendMSP(direction, dataBytes, 200,    armCommandsToGoMSP, direction+ str(dataLength) + h)')
    time.sleep(1/HZ)

print("Armed... waiting to disarm")

for i in range(1, 50):
    EStop_failsafe.updateArmingState()
    stopBtnVal = EStop_failsafe.armingState
    eval('cleanflightMSP0.sendMSP(direction, dataBytes, 200,   [ZERO_ROLL, ZERO_PITCH, 1150, ZERO_YAW_RATE, DISARM, ANGLE_MODE, NEUTRAL, NEUTRAL], direction+ str(dataLength) + h)')
    if(stopBtnVal == 48):
        break
    time.sleep(1/10)
    
#Disarm
eval('cleanflightMSP0.sendMSP(direction, dataBytes, 200,   [ZERO_ROLL, ZERO_PITCH, ZERO_THROTTLE, ZERO_YAW_RATE, DISARM, ANGLE_MODE, NEUTRAL, NEUTRAL], direction+ str(dataLength) + h)')
print("Disarmed")
