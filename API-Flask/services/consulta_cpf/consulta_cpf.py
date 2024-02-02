from flask import request, jsonify
import requests

# Variáveis para utilização da API da Infosimples
API_KEY = 'Yi3azCld-UKGoRdnEZBVhsNvmZ5gsJcBZLR1ROLm'
API_URL = 'https://api.infosimples.com/consultas/docs/receita-federal/cpf'

def consulta_cpf_externa(cpf):
    """
    Faz a consulta do CPF na API da Infosimples.
    """
    headers = {
        'Authorization': f'Token {API_KEY}'
    }
    params = {
        'cpf': cpf,
    }
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Erro ao consultar CPF', 'status_code': response.status_code}

def consulta_cpf_route():
    cpf = request.json.get('cpf')
    if cpf:
        resultado = consulta_cpf_externa(cpf)
        return jsonify(resultado)
    else:
        return jsonify({"error": "CPF não fornecido"}), 400