# API Flask + Supabase

Uma API REST completa construída com Flask e conectada ao Supabase.

## 🚀 Configuração

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Supabase
1. Copie o arquivo `config.env` e renomeie para `.env`
2. Preencha as variáveis com suas credenciais do Supabase:
   - `SUPABASE_URL`: URL do seu projeto Supabase
   - `SUPABASE_KEY`: Chave anônima do Supabase

### 3. Executar a aplicação
```bash
python main.py
```

A API estará disponível em `http://localhost:5000`

## 📚 Endpoints da API

### Operações CRUD Básicas

#### Listar todos os registros
```
GET /api/{table_name}
```

#### Buscar registro por ID
```
GET /api/{table_name}/{id}
```

#### Criar novo registro
```
POST /api/{table_name}
Content-Type: application/json

{
  "campo1": "valor1",
  "campo2": "valor2"
}
```

#### Atualizar registro
```
PUT /api/{table_name}/{id}
Content-Type: application/json

{
  "campo1": "novo_valor1"
}
```

#### Deletar registro
```
DELETE /api/{table_name}/{id}
```

#### Buscar com filtros
```
GET /api/{table_name}/search?campo=valor&limit=10&order_by=nome:asc
```

Parâmetros de busca:
- `limit`: Limitar número de resultados
- `offset`: Pular registros (paginação)
- `order_by`: Ordenar por campo (formato: campo:asc ou campo:desc)
- Qualquer outro parâmetro será usado como filtro de igualdade

## 📝 Exemplos de Uso

### Criar um usuário
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "João", "email": "joao@email.com"}'
```

### Listar todos os usuários
```bash
curl http://localhost:5000/api/users
```

### Buscar usuário por ID
```bash
curl http://localhost:5000/api/users/1
```

### Atualizar usuário
```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "João Silva"}'
```

### Deletar usuário
```bash
curl -X DELETE http://localhost:5000/api/users/1
```

### Buscar com filtros
```bash
curl "http://localhost:5000/api/users/search?name=João&limit=5&order_by=created_at:desc"
```

## 🔧 Estrutura do Projeto

```
FlaskBegin/
├── main.py              # Configuração principal da aplicação
├── routes.py            # Rotas da API
├── requirements.txt     # Dependências Python
├── config.env           # Configurações (renomear para .env)
└── templates/
    └── homepage.html    # Página inicial
```

## 🛡️ Tratamento de Erros

A API retorna respostas padronizadas:

**Sucesso:**
```json
{
  "success": true,
  "data": {...},
  "message": "Operação realizada com sucesso"
}
```

**Erro:**
```json
{
  "success": false,
  "error": "Mensagem de erro"
}
```

## 🔒 Segurança

- Configure adequadamente as políticas RLS (Row Level Security) no Supabase
- Use variáveis de ambiente para credenciais sensíveis
- Implemente autenticação conforme necessário

## 📊 Códigos de Status HTTP

- `200`: Sucesso
- `201`: Criado com sucesso
- `400`: Dados inválidos
- `404`: Registro não encontrado
- `500`: Erro interno do servidor
