from flask import Flask, jsonify, request
from flask_cors import CORS
from ctransformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)

model_name = "TheBloke/Guanaco-13B-Uncensored-GGUF"
model_file = "guanaco-13b-uncensored.Q5_K_S.gguf"
llm = AutoModelForCausalLM.from_pretrained(model_name, model_file=model_file, model_type="llama", gpu_layers=10, hf=True)
tokenizer = AutoTokenizer.from_pretrained(llm)

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    human_prompt = data['message']
    
    inputs = tokenizer(human_prompt, return_tensors="pt")

    with torch.no_grad():
        # Adjust topk and topp parameters here
        output = llm.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=150,  # Adjust max_length as needed
            do_sample=True,
            top_k=50,  # Adjust topk as needed
            top_p=0.95,  # Adjust topp as needed
            temperature=1.0  # Adjust temperature as needed
        )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return jsonify({"response": generated_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
