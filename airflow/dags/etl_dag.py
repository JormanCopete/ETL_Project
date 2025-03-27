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
from etl.transform.data_transformer import DataTransformer
from etl.load.data_load import main
import pandas as pd

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
    df = extract_csv('/data/saldos.csv')
    return  df.to_json()  # Serializar para XCom

def transform_task(**kwargs):
    ti = kwargs['ti']
    df_json = ti.xcom_pull(task_ids='extract')
    df = pd.read_json(df_json)
    
    # Transformaciones
    df = DataTransformer.handle_debcre(df)
    #df = DataTransformer.transform_dates(df, settings.DATE_COLUMNS)
    time_dim = DataTransformer.generate_time_dimension(df, 'fecsolic')
    
    return {
        'main_data': df.to_json(),
        'time_dim': time_dim.to_json()
    }

#def load_task():
def load_task(**kwargs):
#    ti = kwargs['ti']
#    data = ti.xcom_pull(task_ids='transform')

    main()
    
    #main_df = pd.read_json(data['main_data'])
    #time_dim = pd.read_json(data['time_dim'])
    
    #load_data(main_df, time_dim)

from etl.models.database_init import DatabaseManager

#def load_task(**kwargs):
#    ti = kwargs['ti']
#    data = ti.xcom_pull(task_ids='transform')
    
#    main_df = pd.read_json(data['main_data'])
#    time_dim = pd.read_json(data['time_dim'])
    
#    db_manager = DatabaseManager()
    
    # Insertar los datos en la base de datos
#    main_df.to_sql("saldos_staging", db_manager.engine, if_exists="append", index=False)
#    time_dim.to_sql("time_dimension", db_manager.engine, if_exists="append", index=False)


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