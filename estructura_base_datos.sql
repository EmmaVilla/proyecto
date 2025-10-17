
CREATE TABLE IF NOT EXISTS candidatos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    email TEXT UNIQUE,
    password TEXT,
    fecha_registro TIMESTAMP
);

CREATE TABLE IF NOT EXISTS datos_socioeconomicos (
    candidato_id INTEGER REFERENCES candidatos(id),
    situacion_familiar TEXT,
    ingresos TEXT,
    gastos TEXT,
    situacion_laboral TEXT,
    educacion TEXT,
    vivienda TEXT,
    referencias TEXT,
    antecedentes TEXT
);

CREATE TABLE IF NOT EXISTS documentos (
    id SERIAL PRIMARY KEY,
    candidato_id INTEGER REFERENCES candidatos(id),
    nombre_archivo TEXT,
    ruta TEXT,
    fecha_subida TIMESTAMP
);

CREATE TABLE IF NOT EXISTS etapas (
    candidato_id INTEGER REFERENCES candidatos(id),
    estudio_completo BOOLEAN,
    documentos_completos BOOLEAN,
    api_consulta_completa BOOLEAN,
    pdf_generado BOOLEAN
);
