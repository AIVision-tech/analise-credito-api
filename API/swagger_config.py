swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'main',
            "route": '/main.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True, 
            "title": "API Template"
        }
     ],
    "title": "API - Avatar de Atendimento",
    "version": "1",
    "description": """ Base de template para a API da empresa Ai Vision""",
    "termsOfService": "",
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}