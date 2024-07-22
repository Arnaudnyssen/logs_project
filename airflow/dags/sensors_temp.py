import psutil
from datetime import datetime
import psycopg2

def get_sensor_temp():
    timestamp = datetime.now()
    sensor_temp = psutil.sensors_temperatures()
    return [timestamp, sensor_temp]

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

def insert_sensors_data():
    collect_data = get_sensor_temp()
    data_to_insert = transform_sensor_temp(collect_data)
    date_time = data_to_insert[0]
    sensors_data = data_to_insert[1]

    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            host="postgres",
            database="data_computer",
            user="airflow",
            password="airflow"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Insert the timestamp directly
        cur.execute('''
           INSERT INTO sensor_temp (Date,Hour,Minute,sensor_1_percent,sensor_2_percent,sensor_3_percent,
           sensor_4_percent,sensor_5_percent,sensor_6_percent,sensor_7_percent,sensor_8_percent)
           VALUES (%s::DATE, EXTRACT(HOUR FROM %s), EXTRACT(MINUTE FROM %s),%s,%s,%s,%s,%s,%s,%s,%s);
           ''', (date_time, date_time, date_time, *sensors_data))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")