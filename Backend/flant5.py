from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto")

input_text = "translate English to German: How old are you?"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cpu")

outputs = model.generate(input_ids, max_length=256)

# Print outputs to inspect
print(outputs)

# Decode and print the first output
print(tokenizer.decode(outputs[0]))