from main import app, supabase
from flask import render_template, request, jsonify
from supabase import Client
import traceback
import templates
import uuid

# Função auxiliar para obter o cliente Supabase
def get_supabase() -> Client:
    return app.config['SUPABASE']

# Rota da homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("templates.html")

#Rota da tabela total dos acidentes
@app.route('/tabela', methods=['GET'])
def tabela():
    response = supabase.table("Acidentes").select("*").execute()
    return jsonify(response.data)

#Rota tabela das rodovias
@app.route('/rodovias', methods=['GET'])
def rodovias_tabela():
    response = supabase.table("rodovias").select("*").execute()
    return jsonify(response.data)

#Rota para codigo das rodovias
@app.route('/rodovias/codigo', methods=['GET'])
def rodovias_codigo():
    response = supabase.table("rodovias").select("codigo").execute()
    return jsonify(response.data)

#Rota para nome das rodovias
@app.route('/rodovias/nome', methods=['GET'])
def rodovias_nome():
    response = supabase.table("rodovias").select("nome").execute()
    return jsonify(response.data)

#Rota para nome das rodovias e seu respectivo codigo
@app.route('/rodovias/nome/codigo', methods=['GET'])
def rodovias_nome_e_codigo():
    response = supabase.table("rodovias").select("nome, codigo").execute()
    return jsonify(response.data)

#Rota para o ID das rodovias
@app.route('/rodovias/id', methods=['GET'])
def rodovias_id():
    response = supabase.table("rodovias").select("id").execute()
    return jsonify(response.data)

#Rota para o ID e seu respecitvo codigo
@app.route('/rodovias/id/codigo', methods=['GET'])
def rodovias_id_nome():
    response = supabase.table("rodovias").select("id, codigo").execute()
    return jsonify(response.data)

#Rota para um acidente especifico baseado no ID
@app.route("/acidentes/<acidente_id>")
def get_acidente(acidente_id):
    try:
        data = supabase.table("Acidentes").select("*").eq("ID", acidente_id).execute().data
        return (jsonify(data[0]), 200) if data else (jsonify({"erro": "Acidente não encontrado"}), 404)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
#Remove um acidente da tabela
@app.route("/acidentes/delete/<acidente_id>", methods=["DELETE"])
def delete_acidente(acidente_id):
    try:
        # Primeiro, verifica se o registro existe
        data = supabase.table("Acidentes").select("ID").eq("ID", acidente_id).execute().data
        if not data:
            return jsonify({"erro": "Acidente não encontrado"}), 404

        # Se existe, remove
        supabase.table("Acidentes").delete().eq("ID", acidente_id).execute()
        return jsonify({"mensagem": f"Acidente {acidente_id} removido com sucesso."}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

#Insere um novo acidente na tabela
@app.route('/acidentes/novo', methods=['POST'])
def inserir_acidente():

    try:
        dados = request.get_json()
        
        # Validação básica dos campos obrigatórios
        campos_obrigatorios = ['rodovia', 'km', 'data', 'longitude', 'latitude']
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({
                    'erro': f'Campo obrigatório ausente: {campo}'
                }), 400
        
        # Prepara os dados para inserção
        acidente = {
            'concessionaria': dados.get('concessionaria'),
            'rodovia': dados['rodovia'],
            'km': float(dados['km']),
            'sentido': dados.get('sentido'),
            'data': dados['data'],
            'classificação_acidente': dados.get('classificacao_acidente'),
            'Tipo_acidente': dados.get('Tipo_acidente'),
            'causa': dados.get('causa'),
            'meteoro': dados.get('meteoro'),
            'visibilidade': dados.get('visibilidade'),
            'veiculo': dados.get('veiculo'),
            'fatalidades': dados.get('fatalidades', 0),
            'pista': dados.get('pista'),
            'latitude': float(dados['latitude']),
            'longitude': float(dados['longitude']),
            'rodovia_id': dados.get('rodovia_id')
        }
        
        # Insere no Supabase
        resultado = supabase.table('Acidentes').insert(acidente).execute()
        
        return jsonify({
            'mensagem': 'Acidente inserido com sucesso',
            'dados': resultado.data
        }), 201
        
    except Exception as e:
        return jsonify({
            'erro': str(e)
        }), 500

