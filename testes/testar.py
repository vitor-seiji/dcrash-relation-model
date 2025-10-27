import requests

# URL da sua API
url = 'http://127.0.0.1:5000/acidentes/novo'

# Dados do acidente
dados = {
    "concessionaria": "CCR ViaOeste",
    "rodovia": "SP-280",
    "km": 45.5,
    "sentido": "Interior",
    "data": "2025-10-19T10:30:00",
    "classificação_acidente": "Com vítimas",
    "Tipo_acidente": "Colisão traseira",
    "causa": "Falta de atenção",
    "meteoro": "Chuva",
    "visibilidade": "Reduzida",
    "veiculo": "Caminhão",
    "fatalidades": 0,
    "pista": "Dupla",
    "latitude": -23.5505,
    "longitude": -46.6333
}

print("📤 Enviando acidente para a API...")
response = requests.post(url, json=dados)

print(f"\n📊 Status Code: {response.status_code}")
print(f"\n📄 Resposta da API:")
print(response.json())