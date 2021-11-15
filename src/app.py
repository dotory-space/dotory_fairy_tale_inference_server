from flask import Flask, request, jsonify
from flask_cors import CORS
from dotory_fairy_tale_generator import FairyTaleGenerator

class App:
    def __init__(self):
        app = Flask(__name__)
        CORS(app)

        app.config['JSON_AS_ASCII'] = False

        fairy_tale_generator = FairyTaleGenerator('trained/checkpoint.tar', 'trained/', 'trained/config.json')

        @app.route('/', methods=('GET', ))
        def route_get_home():
            return jsonify({
                'data': 'HELLO DOTORY'
            })

        @app.route('/v1/test1', methods=('GET', ))
        def route_test1():
            input_sentence = '옛날에 한 소녀가 살고 있었어요.'
            output_sentences = fairy_tale_generator.generate(input_sentence)

            return jsonify({
                'data': {
                    'input_sentence': input_sentence,
                    'output_sentences': output_sentences,
                },
            })
        
        @app.route('/v1/test2', methods=('GET', ))
        def route_test2():
            input_sentence = request.args.get('sentence')
            output_sentences = fairy_tale_generator.generate(input_sentence)
            
            return jsonify({
                'data': {
                    'input_sentence': input_sentence,
                    'output_sentences': output_sentences,
                },
            })
        
        @app.route('/v1/test3', methods=('POST', ))
        def route_test3():
            input_sentence = request.json['sentence']
            output_sentences = fairy_tale_generator.generate(input_sentence)
            return jsonify({
                'data': {
                    'input_sentence': input_sentence,
                    'output_sentences': output_sentences,
                },
            })
        
        self.app = app
    
    def run(self, host, port, debug):
        self.app.run(host=host, port=port, debug= debug)
