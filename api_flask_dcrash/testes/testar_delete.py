import requests

# Substitua pelo ID do acidente que você quer deletar
acidente_id = "550e8400-e29b-41d4-a716-446655440000"

url = f'http://127.0.0.1:5000/acidentes/delete/{acidente_id}'

print(f"🗑️ Deletando acidente {acidente_id}...")
response = requests.delete(url)

print(f"\n📊 Status Code: {response.status_code}")
print(f"\n📄 Resposta da API:")
print(response.json())