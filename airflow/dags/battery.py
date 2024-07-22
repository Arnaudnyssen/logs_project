import psutil
from datetime import datetime
import psycopg2


def get_battery():
    timestamp = datetime.now()
    battery_info = psutil.sensors_battery()
    battery_info_list = [timestamp, battery_info.percent, battery_info.power_plugged]
    return battery_info_list


def insert_battery_data():
    collect_data = get_battery()

    date_time = collect_data[0]
    battery_percent = collect_data[1]
    power_plugged = collect_data[2]

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
              INSERT INTO battery (date,hour,minute,percent_battery_left,power_plugged)
              VALUES (%s::DATE, EXTRACT(HOUR FROM %s), EXTRACT(MINUTE FROM %s),%s,%s);
              ''', (date_time, date_time, date_time, battery_percent, power_plugged))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")



