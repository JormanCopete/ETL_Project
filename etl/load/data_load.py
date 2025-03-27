import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from etl.models.database_init import DatabaseManager

db_manager = DatabaseManager()
df_saldos_staging = db_manager.execute_query("SELECT * FROM saldos_staging")
print(df_saldos_staging.head())  # Para ver los primeros registros



import pandas as pd
from sqlalchemy import create_engine

def cargar_dimensiones_basicas(engine):
    """Carga las dimensiones básicas con sus valores categóricos"""
    
    # DimSexo
    pd.DataFrame({
        'sexo_code': ['M', 'F'],
        'descripcion': ['Masculino', 'Femenino']
    }).to_sql('dim_sexo', engine, if_exists='append', index=False)
    
    # DimEstadoCivil
    pd.DataFrame({
        'codigo': [1, 2, 3, 4, 5, 6, 7],
        'descripcion': ['Soltero', 'Casado', 'Viudo', 'Union libre', 'Soltero', 'N/A', 'Divorciado']
    }).to_sql('dim_estado_civil', engine, if_exists='append', index=False)
    
    # DimTipoSalario
    pd.DataFrame({
        'codigo': [1, 2, 3, 4, 5, 6],
        'descripcion': ['Integral', 'Ley 50', 'Ley anterior', 'Otro', 'Ley 1278', 'Ley 2277']
    }).to_sql('dim_tipo_salario', engine, if_exists='append', index=False)
    
    # DimCodahor
    pd.DataFrame({
        'codigo': [1, 2, 3, 4, 5, 6, 7],
        'descripcion': ['Aportes', 'Ahorros', 'Servicios', 'Creditos', 'Tarjeta credito', 'CDAT', 'Interes Cdats']
    }).to_sql('dim_codahor', engine, if_exists='append', index=False)
    
    # DimClades
    pd.DataFrame({
        'codigo': [0, 1, 2],
        'descripcion': ['N/A', 'Nomina', 'Caja']
    }).to_sql('dim_clades', engine, if_exists='append', index=False)
    
    # DimClacuo
    pd.DataFrame({
        'codigo': [1, 2],
        'descripcion': ['Fija', 'Variable']
    }).to_sql('dim_clacuo', engine, if_exists='append', index=False)
    
    # DimPeriodd
    pd.DataFrame({
        'codigo': [1, 2, 3, 4],
        'descripcion': ['Mensual', 'Quincenal', 'Decadal', 'Semanal']
    }).to_sql('dim_periodd', engine, if_exists='append', index=False)

def cargar_dim_cliente(df, engine):
    """Carga la dimensión cliente desde saldos_staging"""
    
    # Obtener datos únicos de clientes
    clientes = df[[
        'documento_identidad', 'nombre', 'apellido', 'fecha_ingreso',
        'estrato', 'tipovehiculo'
    ]].drop_duplicates(subset=['documento_identidad'])
    
    # Obtener claves foráneas
    tablas_dim = {
        'sexo': ('sexo', 'dim_sexo', 'sexo_code'),
        'estado_civil': ('estado_civil', 'dim_estado_civil', 'codigo'),
        'tipo_salario': ('tipo_salario', 'dim_tipo_salario', 'codigo')
    }
    
    for col, (col_orig, tabla, col_cod) in tablas_dim.items():
        # Obtener mapeo de la dimensión
        dim_data = pd.read_sql(f"SELECT {col}_key, {col_cod} FROM {tabla}", engine)
        dim_map = dict(zip(dim_data[col_cod], dim_data[f'{col}_key']))
        
        # Mapear valores
        df[f'{col}_key'] = df[col_orig].map(dim_map)
    
    # Agregar claves foráneas al DataFrame de cliente
    cliente_keys = df.groupby('documento_identidad').agg({
        'sexo_key': 'first',
        'estado_civil_key': 'first',
        'tipo_salario_key': 'first'
    }).reset_index()
    
    clientes = clientes.merge(cliente_keys, on='documento_identidad', how='left')
    
    # Cargar datos
    clientes.to_sql('dim_cliente', engine, if_exists='append', index=False)

def cargar_dim_lincred(df, engine):
    """Carga la dimensión lincred desde saldos_staging"""
    
    # Obtener líneas de crédito únicas
    lincred = df[['lincred']].drop_duplicates()
    lincred['descripcion'] = 'Línea ' + lincred['lincred'].astype(str)
    lincred = lincred.rename(columns={'lincred': 'codigo'})
    
    # Cargar datos
    lincred.to_sql('dim_lincred', engine, if_exists='append', index=False)

def cargar_fact_saldos(df, engine):
    """Carga la tabla de hechos desde saldos_staging"""
    
    # Obtener todas las claves foráneas
    dimensiones = {
        'cliente': ('documento_identidad', 'dim_cliente', 'documento_identidad'),
        'lincred': ('lincred', 'dim_lincred', 'codigo'),
        'periodd': ('periodd', 'dim_periodd', 'codigo'),
        'clacuo': ('clacuo', 'dim_clacuo', 'codigo'),
        'clades': ('clades', 'dim_clades', 'codigo'),
        'codahor': ('codahor', 'dim_codahor', 'codigo'),
        'tipo_salario': ('tipo_salario', 'dim_tipo_salario', 'codigo'),
        'estado_civil': ('estado_civil', 'dim_estado_civil', 'codigo'),
        'sexo': ('sexo', 'dim_sexo', 'sexo_code')
    }
    
    for dim, (col_orig, tabla, col_cod) in dimensiones.items():
        # Obtener mapeo de la dimensión
        dim_data = pd.read_sql(f"SELECT {dim}_key, {col_cod} FROM {tabla}", engine)
        dim_map = dict(zip(dim_data[col_cod], dim_data[f'{dim}_key']))
        
        # Mapear valores
        df[f'{dim}_key'] = df[col_orig].map(dim_map)
    
    # Seleccionar columnas para tabla de hechos
    fact_cols = [
        'salario', 'vlrsolicitud', 'valorob', 'saldot', 'cuota', 'tasaint',
        'saldo', 'saldo_inicial', 'vlr_debito', 'vlr_credito', 'valor_pagado',
        'mora_causado', 'mora_abono', 'mora_saldo', 'fecsolic', 'fecaprob',
        'fecfact', 'fecdesc', 'fecultcau', 'fecultpago', 'fecvemto', 'fecha_pago',
        'fecha_registro', 'ciclod', 'clasei', 'debcre', 'cuopen', 'plazo', 'periodo',
        'cliente_key', 'lincred_key', 'periodd_key', 'clacuo_key', 'clades_key',
        'codahor_key', 'tipo_salario_key', 'estado_civil_key', 'sexo_key'
    ]
    
    # Filtrar columnas existentes
    fact_cols = [col for col in fact_cols if col in df.columns]
    
    # Cargar datos
    df[fact_cols].to_sql('fact_saldos', engine, if_exists='append', index=False)

def main():
    # Configurar conexión
    engine = create_engine('postgresql://usuario:contraseña@localhost:5432/base_de_datos')
    
    # 1. Cargar datos desde saldos_staging
    df = pd.read_sql_table('saldos_staging', engine)
    
    # 2. Limpieza básica (sin categorización)
    df.replace('NULL', np.nan, inplace=True)
    numeric_cols = ['salario', 'vlrsolicitud', 'valorob', 'saldot', 'cuota', 
                   'tasaint', 'saldo', 'saldo_inicial', 'vlr_debito', 
                   'vlr_credito', 'valor_pagado', 'mora_causado', 
                   'mora_abono', 'mora_saldo']
    for col in numeric_cols:
        if col in df.columns:
            df[col].fillna(0, inplace=True)
    
    # 3. Cargar dimensiones básicas
    cargar_dimensiones_basicas(engine)
    
    # 4. Cargar dimensión lincred
    cargar_dim_lincred(df, engine)
    
    # 5. Cargar dimensión cliente
    cargar_dim_cliente(df, engine)
    
    # 6. Cargar tabla de hechos
    cargar_fact_saldos(df, engine)
    
    print("Proceso de carga completado exitosamente")

if __name__ == "__main__":
    main()