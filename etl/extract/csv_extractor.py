import pandas as pd

def extract_csv(file_path):
    """Extrae datos del CSV y devuelve DataFrame"""
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
    return df


