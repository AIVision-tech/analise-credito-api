# consulta_cpf.py
import os
import requests

# A definição da função de consulta permanece a mesma
def consulta_cpf_externa(cpf, birthdate):
    """
    Faz a consulta do CPF na API da Infosimples.
    """
    API_KEY = os.getenv('API_KEY', 'Yi3azCld-UKGoRdnEZBVhsNvmZ5gsJcBZLR1ROLm')
    API_URL = 'https://api.infosimples.com/api/v2/consultas/receita-federal/cpf'
    
    headers = {
        'Authorization': f'Token {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'cpf': cpf,
        'birthdate': birthdate
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Erro ao consultar CPF', 'status_code': response.status_code}

def consulta_cpf_route():
    from flask import request, jsonify  # Importe local para evitar dependências circulares
    
    data = request.get_json()

    cpf = data.get('cpf')
    birthdate = data.get('birthdate')

    if not cpf or not birthdate:
        return jsonify({"error": "CPF e/ou birthdate não fornecidos corretamente"}), 400

    resultado = consulta_cpf_externa(cpf, birthdate)

    return jsonify(resultado)
