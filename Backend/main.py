from transformers import AutoModel, GPT2Config
import torch

gpt_model = AutoModel.from_pretrained("gpt2")
gpt_model.save_pretrained("gpt2")
gpt_config = GPT2Config.from_pretrained("gpt2")
print(type(gpt_config))