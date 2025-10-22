
<!-- templates/admin.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel del Administrador</title>
    /static/estilos.css
</head>
<body class="pagina-admin">
    <h2>Panel del Administrador</h2>

    /admin/consultar
        <label for="candidato_id">ID Candidato:</label>
        <input type="number" name="candidato_id" required>

        <label for="curp">CURP:</label>
        <input type="text" name="curp" required>

        <button type="submit">Consultar</button>
    </form>

    {% if datos %}
    <h3>Resultado de la consulta</h3>
    <table>
        <tr><th>ID</th><td>{{ datos.id }}</td></tr>
        <tr><th>Nombre</th><td>{{ datos.nombre }}</td></tr>
        <tr><th>Email</th><td>{{ datos.email }}</td></tr>
        <tr><th>Antecedentes</th><td>{{ datos.antecedentes }}</td></tr>
        <tr><th>Estudio completo</th><td>{{ datos.estudio_completo }}</td></tr>
        <tr><th>Documentos completos</th><td>{{ datos.documentos_completos }}</td></tr>
        <tr><th>API consulta completa</th><td>{{ datos.api_consulta_completa }}</td></tr>
        <tr><th>PDF generado</th><td>{{ datos.pdf_generado }}</td></tr>
    </table>

    <h4>Actualizar estatus</h4>
    /admin/consultar
        <input type="hidden" name="candidato_id" value="{{ datos.id }}">
        <select name="campo">
            <option value="estudio_completo">Estudio completo</option>
            <option value="documentos_completos">Documentos completos</option>
            <option value="api_consulta_completa">API consulta completa</option>
            <option value="pdf_generado">PDF generado</option>
        </select>
        <select name="valor">
            <option value="1">✔️</option>
            <option value="0">❌</option>
        </select>
        <button type="submit" name="actualizar" value="1">Actualizar</button>
    </form>

    <h4>Descargar PDF</h4>
    /documentos/{{ datos.id }}/reporte_final.pdfDescargar reporte</a>

    <h4>Resultado de la API Búho Legal</h4>
    <pre>{{ litigios | tojson(indent=2) }}</pre>
    {% endif %}
</body>
</html>