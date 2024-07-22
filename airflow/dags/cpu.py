import psutil
from datetime import datetime
import psycopg2

def get_cpu_percent():
    timestamp = datetime.now()
    cpu_percent = psutil.cpu_percent(5)
    return [timestamp, cpu_percent]


# Define the function to insert CPU data into PostgreSQL
def insert_cpu_data():
    cpu_list = get_cpu_percent()
    date_time = cpu_list[0]
    cpu_value = cpu_list[1]

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
        INSERT INTO cpu (date,hour,minute,cpu_percent)
        VALUES (%s::DATE, EXTRACT(HOUR FROM %s), EXTRACT(MINUTE FROM %s),%s);
        ''', (date_time, date_time, date_time, cpu_value))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
