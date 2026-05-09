import requests
import time 

# include secrets from secrets.json
import json
with open('/srv/samba/Warning/secrets/secrets.json') as f:
    secrets = json.load(f)

headers = {
"Authorization": secrets['auth_token'],
"Content-Type": "application/json",
}

def are_lights_on():
    url = "http://192.168.0.50:8123/api/states/switch.lights"
    response = get_response(url, headers)
    return response['state'] == 'on'

def turn_on_lights():
    url = "http://192.168.0.50:8123/api/services/switch/turn_on"
    data = {
        "entity_id": "switch.lights"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

def turn_off_lights():
    url = "http://192.168.0.50:8123/api/services/switch/turn_off"
    data = {
        "entity_id": "switch.lights"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

def is_water_level_low():
    url = "http://192.168.0.50:8123/api/states/binary_sensor.water_level_sensor"
    response = get_response(url, headers)
    if response['state'] == 'on':
        return True
    else:        
        return False

def get_EC_value():
   url = "http://192.168.0.50:8123/api/states/sensor.ec_sensor_value"
   response = get_response(url, headers)
   return response['state']


def is_EC_sensor_in_water():
    EC_value = get_EC_value()
    if float(EC_value) <= 350:
        return False
    return True

def is_bad_EC_value():
    EC_value = get_EC_value()
    if float(EC_value) > 350 and float(EC_value) < 800:
        return True
    if float(EC_value) > 1800:
        return True
    return False

def is_water_leak_detected():
    url = "http://192.168.0.50:8123/api/states/binary_sensor.water_leak_threshold"
    response = get_response(url, headers)
    if response['state']=='on':
        return True
    return False
    
def turn_off_water_pump():
    url = "http://192.168.0.50:8123/api/services/switch/turn_off"
    data = {
        "entity_id": "switch.pump"
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    return response.status_code == 200

def turn_on_water_pump():
    url = "http://192.168.0.50:8123/api/services/switch/turn_on"
    data = {
        "entity_id": "switch.pump"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

def disable_water_pump_automation():
    url = "http://192.168.0.50:8123/api/services/automation/turn_off"
    data = {
        "entity_id": "automation.pump_timer"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

def enable_water_pump_automation():
    url = "http://192.168.0.50:8123/api/services/automation/turn_on"
    data = {
        "entity_id": "automation.pump_timer"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

def is_water_pump_automation_enabled():
    url = "http://192.168.0.50:8123/api/states/automation.pump_timer"
    response = get_response(url, headers)
    return response['state'] == 'on'

def get_response(url, headers):
    resp = requests.get(url, headers=headers)
    return resp.json()
