# index.py
from flask import Flask, redirect
from flask_cors import CORS
from flasgger import Swagger
import yaml
import os
from services.consulta_cpf import consulta_cpf_route
from services.consulta_cnpj import consulta_cnpj_route



app = Flask(__name__)

cors = CORS(app, resources={
    r"/api/*": {
       "origins": ["*"],
       "methods": ["GET", "POST"], 
       "allow_headers": ["Content-Type", "Authorization"]
    }
})

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

swagger_docs_dir = os.path.join(os.path.dirname(__file__), 'Swagger')
swagger_template = load_and_combine_swagger_docs(swagger_docs_dir)

swagger = Swagger(app, template=swagger_template)

@app.route('/')
def index():
    return redirect("/apidocs/")


app.add_url_rule('/apidocs/consulta_cpf', view_func=consulta_cpf_route, methods=['POST'])
app.add_url_rule('/apidocs/consulta_cnpj', view_func=consulta_cnpj_route, methods=['POST'])



port = int(os.environ.get("PORT", 5001))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
