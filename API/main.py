from flask import Flask, redirect
from flasgger import Swagger
import yaml
import os

from services.consulta_cpf.consulta_cpf import consulta_cpf_route

app = Flask(__name__)

# Função para carregar e combinar Swagger docs de múltiplos arquivos YAML
def load_and_combine_swagger_docs(directory_path):
    combined_docs = {"paths": {}, "definitions": {}}  # Inclua outras seções necessárias aqui
    for filename in os.listdir(directory_path):
        if filename.endswith('.yaml'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r') as file:
                part = yaml.safe_load(file)
                # Atualize combined_docs com todo o conteúdo relevante de part
                for key, value in part.items():
                    if key in combined_docs:
                        combined_docs[key].update(value)
                    else:
                        combined_docs[key] = value
    return combined_docs

# Diretório que contém os arquivos YAML da documentação Swagger
swagger_docs_dir = os.path.join(os.path.dirname(__file__), 'swagger')
swagger_template = load_and_combine_swagger_docs(swagger_docs_dir)

swagger = Swagger(app, template=swagger_template)

@app.route('/')
def index():
    return redirect("/apidocs/")

# Atualização das regras de URL para usar as funções de rota corretas
app.add_url_rule('/consulta_cpf', 'consulta_cpf', consulta_cpf_route, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
