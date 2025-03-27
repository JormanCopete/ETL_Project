import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
#from airflow.hooks.base import BaseHook

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from etl.models.base import Base  # Ahora puedes usar una importación absoluta

#from .base import Base  # Asegúrate de que Base tenga importados todos tus modelos
#import psycopg2
import pandas as pd

import os

class DatabaseManager:
    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la ruta del script actual
            config_path = os.path.join(base_dir, "..", "..", "config", "config.yaml")

        self.config = self.load_config(config_path)
        self.engine = self.get_db_connection()

    def load_config(self, file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def get_db_connection(self):
        db_config = self.config["database"]
        return create_engine(
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
        )

    def init_db(self):
        """Crea las tablas solo si no existen en la base de datos."""
        inspector = inspect(self.engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:  # Si no hay tablas, crea todas las definidas en Base
            print("Creando tablas en la base de datos...")
            Base.metadata.create_all(self.engine)
            print("Tablas creadas correctamente.")
        else:
            print("Las tablas ya existen. No se requiere creación.")        


    def execute_query(self, query):
        with self.engine.connect() as conn:
            return pd.read_sql(query, conn)        

if __name__ == '__main__':
    db_manager = DatabaseManager()
    db_manager.init_db()
    # Aquí puedes iniciar el proceso ETL o cualquier otra operación de carga.