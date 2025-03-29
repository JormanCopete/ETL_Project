import pandas as pd
from sqlalchemy import text

def procesar_y_guardar_df(df, engine, tabla_destino="saldos_staging"):
    """
    Procesa un DataFrame convirtiendo columnas de fecha y lo guarda en la base de datos
    
    Args:
        df (pd.DataFrame): DataFrame con los datos a procesar
        engine (sqlalchemy.engine.Engine): Conexión a la base de datos
        tabla_destino (str): Nombre de la tabla destino (default: "saldos_staging")
    
    Returns:
        tuple: (bool éxito, str mensaje, int registros_insertados)
    """
    try:
        # 1. Crear copia del DataFrame para staging
        df_staging = df.copy()
        
        # 2. Definir y procesar columnas de fecha
        date_columns = [
            "fecha_ingreso", "fecsolic", "fecaprob", "fecfact", "fecdesc",
            "fecultcau", "fecultpago", "fecvemto"
        ]
        
        for col in date_columns:
            if col in df_staging.columns:
                df_staging[col] = pd.to_datetime(
                    df_staging[col], 
                    format="%d/%m/%Y", 
                    errors="coerce"
                ).dt.date
        
        # 3. Verificar conversión de fechas (logging)
        print("Tipos de datos después de conversión:")
        print(df_staging[date_columns].dtypes)
        
        # 4. Verificar si la tabla está vacía antes de insertar
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {tabla_destino}"))
            row_count = result.scalar()
            
            if row_count == 0:
                # 5. Insertar datos en la base de datos
                registros_insertados = df_staging.to_sql(
                    tabla_destino,
                    con=engine,
                    if_exists="append",
                    index=False
                )
                
                msg = (f"Datos cargados correctamente en {tabla_destino}. "
                      f"Registros insertados: {registros_insertados}")
                return (True, msg, registros_insertados)
            else:
                msg = (f"La tabla '{tabla_destino}' ya contiene {row_count} registros. "
                       "No se insertaron nuevos datos.")
                return (False, msg, 0)
                
    except Exception as e:
        error_msg = f"Error al procesar y guardar datos: {str(e)}"
        print(error_msg)
        return (False, error_msg, 0)