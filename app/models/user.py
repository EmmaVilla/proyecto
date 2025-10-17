from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()

# Tabla de usuarios
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    full_name = Column(String(255))
    curp = Column(String(18), unique=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    documentos = relationship("Documento", back_populates="usuario")
    verificaciones = relationship("VerificacionLegal", back_populates="usuario")

# Tabla de documentos
class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    nombre_original = Column(String(255))
    ruta_local = Column(Text, nullable=False)
    tipo_documento = Column(String(100))
    fecha_subida = Column(TIMESTAMP, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="documentos")

# Tabla de verificaciones legales
class VerificacionLegal(Base):
    __tablename__ = "verificaciones_legales"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    resultado = Column(Text)
    fecha_consulta = Column(TIMESTAMP, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="verificaciones")

print("Modelos SQLAlchemy creados para usuarios, documentos y verificaciones legales.")