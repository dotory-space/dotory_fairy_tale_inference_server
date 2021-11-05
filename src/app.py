from flask import Flask, request, jsonify
from flask_cors import CORS

class App:
    def __init__(self):
        app = Flask(__name__)
        CORS(app)

        @app.route('/', methods=('GET', ))
        def route_get_home():
            return 'dotory inference server'

        @app.route('/v1/models/model/infer', methods=('POST', ))
        def route_post_models_model_infer():
            inputs = request.json['inputs']
            outputs = ""

            return jsonify({
                'inputs': 'hello'          
            })
        
        self.app = app
    
    def run(self, host, port, debug):
        self.app.run(host=host, port=port, debug= debug)