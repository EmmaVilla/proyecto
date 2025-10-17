import requests

headers = {'Authorization': 'Token ' + 'd822ba3c92d8cb5cf3ae6a748004ba0cb654a8201065995a56924d000254046338'}
params = {
    'nombre': 'Juan',
    'paterno': 'Pérez',
    'persona': 'fisica',
    'estado': 'AS',
    'detalle': False
}


resp = requests.get('https://api.buholegal.com/busquedas_disponibles/', headers=headers)
print(resp.status_code, resp.json())
