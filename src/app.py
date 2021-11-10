from flask import Flask, request, jsonify
from flask_cors import CORS

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Config
import nltk
from nltk.tokenize import sent_tokenize
import requests
from .hanspell import spell_checker

class FairyTaleGenerator:
    def __init__(self, checkpoint_path, tokenizer_dir_path, config_file_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        checkpoint = torch.load(checkpoint_path, map_location = self.device)

        self.tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_dir_path)

        self.model = GPT2LMHeadModel(GPT2Config.from_json_file(config_file_path))
        self.model.load_state_dict(checkpoint['model'])
        self.model.to(self.device)

        nltk.download('punkt')

    def translate_kakao(self, text, source, target):
        url = "https://translate.kakao.com/translator/translate.json"

        headers = {
            "Referer": "https://translate.kakao.com/",
            "User-Agent": "Mozilla/5.0"
        }

        data = {
            "queryLanguage": source,
            "resultLanguage": target,
            "q": text
        }

        resp = requests.post(url, headers=headers, data=data)
        data = resp.json()
        output = data['result']['output'][0][0]
        return output

    def generate(self, input_sentence):
        encoded = torch.tensor(self.tokenizer.encode(input_sentence)).unsqueeze(0).to(self.device)
        generated = self.model.generate(encoded, do_sample=True, top_p=0.9, num_return_sequences=3, max_length=200, min_length=1, temperature=0.6, pad_token_id=self.tokenizer.eos_token_id).to(self.device)  # length_penalty=10, 
        decoded = [self.tokenizer.decode(generated[i]) for i in range(3)]  # decode
        output_eng = [decoded[i].replace(input_sentence, '').lstrip(' ') for i in range(3)]  # input 중복 문장 제거
        output_eng = [sent_tokenize(output_eng[i])[0] for i in range(3)]  # 첫 번째 문장 분리
        output_kor = [self.translate_kakao(output_eng[i], 'en', 'ku') for i in range(3)]  # papgo : ko, kakao : ku (ku : 높임말 문체 in kakao)
        output_kor = [spell_checker.check(output_kor[i]).checked for i in range(3)]  # 맞춤법 검사

        return output_kor


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
