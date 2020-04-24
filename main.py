#!/usr/bin/env python
import time

from ant.core import driver
from ant.core import node

from speedSensorRx import SpeedSensorRx
from cadenceSensorRx import CadenceSensorRx
from powerCalculator import PowerCalculator
from config import DEBUG, LOG, SERIAL, NETKEY, SPEED_SENSOR_TYPE, CADENCE_SENSOR_TYPE, SPEED_SENSOR_ID

antnode = None
speed_sensor = None
cadence_sensor = None
power_meter = None
spd = 0.0
cadence = 0.0
power = 0.0

try:
   # print "Using " + POWER_CALCULATOR.__class__.__name__

    stick = driver.USB2Driver(SERIAL, log=LOG, debug=DEBUG)
    antnode = node.Node(stick)
    print "Starting ANT node"
    antnode.start()
    key = node.NetworkKey('N:ANT+', NETKEY)
    antnode.setNetworkKey(0, key)

    print "Starting speed sensor"
    try:
        # Create the speed sensor object and open it
        speed_sensor = SpeedSensorRx(antnode, SPEED_SENSOR_TYPE)
        speed_sensor.start()
        # Notify the power calculator every time we get a speed event
        # speed_sensor.notify_change(POWER_CALCULATOR)
    except Exception as e:
        print"speed_sensor  error: " + e.message
        speed_sensor = None

    print "Starting cadence sensor"
    try:
        # Create the speed sensor object and open it
        cadence_sensor = CadenceSensorRx(antnode, CADENCE_SENSOR_TYPE)
        cadence_sensor.start()
        # Notify the power calculator every time we get a speed event
        # cadence_sensor.notify_change(POWER_CALCULATOR)
    except Exception as e:
        print"cadence_sensor  error: " + e.message
        cadences_sensor = None

    power_meter = PowerCalculator()
    '''
    print "Starting power meter with ANT+ ID " + repr(POWER_SENSOR_ID)
    try:
        # Create the power meter object and open it
        power_meter = PowerMeterTx(antnode, POWER_SENSOR_ID)
        power_meter.open()
    except Exception as e:
        print "power_meter error: " + e.message
        power_meter = None

    # Notify the power meter every time we get a calculated power value
    POWER_CALCULATOR.notify_change(power_meter)
    '''

    print "Main wait loop"
    while True:
        try:
            time.sleep(1)
            
            spd = speed_sensor.getSpeed()
            cadence = cadence_sensor.getCadence()
            power = power_meter.calculatePower(spd, cadence)

            # Stampa i valori
            print "Speed: " , spd
            print "Cadence: " , cadence
            print "Power: " , power

        except (KeyboardInterrupt, SystemExit):
            break

except Exception as e:
    print "Exception: "+repr(e)
finally:
    if speed_sensor:
        print "Closing speed sensor"
        speed_sensor.stop()

    if cadence_sensor:
        print "Closing speed sensor"
        cadence_sensor.stop()
    '''
    if power_meter:
        print "Closing power meter"
        power_meter.close()
        power_meter.unassign()
    '''
    if antnode:
        print "Stopping ANT node"
        antnode.stop()
