from flask import Flask, request, jsonify
from flask_cors import CORS
from dotory_fairy_tale_generator import get_model, get_tokenizer, generate_sentences
import torch

class App:
    def __init__(self):
        app = Flask(__name__)
        CORS(app)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = get_model('model.pt', 'config.json', device)
        tokenizer = get_tokenizer()

        @app.route('/', methods=('GET', ))
        def route_get_home():
            sentences = generate_sentences(model, tokenizer, '옛날에 한 소녀가 살고 있었어요.', device)
            return 'dotory fairy tale generator server'

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
