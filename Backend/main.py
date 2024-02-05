from flask import Flask
from flask_cors import CORS
from transformers import pipeline
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

class ChatBot:
    def __init__(self):
        self.pipe = pipeline("text-generation", model="PygmalionAI/pygmalion-6b")

    def generate_response(self, prompt):
        response = self.pipe(prompt, max_length=5000, pad_token_id=self.pipe.tokenizer.eos_token_id)
        return response[0]['generated_text']

    def get_response(self, prompt):
        response = self.generate_response(prompt)
        return {'response': response}

chatbot = ChatBot()

@app.route('/get_response/<prompt>', methods=['GET'])
def get_response(prompt):
    prompt = unquote(prompt)
    return chatbot.get_response(prompt)

if __name__ == '__main__':
    app.run(debug=True)
