from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime
import requests

import shutil
import os
import fitz  # PyMuPDF
import psycopg2


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
def subir_documento(candidato_id: int = Form(...), archivos: List[UploadFile] = File(...)):
    carpeta = f"documentos/{candidato_id}"
    os.makedirs(carpeta, exist_ok=True)

    conn = psycopg2.connect(...)  # tu conexión
    cursor = conn.cursor()

    for archivo in archivos:
        ruta = os.path.join(carpeta, archivo.filename)
        with open(ruta, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)

        cursor.execute(
            "INSERT INTO documentos (candidato_id, nombre_archivo, ruta, fecha_subida) VALUES (%s, %s, %s, %s)",
            (candidato_id, archivo.filename, ruta, datetime.now())
        )

    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": f"{len(archivos)} documentos subidos correctamente"}


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


# Función para obtener el token de autenticación

def obtener_token():
    url = "https://www.buholegal.com/apikey/"
    payload = {
        "username": BUHO_USERNAME,
        "password": BUHO_PASSWORD
    }
    response = requests.post(url, json=payload, allow_redirects=False)
    if response.status_code == 200:
        return response.json()["token"]
    elif response.status_code in (301, 302, 307, 308):
        raise Exception(f"Redireccionado inesperadamente a {response.headers.get('Location')}")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Función para consultar litigios por CURP

def consultar_litigios(curp):
    token = obtener_token()
    url = f"https://www.buholegal.com/busqueda/?curp={curp}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        return response.json()
    elif response.status_code in (301, 302):
        raise Exception(f"Redirigido a {response.headers.get('Location')}")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Ruta FastAPI para consultar litigios y actualizar base de datos
@app.post("/consultar_litigios")
def consultar(candidato_id: int = Form(...), curp: str = Form(...)):

    try:
        resultado = consultar_litigios(curp)
        resumen = str(resultado)

        # Conexión a PostgreSQL
        conn = psycopg2.connect(
            dbname="candidatos_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Guardar resultado en la base de datos

        cursor.execute("UPDATE datos_socioeconomicos SET antecedentes = %s WHERE candidato_id = %s",
                       (resumen, candidato_id))

        cursor.execute("UPDATE etapas SET api_consulta_completa = TRUE WHERE candidato_id = %s",
                       (candidato_id,))

        conn.commit()
        cursor.close()
        conn.close()

        return {"mensaje": "Consulta realizada y guardada correctamente", "resultado": resultado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



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
