from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotory_fairy_tale_generator import FairyTaleGenerator
from dotory_fairy_tale_image_style_transferer import StyleTransferer
from PIL import Image
from datetime import datetime
import os
import random

def get_extenstion_of_file_name(file_name):
    return file_name.split('.')[-1]

class App:
    def __init__(self):
        app = Flask(__name__)
        CORS(app)

        app.config['JSON_AS_ASCII'] = False

        fairy_tale_generator = FairyTaleGenerator(
            'generator_config_20220327/labeled_5sentence_344_checkpoint',
            'generator_config_20220327/labeled_first_sentence_344.txt',
            'generator_config_20220327/filtering.txt',
        )
        style_transferer = StyleTransferer()

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
        
        @app.route('/v1/fairy-tale-images', methods=('POST', ))
        def route_fairy_tale_images():
            working_dir_path = os.getcwd()
            image_dir_path = working_dir_path + "/resources/temp_image/"
            datetime_string = datetime.today().strftime("%Y%m%d%H%M%S")
            file = request.files['image']
            file_path = image_dir_path + datetime_string + "-" + file.filename
            os.makedirs(image_dir_path, exist_ok=True)
            file.save(file_path)

            style_image = Image.open('resources/image/abstract-image-' + str(random.randrange(1, 29)) + '.jpeg').convert('RGB')
            content_image = Image.open(file_path).convert('RGB')
            style_transfered_image = style_transferer.transfer(style_image, content_image)
        
            result_image_dir_path = working_dir_path + "/resources/result_image/"
            result_file_path = result_image_dir_path + datetime_string + "-" + file.filename
            os.makedirs(result_image_dir_path, exist_ok=True)
            style_transfered_image.save(result_file_path)

            return send_file(result_file_path, mimetype='image/' + get_extenstion_of_file_name(file.filename))
        
        @app.route('/v1/fairy-tale-first-sentences', methods=('POST', ))
        def route_fairy_tale_first_sentence():
            theme_name = request.json['theme_name']
            character1_name = request.json['character1_name']
            character2_name = request.json['character2_name']
            output_sentence = fairy_tale_generator.generate_first_sentences(theme_name, character1_name, character2_name)
            return jsonify({
                'data': {
                    'output_sentence': output_sentence,
                },
            })
        
        @app.route('/v1/fairy-tale-sentences', methods=('POST', ))
        def route_fairy_tale_sentences():
            input_sentence = request.json['sentence']
            character1_name = request.json['character1_name']
            character2_name = request.json['character2_name']
            encoded = request.json['encoded']
            output_sentences, encoded = fairy_tale_generator.generate_sentence(input_sentence, character1_name, character2_name)
            return jsonify({
                'data': {
                    'output_sentences': output_sentences,
                    'output_encoded': encoded,
                },
            })
        
        self.app = app
    
    def run(self, host, port, debug):
        self.app.run(host=host, port=port, debug= debug)
