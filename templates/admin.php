
<?php
$conn = pg_connect("host=localhost dbname=socioeconomicos user=postgres password=admin");

// Procesar formulario principal
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['consultar'])) {
    $candidato_id = $_POST['candidato_id'];
    $curp = $_POST['curp'];

    // Llamar a la API FastAPI usando cURL
    $ch = curl_init('http://localhost:8000/consultar_litigios');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
        'candidato_id' => $candidato_id,
        'curp' => $curp
    ]));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/x-www-form-urlencoded'
    ]);

    $response = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error en cURL: ' . curl_error($ch);
    }
    curl_close($ch);

    $litigios = json_decode($response, true);

    // Obtener datos del candidato
    $query = "
        SELECT c.id, c.nombre, c.email, d.antecedentes, e.estudio_completo, e.documentos_completos, e.api_consulta_completa, e.pdf_generado
        FROM candidatos c
        LEFT JOIN datos_socioeconomicos d ON c.id = d.candidato_id
        LEFT JOIN etapas e ON c.id = e.candidato_id
        WHERE c.id = $1
    ";
    $result = pg_query_params($conn, $query, array($candidato_id));
    $datos = pg_fetch_assoc($result);
}

// Procesar actualizaciones de estatus
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['actualizar'])) {
    $candidato_id = $_POST['candidato_id'];
    $campo = $_POST['campo'];
    $valor = $_POST['valor'] === '1' ? 'TRUE' : 'FALSE';
    pg_query($conn, "UPDATE etapas SET $campo = $valor WHERE candidato_id = $candidato_id");
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel del Administrador</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Panel del Administrador</h1>

    <form method="post">
        ID Candidato: <input type="number" name="candidato_id" required><br>
        CURP: <input type="text" name="curp" required><br>
        <input type="submit" name="consultar" value="Consultar">
    </form>

    <?php if (!empty($datos)) { ?>
    <h2>Resultado de la consulta</h2>
    <table>
        <tr><th>ID</th><td><?= $datos['id'] ?></td></tr>
        <tr><th>Nombre</th><td><?= $datos['nombre'] ?></td></tr>
        <tr><th>Email</th><td><?= $datos['email'] ?></td></tr>
        <tr><th>Antecedentes</th><td><pre><?= $datos['antecedentes'] ?></pre></td></tr>
        <tr><th>Estudio completo</th><td><?= $datos['estudio_completo'] ? '✔️' : '❌' ?></td></tr>
        <tr><th>Documentos completos</th><td><?= $datos['documentos_completos'] ? '✔️' : '❌' ?></td></tr>
        <tr><th>API consulta completa</th><td><?= $datos['api_consulta_completa'] ? '✔️' : '❌' ?></td></tr>
        <tr><th>PDF generado</th><td><?= $datos['pdf_generado'] ? '✔️' : '❌' ?></td></tr>
    </table>

    <h3>Actualizar estatus</h3>
    <form method="post">
        <input type="hidden" name="candidato_id" value="<?= $datos['id'] ?>">
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
        <input type="submit" name="actualizar" value="Actualizar">
    </form>

    <?php if ($datos['pdf_generado']) { ?>
    <h3>Descargar PDF</h3>
    <a href="documentos/<?= $datos['id'] ?>/reporte_final.pdf" target="_blank">Descargar reporte</a>
    <?php } ?>

    <?php if (!empty($litigios)) { ?>
    <h3>Resultado de la API Búho Legal</h3>
    <pre><?= print_r($litigios, true) ?></pre>
    <?php } ?>
    <?php } ?>
</body>
</html>
