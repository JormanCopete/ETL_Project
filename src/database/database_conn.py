import yaml
from sqlalchemy import create_engine
from airflow.hooks.base import BaseHook
from .base import Base  # Asegúrate de que Base tenga importados todos tus modelos
import psycopg2

class DatabaseManager:
    def __init__(self, config_path="../../config/config.yaml"):
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
        # Crea todas las tablas definidas en la metadata de Base
        Base.metadata.create_all(self.engine)

if __name__ == '__main__':
    db_manager = DatabaseManager()
    db_manager.init_db()
    # Aquí puedes iniciar el proceso ETL o cualquier otra operación de carga.