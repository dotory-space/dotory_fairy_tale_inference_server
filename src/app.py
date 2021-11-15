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
            return jsonify({
                'data': 'HELLO DOTORY'
            })

        @app.route('/v1/test1', methods=('GET', ))
        def route_test1():
            sentence = '옛날에 한 소녀가 살고 있었어요.'
            sentences = fairy_tale_generator.generate(sentence)
            print(sentences)
            return jsonify({
                'data': {
                    'input_sentence': sentence,
                    'output_sentences': sentences,
                    'encoded_output_sentence': sentences[0].decode('utf8'),
                    'output_sentence_type': type(sentences[0]),
                },
            })
        
        @app.route('/v1/test2', methods=('GET', ))
        def route_test2():
            sentence = request.args.get('sentence')
            sentences = fairy_tale_generator.generate(sentence)
            sentences = [s.decode('utf8') for s in sentences]
            return jsonify({
                'data': sentences,
            })
        
        @app.route('/v1/test3', methods=('POST', ))
        def route_test3():
            sentence = request.json['sentence']
            sentences = fairy_tale_generator.generate(sentence)
            return jsonify({
                'data': sentences,
            })
        
        self.app = app
    
    def run(self, host, port, debug):
        self.app.run(host=host, port=port, debug= debug)
