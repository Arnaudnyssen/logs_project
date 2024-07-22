import psutil
from datetime import datetime
import sqlite3

def get_battery():
    timestamp = datetime.now()
    battery_info = psutil.sensors_battery()
    return [timestamp, battery_info]

def transform_battery(battery_list):
    lst = [battery_list[0]]
    battery_info = battery_list[1]
    for data in [battery_info.percent, battery_info.secsleft, battery_info.power_plugged]:
        lst.append(data)
    return lst

def insert_battery_data():
    collect_data = get_battery()
    data_to_insert = transform_battery(collect_data)
    date_time = data_to_insert[0]
    battery_data = data_to_insert[1:]

    try:
        # Connect to SQLite database
        conn = sqlite3.connect('data_computer.db')

        # Create a cursor object
        cur = conn.cursor()

        # Create table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS battery (
                Date TEXT,
                Hour INTEGER,
                Minute INTEGER,
                percent_battery_left REAL,
                seconds_left INTEGER,
                power_plugged INTEGER
            )
        ''')

        # Insert the data
        cur.execute('''
            INSERT INTO battery (Date, Hour, Minute, percent_battery_left, seconds_left, power_plugged)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date_time.date(), date_time.hour, date_time.minute, *battery_data))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

# Test the function
insert_battery_data()
