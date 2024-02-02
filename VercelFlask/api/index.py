from flask import Flask, redirect
from flasgger import Swagger
import yaml
import os
import sys
 

# Adiciona o diretório raiz ao sys.path para permitir a importação de 'services'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Supondo que consulta_cpf_route() esteja em services.consulta_cpf.consulta_cpf
from services.consulta_cpf.consulta_cpf import consulta_cpf_route

app = Flask(__name__)

# Carregamento e combinação dos documentos Swagger
def load_and_combine_swagger_docs(swagger_dir_path):
    combined_docs = {"paths": {}, "definitions": {}}
    for root, dirs, files in os.walk(swagger_dir_path):
        for filename in files:
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    part = yaml.safe_load(file)
                    for key, value in part.items():
                        if key in combined_docs:
                            combined_docs[key].update(value)
                        else:
                            combined_docs[key] = value
    return combined_docs

# Caminho para o diretório que contém os arquivos YAML da documentação Swagger
swagger_docs_dir = os.path.join(os.path.dirname(__file__), '..', 'swagger')
swagger_template = load_and_combine_swagger_docs(swagger_docs_dir)

swagger = Swagger(app, template=swagger_template)

@app.route('/')
def index():
    return redirect("/apidocs/")

app.add_url_rule('/consulta_cpf', 'consulta_cpf', consulta_cpf_route, methods=['POST'])

if __name__ == "__main__":
    print("O servidor está rodando em http://127.0.0.1:5001")
    app.run(host='0.0.0.0', port=5001)
