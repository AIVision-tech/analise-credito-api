import os
import requests
from datetime import datetime
from flask import request, jsonify

def consulta_cpf_externa(cpf, birthdate):
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        return {'error': 'Chave da API não configurada.'}, 500

    API_URL = 'https://api.infosimples.com/api/v2/consultas/receita-federal/cpf'
    
    # Dados que serão enviados no corpo da solicitação
    data = {
        'cpf': cpf,
        'birthdate': birthdate,
        'token': API_KEY,
        'timeout': 300  
    }

    # Fazendo a solicitação POST com dados de formulário
    response = requests.post(API_URL, data=data)
    
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {'error': 'Erro ao consultar CPF', 'status_code': response.status_code}, response.status_code

def consulta_cpf_route():
    data = request.get_json()

    cpf = data.get('cpf')
    birthdate = data.get('birthdate')

    if not cpf or not birthdate:
        return jsonify({"error": "CPF e/ou birthdate não fornecidos corretamente"}), 400

    # Converter a data de dd/mm/yyyy para yyyy-mm-dd
    try:
        birthdate_converted = datetime.strptime(birthdate, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use dd/mm/yyyy."}), 400

    resultado, status_code = consulta_cpf_externa(cpf, birthdate_converted)

    return jsonify(resultado), status_code
