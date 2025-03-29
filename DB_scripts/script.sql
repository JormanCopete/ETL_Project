CREATE TABLE IF NOT EXISTS saldos_staging
(
    id bigserial NOT NULL,
    documento_identidad character varying(20) COLLATE pg_catalog."default",
    nombre character varying(100) COLLATE pg_catalog."default",
    apellido character varying(100) COLLATE pg_catalog."default",
    sexo character(1) COLLATE pg_catalog."default",
    estado_civil integer,
    fecha_ingreso date,
    tipo_salario integer,
    salario numeric(15,2),
    estrato integer,
    tipovehiculo integer,
    lincred integer,
    fecsolic date,
    fecaprob date,
    fecfact date,
    fecdesc date,
    fecultcau date,
    fecultpago date,
    fecvemto date,
    plazo integer,
    vlrsolicitud numeric(15,2),
    valorob numeric(15,2),
    saldot numeric(15,2),
    cuota numeric(15,2),
    tasaint numeric(3,2),
    ciclod character(1) COLLATE pg_catalog."default",
    periodd character(1) COLLATE pg_catalog."default",
    clacuo character(1) COLLATE pg_catalog."default",
    clasei character(1) COLLATE pg_catalog."default",
    clades character(1) COLLATE pg_catalog."default",
    periodo integer,
    saldo numeric(15,2),
    saldo_inicial numeric(15,2),
    vlr_debito numeric(15,2),
    vlr_credito numeric(15,2),
    cuopen integer,
    valor_pagado numeric(15,2),
    fecha_pago character varying(20) COLLATE pg_catalog."default",
    mora_causado numeric(15,2),
    mora_abono numeric(15,2),
    mora_saldo numeric(15,2),
    descripcion character varying(100) COLLATE pg_catalog."default",
    codahor character(1) COLLATE pg_catalog."default",
    debcre character(1) COLLATE pg_catalog."default",
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT saldos_staging_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS  dim_sexo (
    sexo_key SERIAL PRIMARY KEY,
    sexo_code CHAR(1) UNIQUE,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS  dim_estado_civil (
    estado_civil_key SERIAL PRIMARY KEY,
    codigo INT UNIQUE,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS  dim_tipo_salario (
    tipo_salario_key SERIAL PRIMARY KEY,
    codigo INT UNIQUE,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS  dim_codahor (
    codahor_key SERIAL PRIMARY KEY,
    codigo INT UNIQUE,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS  dim_clades (
    clades_key SERIAL PRIMARY KEY,
    codigo INT UNIQUE,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS  dim_clacuo (
    clacuo_key SERIAL PRIMARY KEY,
    codigo INT UNIQUE,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS  dim_periodd (
    periodd_key SERIAL PRIMARY KEY,
    codigo INT UNIQUE,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS  dim_lincred (
    lincred_key SERIAL PRIMARY KEY,
    codigo INT UNIQUE,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS  dim_cliente (
    cliente_key SERIAL PRIMARY KEY,
    documento_identidad VARCHAR(20) UNIQUE,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    fecha_ingreso DATE,
    estrato INT,
    tipovehiculo INT
);

CREATE TABLE IF NOT EXISTS  fact_saldos (
    fact_key SERIAL PRIMARY KEY,
    salario FLOAT,
    vlrsolicitud FLOAT,
    valorob FLOAT,
    saldot FLOAT,
    cuota FLOAT,
    tasaint FLOAT,
    saldo FLOAT,
    saldo_inicial FLOAT,
    vlr_debito FLOAT,
    vlr_credito FLOAT,
    valor_pagado FLOAT,
    mora_causado FLOAT,
    mora_abono FLOAT,
    mora_saldo FLOAT,
    fecsolic DATE,
    fecaprob DATE,
    fecfact DATE,
    fecdesc DATE,
    fecultcau DATE,
    fecultpago DATE,
    fecvemto DATE,
    fecha_pago DATE,
    fecha_registro TIMESTAMP,
    ciclod CHAR(1),
    clasei CHAR(1),
    debcre CHAR(1),
    cuopen INT,
    plazo INT,
    periodo INT,
    cliente_key INT REFERENCES dim_cliente(cliente_key),
    lincred_key INT REFERENCES dim_lincred(lincred_key),
    periodd_key INT REFERENCES dim_periodd(periodd_key),
    clacuo_key INT REFERENCES dim_clacuo(clacuo_key),
    clades_key INT REFERENCES dim_clades(clades_key),
    codahor_key INT REFERENCES dim_codahor(codahor_key),
    tipo_salario_key INT REFERENCES dim_tipo_salario(tipo_salario_key),
    estado_civil_key INT REFERENCES dim_estado_civil(estado_civil_key),
    sexo_key INT REFERENCES dim_sexo(sexo_key)
);
