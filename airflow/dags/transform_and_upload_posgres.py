import psycopg2

#we want to make a function that takes as argument a list of datetime and a dictionary
#and return a list with datetime as first argument and the percentage of current temperature
#on the critical temperature
def transform_sensor_temp(sensor_temp):
    lst = [sensor_temp[0]]
    actiz_data = sensor_temp[1].get('actiz', [])
    for data in actiz_data:
        if 'current' in data and 'critical' in data:
            actiz_percentage = data['current'] / data['critical']
            lst.append(actiz_percentage)
    coretemp_data = sensor_temp[1].get('coretemp', [])
    for data in coretemp_data:
        coretemp = data['current']
        lst.append(coretemp)
    return lst

def transform_battery(battery_list):
    lst = [battery_list[0]]
    battery_info = battery_list[1]
    for data in battery_info:
        lst.append(data)
    return lst

def transform_memory(memory_list):
    lst = [memory_list[0]]
    memory_info = memory_list[1]
    available_gb = memory_info.available / (1024 ** 3)
    lst.append(available_gb)

    lst.append(memory_info.percent)

    cached_gb = memory_info.cached / (1024 ** 3)
    lst.append(cached_gb)

    return lst

def transform_data(data):
    transformed_data = {}

    transformed_data["cpu_usage"] = data["cpu_usage"]  # No transformation needed here

    # Call specific transform function for sensor temp data
    transformed_data["sensor_temp"] = transform_sensor_temp(data["sensor_temp"])

    # Call specific transform function for battery data
    transformed_data["battery_info"] = transform_battery(data["battery_info"])

    # Call specific transform function for memory data
    transformed_data["memory_usage"] = transform_memory(data["memory_usage"])

    return transformed_data







