from sqlalchemy import Column, Integer, String, Date
from .base import Base

class DimSexo(Base):
    __tablename__ = 'dim_sexo'
    sexo_key = Column(Integer, primary_key=True)
    sexo_code  = Column(String(1), unique=True)
    descripcion  = Column(String(50))

class DimEstadoCivil (Base):
    __tablename__ = 'dim_estado_civil'
    estado_civil_key  = Column(Integer, primary_key=True)
    codigo   = Column(Integer, unique=True)
    descripcion  = Column(String(50))

class DimTipoSalario  (Base):
    __tablename__ = 'dim_tipo_salario'
    tipo_salario_key   = Column(Integer, primary_key=True)
    codigo   = Column(Integer, unique=True)
    descripcion  = Column(String(50))

class DimCodahor   (Base):
    __tablename__ = 'dim_codahor'
    codahor_key    = Column(Integer, primary_key=True)
    codigo   = Column(Integer, unique=True)
    descripcion  = Column(String(50))

class DimClades    (Base):
    __tablename__ = 'dim_clades'
    clades_key     = Column(Integer, primary_key=True)
    codigo   = Column(Integer, unique=True)
    descripcion  = Column(String(50))

class DimClacuo     (Base):
    __tablename__ = 'dim_clacuo'
    clacuo_key      = Column(Integer, primary_key=True)
    codigo   = Column(Integer, unique=True)
    descripcion  = Column(String(50))

class DimPeriodd(Base):
    __tablename__ = 'dim_periodd'
    periodd_key  = Column(Integer, primary_key=True)
    codigo   = Column(Integer, unique=True)
    descripcion  = Column(String(50))

class DimLincred(Base):
    __tablename__ = 'dim_lincred'
    lincred_key  = Column(Integer, primary_key=True)
    codigo   = Column(Integer, unique=True)
    descripcion  = Column(String(50))

class DimCliente(Base):
    __tablename__ = 'dim_cliente'
    cliente_key = Column(Integer, primary_key=True)
    documento_identidad = Column(String(20), unique=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    fecha_ingreso = Column(Date)
    estrato = Column(Integer)
    tipovehiculo = Column(Integer)
    
