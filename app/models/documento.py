
import os

# Crear carpetas si no existen
os.makedirs("app/models", exist_ok=True)
os.makedirs("app/schemas", exist_ok=True)
os.makedirs("app/routers", exist_ok=True)

# Crear modelo documento.py
with open("app/models/documento.py", "w") as f:
    f.write('''
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    nombre_original = Column(String(255))
    ruta_local = Column(Text, nullable=False)
    tipo_documento = Column(String(100))
    fecha_subida = Column(TIMESTAMP, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="documentos")
''')
    
# Crear router documentos.py
with open("app/routers/documentos.py", "w") as f:
    f.write('''
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from app.database import SessionLocal
from app.models.documento import Documento
from app.models.user import Usuario
from app.schemas.documento_schema import DocumentoCreate, DocumentoResponse
from app.routers.auth import get_current_user

router = APIRouter()

UPLOAD_DIR = "uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-document", response_model=DocumentoResponse)
def upload_document(
    tipo_documento: str,
    file: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filename = file.filename
    user_folder = os.path.join(UPLOAD_DIR, current_user.curp or str(current_user.id))
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    documento = Documento(
        usuario_id=current_user.id,
        nombre_original=filename,
        ruta_local=file_path,
        tipo_documento=tipo_documento
    )
    db.add(documento)
    db.commit()
    db.refresh(documento)

    return documento
''')

print("Archivos documento.py, verificacion_legal.py, documento_schema.py y documentos.py creados correctamente.")

