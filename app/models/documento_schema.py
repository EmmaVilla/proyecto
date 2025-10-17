
# Crear archivos faltantes para el proyecto sociolegal
import os

# Crear carpetas si no existen
os.makedirs("app/models", exist_ok=True)
os.makedirs("app/schemas", exist_ok=True)
os.makedirs("app/routers", exist_ok=True)

with open("app/schemas/documento_schema.py", "w") as f:
    f.write('''
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentoCreate(BaseModel):
    tipo_documento: str

class DocumentoResponse(BaseModel):
    id: int
    nombre_original: str
    ruta_local: str
    tipo_documento: str
    fecha_subida: datetime

    class Config:
        orm_mode = True
''')
