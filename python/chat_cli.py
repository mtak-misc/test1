import os
import time
from llama_cpp import Llama
model_name_or_path = "mmnga/japanese-stablelm-instruct-gamma-7b-gguf"
model_basename = "japanese-stablelm-instruct-gamma-7b-q8_0.gguf" 

from huggingface_hub import hf_hub_download

model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

llm = Llama(
    model_path=model_path,
    n_threads=2, # CPU cores
    n_batch=512, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    n_gpu_layers=43, # Change this value based on your model and your GPU VRAM pool.
    n_ctx=4096, # Context window
)

history = []

#system_message = """
#あなたはAIアシスタントです。
#"""

system_message = """
SYSTEM: You are an Assistant, a helpful, respectful, honest and highly intelligent assistant.
"""

def generate_text(message, history):
    temp = ""
    input_prompt = f"{system_message}"
    for interaction in history:
        input_prompt = input_prompt + "\nUSER: " + str(interaction[0]) + "\nASSISTANT: " + str(interaction[1])

    input_prompt = input_prompt + "\nUSER: " + str(message) + "\nASSISTANT: "

    output = llm.create_completion(
        input_prompt,
        temperature=0.7,
        top_p=0.3,
        top_k=40,
        repeat_penalty=1.1,
        max_tokens=1024,
        stop=[
            "ASSISTANT:",
            "USER:",
            "SYSTEM:",
        ],
        stream=False,
    )
    print('bot: '+output["choices"][0]["text"])
    history = ["init", input_prompt]

while True:
    message = input('user: ')
    generate_text(message, history)
