# add the sensor code here
import sensor
import alert
import time
import sys

import sys
sys.path.append('/srv/samba/Server')

# include secrets from secrets.json
import json
with open('/srv/samba/Warning/secrets/secrets.json') as f:
    secrets = json.load(f)

email_recipients = secrets['email_recipients']

# Use package-style imports
from database import database_util
from plant_requests.utils import image_util

ec_value_tripped = False
water_leak_tripped = False
low_water_level_tripped = False
ec_not_in_water = False
daily_email_sent = False

#sensor.enable_water_pump_automation()
sensor.turn_on_water_pump()

def handle_ece_check():
    global ec_value_tripped
    if not sensor.is_EC_sensor_in_water():
        print("\033[33mEC Value: \033[0m", sensor.get_EC_value(), "\033[33mSensor not in water\033[0m")
    else:
        if sensor.is_bad_EC_value() and not ec_value_tripped:
                print("\033[91mEC Value: \033[0m", sensor.get_EC_value(), "\033[91mBad value!\033[0m")
                alert.send_email("ALERT: Bad EC Value Detected in Greenhouse", f"Hello! Automated Greenhouse has detected a bad EC value of {sensor.get_EC_value()}. Please check the nutrient levels and adjust as necessary.", email_recipients)
                ec_value_tripped = True
        elif sensor.is_bad_EC_value() and ec_value_tripped:
                print("\033[91mEC Value: \033[0m", sensor.get_EC_value(), "\033[91mBad value!\033[0m")
        else:
                print("\033[92mEC Value: \033[0m", sensor.get_EC_value(), "\033[92mGood value!\033[0m")

def handle_water_level():
    global low_water_level_tripped
    if sensor.is_water_level_low() and not low_water_level_tripped:
        print("\033[91mLow Water Level: \033[0m", sensor.is_water_level_low(), "\033[91mLow water level detected!\033[0m")
        alert.send_email("ALERT: Low Water Level Detected in Greenhouse", "Hello! Automated Greenhouse has detected a low water level. Please refill the water reservoir as soon as possible.", email_recipients)
        low_water_level_tripped = True
    elif sensor.is_water_level_low() and low_water_level_tripped:
        print("\033[91mLow Water Level: \033[0m", sensor.is_water_level_low(), "\033[91mLow water level detected!\033[0m")
    else:
        print("\033[92mLow Water Level: \033[0m", sensor.is_water_level_low(), "\033[92mWater level is sufficient!\033[0m")

def handle_water_leak():
    global water_leak_tripped
    if sensor.is_water_leak_detected() and not water_leak_tripped:
        print("\033[91mWater Leak: \033[0m", sensor.is_water_leak_detected(), "\033[91mThere is a leak!\033[0m")
        alert.send_email("URGENT: Water Leak Detected in Greenhouse", "Hello! Automated Greenhouse has detected a leak in the water system. The water pump has been turned off and the automation has been disabled.", email_recipients)
        water_leak_tripped = True
        sensor.turn_off_water_pump()
    elif sensor.is_water_leak_detected() and water_leak_tripped:
        print("\033[91mWater Leak: \033[0m", sensor.is_water_leak_detected(), "\033[91mThere is a leak!\033[0m")
    else:
        print("\033[92mWater Leak: \033[0m", sensor.is_water_leak_detected(), "\033[92mThere is no leak!\033[0m")

while True:
    handle_ece_check()
    handle_water_level()
    handle_water_leak()
    
    
    #how to make the colors of the text appear as different colors in the console:
    #print("\033[92mEC Value: \033[0m", sensor.get_EC_value(), "\033[92mGood value!\033[0m")
    #print("\033[91mWater Leak: \033[0m", sensor.is_water_leak_detected(), "\033[91mNo leaks!\033[0m")

    time.sleep(10)
    
