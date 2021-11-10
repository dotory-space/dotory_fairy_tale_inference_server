from flask import Flask, request, jsonify
from flask_cors import CORS
from dotory_fairy_tale_generator import FairyTaleGenerator

class App:
    def __init__(self):
        app = Flask(__name__)
        CORS(app)

        fairy_tale_generator = FairyTaleGenerator('trained/checkpoint.tar', 'trained/', 'trained/config.json')

        @app.route('/', methods=('GET', ))
        def route_get_home():
            sentences = fairy_tale_generator.generate('옛날에 한 소녀가 살고 있었어요.')
            return sentences

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
