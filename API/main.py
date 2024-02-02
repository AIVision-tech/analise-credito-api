from flask import Flask, redirect
from flasgger import Swagger

from swagger_config import swagger_config
from auth_service.auth import create_token
from protected_service.protected import protected_route
from sentiment_service.sentiment import analyze

app = Flask(__name__)
swagger = Swagger(app, config=swagger_config)


@app.route('/')
def index():
    return redirect("/apidocs/")


app.add_url_rule('/token', 'create_token', create_token, methods=['POST'])
app.add_url_rule('/protected', 'protected_route', protected_route, methods=['GET'])
app.add_url_rule('/sentiment', 'analyze', analyze, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)