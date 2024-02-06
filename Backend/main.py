from flask import Flask, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from urllib.parse import unquote
import torch

model_name = "JosephusCheung/Guanaco"
fp16_enabled = True  # Set to True for fp16 inference

app = Flask(__name__)
CORS(app)

class ChatBot:
    def __init__(self, model_name, fp16_enabled):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        if fp16_enabled:
            self.model.half()  # Enable fp16 inference

    def generate_response(self, prompt, max_length=100):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        if fp16_enabled:
            input_ids = input_ids.half()  # Convert input to fp16 if enabled
        input_ids = input_ids.to(torch.long)  # Convert input to Long dtype
        response_ids = self.model.generate(input_ids, max_length=max_length, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(response_ids[0], skip_special_tokens=True)
        return response
    
    def get_response(self, prompt):
        response = self.generate_response(prompt)
        return {'response': response}

chatbot = ChatBot(model_name, fp16_enabled)


@app.route('/get_response/<prompt>', methods=['GET'])
def get_response(prompt):
    prompt = unquote(prompt)
    return jsonify(chatbot.get_response(prompt))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
