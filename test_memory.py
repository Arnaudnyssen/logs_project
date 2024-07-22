import psutil
from datetime import datetime
import sqlite3


def get_memory():
    timestamp = datetime.now()
    memory_info = psutil.virtual_memory()
    return [timestamp, memory_info]


def transform_memory(memory_list):
    timestamp = memory_list[0]
    memory_info = memory_list[1]

    available_gb = memory_info.available / (1024 ** 3)
    percent_used = memory_info.percent

    return [timestamp, available_gb, percent_used]


def insert_memory_data():
    collect_data = get_memory()
    data_to_insert = transform_memory(collect_data)
    date_time = data_to_insert[0]
    memory_data = data_to_insert[1:]

    try:
        # Connect to SQLite database
        conn = sqlite3.connect('data_computer.db')

        # Create a cursor object
        cur = conn.cursor()

        # Create table if not exists
        cur.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                Date TEXT,
                Hour INTEGER,
                Minute INTEGER,
                Available_GB REAL,
                Percent_Used REAL
            )
        ''')

        # Insert the data
        cur.execute('''
            INSERT INTO memory (Date, Hour, Minute, Available_GB, Percent_Used)
            VALUES (?, ?, ?, ?, ?)
        ''', (date_time.date(), date_time.hour, date_time.minute, *memory_data))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


# Test the function
insert_memory_data()
