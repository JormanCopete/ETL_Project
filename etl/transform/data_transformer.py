#from datetime import datetime
import pandas as pd

class DataTransformer:
    @staticmethod
    def transform_dates(df, date_columns):
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    
    @staticmethod
    def handle_debcre(df):
        if 'debcre' in df.columns:
            df.loc[df['debcre'] == 'C', ['saldo', 'saldo_inicial']] *= -1
        return df
    
    @staticmethod
    def generate_time_dimension(df, date_column):
        dates = df[date_column].dropna().unique()
        time_dim = pd.DataFrame({
            'fecha_completa': dates,
            'año': dates.dt.year,
            'mes': dates.dt.month,
            'dia': dates.dt.day,
            'trimestre': dates.dt.quarter
        })
        time_dim['fecha_key'] = time_dim['fecha_completa'].dt.strftime('%Y%m%d').astype(int)
        return time_dim