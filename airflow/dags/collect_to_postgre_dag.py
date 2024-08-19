from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from memory import insert_memory_data
from cpu import insert_cpu_data

start_date = datetime.now() - timedelta(minutes=5)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': start_date,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG to run every minute
dag = DAG(
    'computer_data',
    description='DAG to insert  memory and CPU data into PostgreSQL every minute',
    schedule_interval='*/1 * * * *',  # Run every minute
    default_args=default_args,
    catchup=False
)




# Define tasks for inserting memory data
insert_memory_data_task = PythonOperator(
    task_id='insert_memory_data_task',
    python_callable=insert_memory_data,
    dag=dag
)

# Define tasks for inserting CPU data
insert_cpu_data_task = PythonOperator(
    task_id='insert_cpu_data_task',
    python_callable=insert_cpu_data,
    dag=dag
)

# Set task dependencies
insert_memory_data_task >> insert_cpu_data_task