# Use the official Apache Airflow image
FROM apache/airflow:2.9.1
# Install additional Python packages
RUN pip install psycopg2-binary psutil
#copy Python scripts from the directory into container
COPY dags/ /usr/local/airflow/dags
# Set the working directory
WORKDIR /usr/local/airflow