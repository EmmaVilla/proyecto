import requests

credenciales = {
    'username': 'emmanuel.v@acheme.com.mx',
    'password': 'Cfsqh9'
}

response = requests.post('https://api.buholegal.com/apikey/', data=credenciales)

if response.status_code == 200:
    print("Respuesta completa:")
    print(response.json())  # Esto mostrará todo el contenido, incluyendo user_ID si está presente
else:
    print(f'Error al autenticar. Código de estado: {response.status_code}')
    print(f'Respuesta: {response.text}')