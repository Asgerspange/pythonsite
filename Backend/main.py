from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch

app = Flask(__name__)
CORS(app)

class ChatBot:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("t5-large", model_max_length=512, legacy=False)

        self.model = T5ForConditionalGeneration.from_pretrained("t5-large")

    def generate_response(self, prompt, context):
        input_text = f'{context} {prompt}'
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')

        # Add </s> token at the end of the input sequence
        input_ids = torch.cat([input_ids, torch.tensor([[self.tokenizer.eos_token_id]])], dim=-1)

        response = self.model.generate(input_ids, max_length=150, num_beams=16, diversity_penalty=0, num_beam_groups=1, temperature=0.7, no_repeat_ngram_size=2, early_stopping=True, use_cache=True, top_k=50, top_p=0.95, do_sample=False, pad_token_id=0, eos_token_id=1, bos_token_id=0, length_penalty=1.0, num_return_sequences=1, attention_mask=None, decoder_start_token_id=None, forced_bos_token_id=None, forced_eos_token_id=None, head_mask=None, input_embeds=None, labels=None, output_attentions=None, output_hidden_states=None)
        return response


chatbot = ChatBot()

@app.route('/get_chatbot_response/', methods=['GET'])
def get_chatbot_response():
    prompt = request.args.get('prompt', '')
    context = request.args.get('context', '')
    response = chatbot.generate_response(prompt, context)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
