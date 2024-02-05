from flask import Flask, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from urllib.parse import unquote
import torch
import os

model_name = "microsoft/DialoGPT-large"

# Define the directory where you want to save the model
cache_dir = "E:/Hugging"

# Download and load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, local_files_only=True)

# Download and load the model
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir, local_files_only=True)

app = Flask(__name__)
CORS(app)

class ChatBot:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir, local_files_only=True)

    def generate_response(self, prompt, max_length=100):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        response_ids = self.model.generate(input_ids, max_length=max_length, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(response_ids[0], skip_special_tokens=True)
        return response
    
    def get_data(self):
        data = {'message': 'This is data from Flask backend'}
        return jsonify(data)
    
    def get_response(self, prompt):
        response = self.generate_response(prompt)
        return {'response': response}

chatbot = ChatBot(model_name)

@app.route('/get_data', methods=['GET'])
def get_data():
    return chatbot.get_data()

@app.route('/get_response/<prompt>', methods=['GET'])
def get_response(prompt):
    prompt = unquote(prompt)
    return chatbot.get_response(prompt)


if __name__ == '__main__':
    app.run(debug=True)
