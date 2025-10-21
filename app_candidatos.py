

from fastapi import FastAPI, UploadFile, Form, Request, File, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import psycopg2
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    return psycopg2.connect(
        dbname="socioeconomicos",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )


@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    response = templates.TemplateResponse("login.html", {"request": request})
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT rol FROM candidatos WHERE email=%s AND password=%s", (email, password))
    resultado = cur.fetchone()
    conn.close()

    if resultado and resultado[0] == "candidato":
        response = RedirectResponse(url="/candidato", status_code=303)
        response.set_cookie(key="usuario_autenticado", value="candidato", httponly=True)
        return response
    elif resultado and resultado[0] == "admin":
        response = RedirectResponse(url="/redadmin", status_code=303)
        response.set_cookie(key="usuario_autenticado", value="admin", httponly=True)
        return response
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas o usuario no creado")
    
@app.get("/candidato", response_class=HTMLResponse)
async def candidato_panel(request: Request):
    usuario = request.cookies.get("usuario_autenticado")
    if usuario != "candidato":
        return RedirectResponse(url="/", status_code=303)

    response = templates.TemplateResponse("candidato.html", {"request": request})
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/redadmin", response_class=HTMLResponse)
async def login_form(request: Request):
    response = templates.TemplateResponse("admin.html", {"request": request})
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
    
@app.post("/admin/consultar", response_class=HTMLResponse)
async def consultar_admin(request: Request, candidato_id: int = Form(...), curp: str = Form(...)):
    usuario = request.cookies.get("usuario_autenticado")
    if usuario != "admin":
        return RedirectResponse(url="/", status_code=303)

    conn = get_db()
    cur = conn.cursor()

    # Consultar datos del candidato
    cur.execute("""
        SELECT c.id, c.nombre, c.email, d.antecedentes, e.estudio_completo, e.documentos_completos, e.api_consulta_completa, e.pdf_generado
        FROM candidatos c
        LEFT JOIN datos_socioeconomicos d ON c.id = d.candidato_id
        LEFT JOIN etapas e ON c.id = e.candidato_id
        WHERE c.id = %s
    """, (candidato_id,))
    datos = cur.fetchone()

    # Consultar API de Búho Legal
    litigios = {}
    try:
        resultado = consultar_litigios(curp)
        litigios = resultado
    except Exception as e:
        litigios = {"error": str(e)}

    conn.close()

    if datos:
        datos_dict = {
            "id": datos[0],
            "nombre": datos[1],
            "email": datos[2],
            "antecedentes": datos[3],
            "estudio_completo": datos[4],
            "documentos_completos": datos[5],
            "api_consulta_completa": datos[6],
            "pdf_generado": datos[7]
        }
    else:
        datos_dict = {}

    response = templates.TemplateResponse("admin.html", {
        "request": request,
        "datos": datos_dict,
        "litigios": litigios
    })
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("usuario_autenticado")
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
print("Rutas protegidas y encabezados de caché configurados correctamente.")


@app.get("/redregistro", response_class=HTMLResponse)
async def login_form(request: Request):
    usuario = request.cookies.get("usuario_autenticado")
    if usuario == "candidato":
        return RedirectResponse(url="/candidato", status_code=303)
    elif usuario == "admin":
        return RedirectResponse(url="/admin", status_code=303)

    response = templates.TemplateResponse("registro.html", {"request": request})
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.post("/registro")
async def registro(nombre: str = Form(...), email: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM candidatos WHERE email=%s", (email,))
    if cur.fetchone():
        conn.close()
        return RedirectResponse(url="/candidato?mensaje=El+usuario+ya+existe", status_code=303)

    cur.execute(
        "INSERT INTO candidatos (nombre, email, password, fecha_registro, rol) VALUES (%s, %s, %s, %s, %s)",
        (nombre, email, password, datetime.now(), "candidato")
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/candidato?mensaje=Registro+exitoso", status_code=303)


if __name__ == '__main__':
    app.run(debug=True)

class DatosSocioeconomicos(BaseModel):
    situacion_familiar: str
    ingresos: str
    gastos: str
    situacion_laboral: str
    educacion: str
    vivienda: str
    referencias: str
    antecedentes: str


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
