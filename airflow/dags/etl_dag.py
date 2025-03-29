import sys
from pathlib import Path

# Ajusta el número de parents según tu estructura real
project_root = Path(__file__).parents[2]  # Sube 2 niveles desde dags/
sys.path.insert(0, str(project_root))


from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from etl.extract.csv_extractor import extract_csv
from etl.transform.data_transformer import procesar_y_guardar_df
from etl.load.data_load import main as load_data
from etl.models.database_init import DatabaseManager
import pandas as pd

db_manager = DatabaseManager()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 15),  # Update the start date to today or an appropriate date
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def extract_task():
    data_path = project_root / "data" / "saldos.csv"
    df = extract_csv(data_path)
    return  df.to_json()  # Serializar para XCom

def transform_task(**kwargs):
    ti = kwargs['ti']
    df_json = ti.xcom_pull(task_ids='extract')
    df = pd.read_json(df_json)
    
    # Transformaciones
    engine = db_manager.get_db_connection()     
    procesar_y_guardar_df(df,engine)
    
    return {
        'main_data': df.to_json()
    }

def load_task(**kwargs):
    ti = kwargs['ti']
    ti.xcom_pull(task_ids='transform')
    load_data()
    

with DAG('saldos_etl', 
     default_args=default_args,
     description='Cargar el proceso de saldos de cooperativa!',
     schedule_interval='@daily',  # Set the schedule interval as per your requirements
) as dag:

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_task
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_task,
        provide_context=True
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_task,
        provide_context=True
    )

    extract >> transform >> load