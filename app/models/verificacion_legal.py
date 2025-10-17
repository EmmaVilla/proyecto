
import os

# Crear carpetas si no existen
os.makedirs("app/models", exist_ok=True)
os.makedirs("app/schemas", exist_ok=True)
os.makedirs("app/routers", exist_ok=True)

with open("app/models/verificacion_legal.py", "w") as f:
    f.write('''
from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class VerificacionLegal(Base):
    __tablename__ = "verificaciones_legales"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    resultado = Column(Text)
    fecha_consulta = Column(TIMESTAMP, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="verificaciones")
''')
