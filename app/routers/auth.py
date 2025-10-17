from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import Usuario

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_PASSWORD_LENGTH = 72

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

@router.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    if len(request.password.encode("utf-8")) > MAX_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no puede exceder los 72 bytes."
        )

    hashed_password = pwd_context.hash(request.password[:MAX_PASSWORD_LENGTH])

    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado."
        )

    new_user = User(
        email=request.email,
        hashed_password=hashed_password,
        full_name=request.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

