from flask import Flask, redirect
from flasgger import Swagger
import yaml
import os

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
swagger_docs_dir = os.path.join(os.path.dirname(__file__), 'Swagger')
swagger_template = load_and_combine_swagger_docs(swagger_docs_dir)

swagger = Swagger(app, template=swagger_template)

print("Caminho do diretório Swagger:", swagger_docs_dir)
print("Arquivos no diretório Swagger:", os.listdir(swagger_docs_dir))


@app.route('/')
def index():
    return redirect("/apidocs/")

# Use a porta fornecida pelo ambiente do Vercel ou padrão 5000 se não especificada
port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
