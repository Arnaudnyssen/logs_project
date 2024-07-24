# logs_project

## Data Engineering Project Logs

This project is designed to monitor and display the CPU and memory usage of your computer. The data is collected using Apache Airflow, stored in a PostgreSQL database, and visualized using a Streamlit app.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Project Structure](#project-structure)
4. [Components](#components)
   - [Apache Airflow](#apache-airflow)
   - [PostgreSQL and pgAdmin](#postgresql-and-pgadmin)
   - [Streamlit App](#streamlit-app)
   - [Flower](#flower)
5. [Docker Compose Configuration](#docker-compose-configuration)
6. [Usage](#usage)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

Ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Setup

Clone the repository:

```sh
git clone https://github.com/yourusername/Data_engineering_project_logs.git
cd Data_engineering_project_logs
```
Initialize the PostgreSQL database:

docker-compose up -d postgres
Initialize Airflow and other services:


docker-compose up -d
## Project Structure


Data_engineering_project_logs/
│
├── airflow/
│   ├── dags/
│   │   ├── collect_to_postgre_dag.py
│   │   ├── cpu.py
│   │   └── memory.py
│   ├── Dockerfile
│   ├── logs/
│   └── init.sql
│
├── streamlit/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── docker-compose.yml
├── README.md
└── .env (optional for environment variables)
Components

Apache Airflow
Apache Airflow is used to schedule and manage the tasks of collecting CPU and memory logs every minute. The DAG script is located in airflow/dags/collect_to_postgre_dag.py.

Starting Airflow

To start the Airflow web server and scheduler, run:

docker-compose up -d airflow-webserver airflow-scheduler
PostgreSQL and pgAdmin
PostgreSQL is used to store the logs in a database named data_computer with tables cpu and memory.

Access pgAdmin

pgAdmin can be accessed at http://localhost:5050 with the following default credentials:

Email: airflow@hotmail.be
Password: airflow
Streamlit App
The Streamlit app visualizes the logs stored in PostgreSQL. It displays the last 10 minutes of data in graphical form. You can select which graph to display by clicking on a button in the Streamlit app.

Running Streamlit

To run the Streamlit app, execute:

docker-compose up -d streamlit
The app can be accessed at http://localhost:8501.

Flower
Flower is a web-based tool for monitoring and administrating Celery clusters.

Access Flower

Flower can be accessed at http://localhost:5555.

Docker Compose Configuration

The docker-compose.yml file configures the services for this project. Below are some important sections:

version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: data_computer
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: airflow@hotmail.be
      PGADMIN_DEFAULT_PASSWORD: airflow
    ports:
      - "5050:80"
    depends_on:
      - postgres

  airflow-webserver:
    build: ./airflow
    command: webserver
    ports:
      - "8080:8080"
    depends_on:
      - postgres

  airflow-scheduler:
    build: ./airflow
    command: scheduler
    depends_on:
      - airflow-webserver

  flower:
    build: ./airflow
    command: celery flower
    ports:
      - "5555:5555"
    depends_on:
      - airflow-scheduler

  streamlit:
    build: ./streamlit
    ports:
      - "8501:8501"
    depends_on:
      - postgres

volumes:
  pgdata:
  logs:
    driver: local
Usage

Start all services:

docker-compose up -d
Verify that all containers are running:


docker-compose ps
Access the Airflow web UI at http://localhost:8080.
Access pgAdmin at http://localhost:5050.
Access the Streamlit app at http://localhost:8501.
Access Flower at http://localhost:5555.
Customization

Modify the Airflow DAG in airflow/dags/collect_to_postgre_dag.py as needed.
Customize the Streamlit app in streamlit/app.py.
Troubleshooting

Ensure Docker and Docker Compose are properly installed.

Check logs for any errors:

docker-compose logs
If the Airflow webserver or scheduler is not starting, verify the configuration in docker-compose.yml.