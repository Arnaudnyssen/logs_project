import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import logging
import time

# Database connection parameters
DB_USER = "airflow"
DB_PASSWORD = "airflow"
DB_HOST = "postgres"
DB_PORT = "5432"
DB_NAME = "data_computer"

# Function to create a SQLAlchemy engine
def create_db_engine(user, password, host, port, db):
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

# Function to query the last 10 rows from a table
def get_last_10_rows(engine, table_name):
    query = f"""
    SELECT * FROM (
        SELECT *
        FROM {table_name} t
        ORDER BY t.id DESC
        LIMIT 10
    ) as temp
    ORDER BY temp.id
    ;
    """
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        logging.error(f"Error executing SQL query: {e}")
        return None

# Set up the Streamlit app
st.title("Real-Time Data Display")

# Initialize session state to store data
if 'data' not in st.session_state:
    st.session_state['data'] = {}

def main():
    # Create the database engine
    engine = create_db_engine(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    # Query the last 10 rows from each table and display them
    tables = ['memory', 'cpu']
    for table in tables:
        df = get_last_10_rows(engine, table)

        if df is not None:
            if not df.empty:
                # Append new data to session state
                if table in st.session_state['data']:
                    st.session_state['data'][table] = pd.concat([st.session_state['data'][table], df]).drop_duplicates().reset_index(drop=True)
                else:
                    st.session_state['data'][table] = df
                 # Ensure no more than 10 rows are stored
                st.session_state['data'][table] = st.session_state['data'][table].tail(10)

                # Create a line chart for each column in the table using minute as x-axis
                for column in df.columns:
                    if column not in ['date', 'hour', 'minute', 'id']:
                        full_df = st.session_state['data'][table]
                        fig = px.line(full_df, x='minute', y=column, title=f'{column} over Last 10 Minutes', labels={'minute': 'Minute', column: column})
                        st.plotly_chart(fig)
            else:
                st.warning(f"No data returned for table {table}.")
        else:
            st.error(f"Failed to retrieve data for table {table}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(30)
        st.experimental_rerun()
