import sys
from pathlib import Path

# Ajusta el número de parents según tu estructura real
project_root = Path(__file__).parents[1]  # Sube 2 niveles desde scripts/
sys.path.insert(0, str(project_root))

import logging
import os
from datetime import datetime
from etl.extract.csv_extractor import extract_csv
from etl.transform.data_transformer import procesar_y_guardar_df
from etl.load.data_load import main as load_data
from etl.models.database_init import DatabaseManager

db_manager = DatabaseManager()
df_saldos_staging = db_manager.execute_query("SELECT * FROM saldos_staging")
print(df_saldos_staging.head())  # Para ver los primeros registros

def configure_logging():
    """Configura el sistema de logging asegurando que exista el directorio"""
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)  # Crea el directorio si no existe
    
    log_filename = os.path.join(log_dir, f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return log_filename  # Retorna la ruta del archivo de log para referencia
def run_etl_pipeline():
    """Ejecuta el pipeline ETL completo"""
    try:
        logging.info("Iniciando proceso ETL")
        
        # 1. Extracción
        logging.info("Fase de Extracción")
        data_path = project_root / "data" / "saldos.csv"

        if not data_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {data_path}")        
        
        raw_data = extract_csv(data_path)
        logging.info(f"Extraídos {len(raw_data)} registros")
        
        # 2. Transformación
        logging.info("Fase de Transformación")   
        engine = db_manager.get_db_connection()     
        exito, mensaje, registros = procesar_y_guardar_df(raw_data,engine)
        logging.info(f"Transformados {registros} registros")
        
        print(mensaje)
        if exito:
            print(f"Se insertaron {registros} registros")
        else:
            print("Ocurrió un error en el proceso")
        
        # 3. Carga
        logging.info("Fase de Carga")
        load_data()
        logging.info("Carga completada exitosamente")
        
        logging.info("Proceso ETL finalizado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error en el proceso ETL: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    configure_logging()
    success = run_etl_pipeline()
    exit(0 if success else 1)