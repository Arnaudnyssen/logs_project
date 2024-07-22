import psutil
from datetime import datetime

def get_cpu_percent():
    timestamp = datetime.now()
    cpu_percent = psutil.cpu_percent(1)
    return [timestamp, cpu_percent]

def get_sensor_temp():
    timestamp = datetime.now()
    sensor_temp = psutil.sensors_temperatures()
    return [timestamp, sensor_temp]

def get_battery():
    timestamp = datetime.now()
    battery_info = psutil.sensors_battery()
    return [timestamp, battery_info]

def get_memory():
    timestamp = datetime.now()
    memory_info = psutil.virtual_memory()
    return [timestamp, memory_info]

def collect_data():
    data = {}

    data["cpu_usage"] = get_cpu_percent()
    data["sensor_temp"] = get_sensor_temp()
    data["battery_info"] = get_battery()
    data["memory_usage"] = get_memory()

    return data