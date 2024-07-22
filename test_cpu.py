import psutil
from datetime import datetime
import sqlite3

def get_cpu_percent():
    timestamp = datetime.now()
    cpu_percent = psutil.cpu_percent(1)
    return [timestamp, cpu_percent]

def insert_cpu_data():
    cpu_list = get_cpu_percent()
    date_time = cpu_list[0]
    cpu_value = cpu_list[1]

    try:
        # Connect to SQLite database
        conn = sqlite3.connect('data_computer.db')

        # Create a cursor object
        cur = conn.cursor()

        # Create table if not exists
        cur.execute('''
            CREATE TABLE IF NOT EXISTS cpu (
                Date TEXT,
                Hour INTEGER,
                Minute INTEGER,
                Cpu_percent REAL
            )
        ''')

        # Insert the data
        cur.execute('''
            INSERT INTO cpu (Date, Hour, Minute, Cpu_percent)
            VALUES (?, ?, ?, ?)
        ''', (date_time.date(), date_time.hour, date_time.minute, cpu_value))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

# Test the function
insert_cpu_data()
