import pandas as pd
from pathlib import Path
import logging

def extract_csv(file_path):
    """Extrae datos del CSV y devuelve DataFrame"""

    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    logging.info(f"Intentando leer archivo: {file_path}")
    df = pd.read_csv(
        file_path,
        sep=';', 
        low_memory=False, 
        dtype={    
                'vlr_debito': 'float64',
                'vlr_credito': 'float64',
                'cuopen': 'Int64',
                'valor_pagado': 'float64',    
                'mora_causado': 'float64',
                'mora_abono': 'float64',
                'mora_saldo': 'float64'
              }, encoding='ISO-8859-1')
    logging.info(f"Archivo leído correctamente. Registros: {len(df)}")
    return df


