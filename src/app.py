from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotory_fairy_tale_generator import FairyTaleGenerator
from dotory_fairy_tale_image_style_transferer import StyleTransferer
from PIL import Image
from datetime import datetime
import os

def get_extenstion_of_file_name(file_name):
    return file_name.split('.')[-1]


class App:
    def __init__(self):
        app = Flask(__name__)
        CORS(app)

        app.config['JSON_AS_ASCII'] = False

        fairy_tale_generator = FairyTaleGenerator('trained/checkpoint.tar', 'trained/', 'trained/config.json')
        style_transferer = StyleTransferer(Image.open('resources/image/abstract-image-13.jpeg'))

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
        
        @app.route('/v1/test2', methods=('POST', ))
        def route_test2():
            image_dir_path = "resources/temp_image/"
            datetime_string = datetime.today().strftime("%Y%m%d%H%M%S")
            file = request.files['image']
            file_path = image_dir_path + datetime_string + "-" + file.filename
            os.makedirs(image_dir_path, exist_ok=True)
            file.save(file_path)

            style_transfered_image = style_transferer.transfer(Image.open(file_path))
        
            result_image_dir_path = "resources/result_image"
            result_file_path = result_image_dir_path + datetime_string + file.filename
            os.makedirs(result_image_dir_path, exist_ok=True)
            style_transfered_image.save(result_file_path)

            return send_file(result_file_path, mimetype='image/' + get_extenstion_of_file_name(file.filename))
        
        
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
