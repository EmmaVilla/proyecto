
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import shutil
import os
import fitz  # PyMuPDF
import psycopg2
import requests
from datetime import datetime


# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="socioeconomicos",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

app = FastAPI()

class DatosSocioeconomicos(BaseModel):
    situacion_familiar: str
    ingresos: str
    gastos: str
    situacion_laboral: str
    educacion: str
    vivienda: str
    referencias: str
    antecedentes: str

@app.post("/registro")
def registrar(nombre: str = Form(...), email: str = Form(...), password: str = Form(...)):
    cursor.execute("INSERT INTO candidatos (nombre, email, password, fecha_registro) VALUES (%s, %s, %s, %s) RETURNING id",
                   (nombre, email, password, datetime.now()))
    candidato_id = cursor.fetchone()[0]
    conn.commit()
    return {"mensaje": "Registro exitoso", "candidato_id": candidato_id}

@app.post("/subir_documento")
def subir_documento(candidato_id: int = Form(...) , archivo: UploadFile = File(...)):
    carpeta = f"documentos/{candidato_id}"
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, archivo.filename)
    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)
    cursor.execute("INSERT INTO documentos (candidato_id, nombre_archivo, ruta, fecha_subida) VALUES (%s, %s, %s, %s)",
                   (candidato_id, archivo.filename, ruta, datetime.now()))
    conn.commit()
    return {"mensaje": "Documento subido correctamente"}

@app.post("/datos_socioeconomicos")
def guardar_datos(
    candidato_id: int = Form(...),
    situacion_familiar: str = Form(...),
    ingresos: str = Form(...),
    gastos: str = Form(...),
    situacion_laboral: str = Form(...),
    educacion: str = Form(...),
    vivienda: str = Form(...),
    referencias: str = Form(...),
    antecedentes: str = Form(...)
):
    cursor.execute(
        "INSERT INTO datos_socioeconomicos VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (candidato_id, situacion_familiar, ingresos, gastos,
         situacion_laboral, educacion, vivienda, referencias, antecedentes)
    )
    conn.commit()
    return {"mensaje": "Datos guardados correctamente"}


# Credenciales de Búho Legal
BUHO_USERNAME = "emmanuel.v@acheme.com.mx"
BUHO_PASSWORD = "Nuevo*2025$"

def obtener_token():
    url = "https://www.buholegal.com/apikey/"
    payload = {
        "username": BUHO_USERNAME,
        "password": BUHO_PASSWORD
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception("Error al obtener token de Búho Legal")

def consultar_litigios(curp):
    token = obtener_token()
    url = f"https://www.buholegal.com/busqueda/?curp={curp}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error al consultar litigios")


@app.post("/consultar_litigios")
def ruta_consultar_litigios(candidato_id: int = Form(...), curp: str = Form(...)):
    conn = psycopg2.connect(
        dbname="socioeconomicos",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    try:
        resultado = consultar_litigios(curp)
        resumen = str(resultado)

        cursor.execute("UPDATE datos_socioeconomicos SET antecedentes = %s WHERE candidato_id = %s",
                       (resumen, candidato_id))

        cursor.execute("UPDATE etapas SET api_consulta_completa = TRUE WHERE candidato_id = %s",
                       (candidato_id,))

        conn.commit()
        return {"mensaje": "Consulta realizada y guardada correctamente", "resultado": resultado}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()




@app.get("/generar_pdf")
def generar_pdf(candidato_id: int):
    cursor.execute("SELECT * FROM datos_socioeconomicos WHERE candidato_id = %s", (candidato_id,))
    datos = cursor.fetchone()
    cursor.execute("SELECT fecha_subida FROM documentos WHERE candidato_id = %s ORDER BY fecha_subida ASC LIMIT 1", (candidato_id,))
    fecha_documento = cursor.fetchone()
    fecha_reporte = datetime.now()

    contenido = f"""
Fecha de documentos: {fecha_documento[0] if fecha_documento else 'N/A'}

Fecha del reporte: {fecha_reporte}

--- Estudio Socioeconómico ---

Situación familiar: {datos[1]}

Ingresos: {datos[2]}

Gastos: {datos[3]}

Situación laboral: {datos[4]}

Educación: {datos[5]}

Vivienda: {datos[6]}

Referencias: {datos[7]}

Antecedentes: {datos[8]}

"""

    ruta_pdf = f"documentos/{candidato_id}/reporte_final.pdf"
    doc = fitz.open()
    pagina = doc.new_page()
    pagina.insert_text((72, 72), contenido, fontsize=12)
    doc.save(ruta_pdf)
    doc.close()

    cursor.execute("UPDATE etapas SET pdf_generado = TRUE WHERE candidato_id = %s", (candidato_id,))
    conn.commit()

    return FileResponse(ruta_pdf, media_type="application/pdf", filename="reporte_final.pdf")
