import psutil
from datetime import datetime
import psycopg2

def get_memory():
    timestamp = datetime.now()
    memory_info = psutil.virtual_memory()
    return [timestamp, memory_info]


def transform_memory(memory_list):
    lst = [memory_list[0]]
    memory_info = memory_list[1]
    available_gb = memory_info.available / (1024 ** 3)
    lst.append(available_gb)
    lst.append(memory_info.percent)
    return lst

def insert_memory_data():
    collect_data = get_memory()
    data_to_insert = transform_memory(collect_data)
    date_time = data_to_insert[0]
    available_gb = data_to_insert[1]
    percent_used = data_to_insert[2]

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
               INSERT INTO memory (date,Hour,minute,available_gb,percent_used)
               VALUES (%s::DATE, EXTRACT(HOUR FROM %s), EXTRACT(MINUTE FROM %s),%s,%s);
               ''', (date_time, date_time, date_time, available_gb, percent_used))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
