import os
import requests
from flask import request, jsonify

def consulta_cnpj_externa(cnpj, mobile_sem_login):
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        return {'error': 'Chave da API não configurada.'}, 500

    API_URL = 'https://api.infosimples.com/api/v2/consultas/receita-federal/cnpj'
    
    # Dados que serão enviados no corpo da solicitação
    data = {
        'cnpj': cnpj,
        'token': API_KEY,
        'mobile_sem_login': 0,  
        'timeout': 300,
    }

    # Fazendo a solicitação POST com dados de formulário
    response = requests.post(API_URL, data=data)
    
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {'error': 'Erro ao consultar CNPJ', 'status_code': response.status_code}, response.status_code

def consulta_cnpj_route():
    data = request.get_json()

    cnpj = data.get('cnpj')
    

    if not cnpj:
        return jsonify({"error": "CNPJ não fornecido corretamente"}), 400

    resultado, status_code = consulta_cnpj_externa(cnpj)

    return jsonify(resultado), status_code
