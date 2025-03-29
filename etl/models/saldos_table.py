from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, DateTime
from .base import Base

class FactSaldos(Base):
    __tablename__ = 'fact_saldos'
    fact_key = Column(Integer, primary_key=True)
   
    salario  = Column(Float)
    vlrsolicitud = Column(Float)
    valorob  = Column(Float)
    saldot  = Column(Float)
    cuota  = Column(Float)
    tasaint  = Column(Float)
    saldo = Column(Float)
    saldo_inicial = Column(Float)
    vlr_debito = Column(Float)
    vlr_credito = Column(Float)
    
    valor_pagado = Column(Float)
    mora_causado = Column(Float)
    mora_abono = Column(Float)
    mora_saldo = Column(Float)

    fecsolic = Column(Date)
    fecaprob = Column(Date)
    fecfact = Column(Date)
    fecdesc = Column(Date)
    fecultcau = Column(Date)
    fecultpago = Column(Date)
    fecvemto = Column(Date)
    fecha_pago = Column(Date)
    fecha_registro = Column(DateTime)

    ciclod  = Column(String(1))
    clasei  = Column(String(1))
    debcre = Column(String(1))

    cuopen = Column(Integer)
    plazo  = Column(Integer)
    periodo  = Column(Integer)


    cliente_key = Column(Integer, ForeignKey('dim_cliente.cliente_key'))
    lincred_key = Column(Integer, ForeignKey('dim_lincred.lincred_key'))
    periodd_key = Column(Integer, ForeignKey('dim_periodd.periodd_key'))
    clacuo_key = Column(Integer, ForeignKey('dim_clacuo.clacuo_key'))
    clades_key = Column(Integer, ForeignKey('dim_clades.clades_key'))
    codahor_key = Column(Integer, ForeignKey('dim_codahor.codahor_key'))
    tipo_salario_key = Column(Integer, ForeignKey('dim_tipo_salario.tipo_salario_key'))
    estado_civil_key = Column(Integer, ForeignKey('dim_estado_civil.estado_civil_key'))
    sexo_key = Column(Integer, ForeignKey('dim_sexo.sexo_key'))

