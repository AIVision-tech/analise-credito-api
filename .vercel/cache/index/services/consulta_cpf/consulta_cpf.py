from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

CORS(app, resources={r"*": {"origins": "*"}})

# Utiliza variáveis de ambiente para maior segurança
API_KEY = os.getenv('API_KEY', 'Yi3azCld-UKGoRdnEZBVhsNvmZ5gsJcBZLR1ROLm')
API_URL = 'https://api.infosimples.com/api/v2/consultas/receita-federal/cpf'

def consulta_cpf_externa(cpf, birthdate):
    """
    Faz a consulta do CPF na API da Infosimples.
    """
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

@app.route('/consulta_cpf', methods=['POST'])
def consulta_cpf_route():
    data = request.get_json()  # Usa get_json() para melhor manipulação de erros de JSON malformado

    cpf = data.get('cpf')
    birthdate = data.get('birthdate')

    if not cpf or not birthdate:
        return jsonify({"error": "CPF e/ou birthdate não fornecidos corretamente"}), 400

    resultado = consulta_cpf_externa(cpf, birthdate)

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
