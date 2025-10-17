
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
import psycopg2
import shutil
import os
import datetime
from app.routers import auth
from app.database import Base, engine
from app.routers import documentos

app = FastAPI()
app.include_router(documentos.router)
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "API sociolegal funcionando"}

# Configuración JWT
SECRET_KEY = "clave_secreta_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Seguridad y autenticación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="socioeconomicos",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Crear tablas necesarias
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS socioeconomico (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    ingresos INTEGER,
    vivienda VARCHAR(100),
    dependientes INTEGER,
    escolaridad VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS documentos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    filename TEXT,
    filepath TEXT
);
""")
conn.commit()

# Modelos
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Funciones auxiliares
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(username: str):
    cursor.execute("SELECT id, username, hashed_password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        return {"id": result[0], "username": result[1], "hashed_password": result[2]}
    return None

# Rutas
@app.post("/register")
def register(user: User):
    try:
        if get_user(user.username):
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        hashed_password = get_password_hash(user.password)
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
            (user.username, hashed_password)
        )
        conn.commit()
        return {"msg": "Usuario registrado exitosamente"}
    except Exception as e:
        print("❌ Error en /register:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/formulario")
def guardar_formulario(
    ingresos: int = Form(...),
    vivienda: str = Form(...),
    dependientes: int = Form(...),
    escolaridad: str = Form(...),
    user: dict = Depends(get_current_user)
):
    cursor.execute("""
        INSERT INTO socioeconomico (user_id, ingresos, vivienda, dependientes, escolaridad)
        VALUES (%s, %s, %s, %s, %s)
    """, (user["id"], ingresos, vivienda, dependientes, escolaridad))
    conn.commit()
    return {"msg": "Formulario guardado exitosamente"}

@app.post("/subir-documento")
def subir_documento(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    carpeta = f"documentos/{user['username']}"
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, file.filename)
    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    cursor.execute("INSERT INTO documentos (user_id, filename, filepath) VALUES (%s, %s, %s)", (user["id"], file.filename, ruta))
    conn.commit()
    return {"msg": "Documento subido exitosamente", "archivo": file.filename}
