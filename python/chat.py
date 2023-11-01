import os
import sys
import gradio as gr
import copy
import time
from llama_cpp import Llama

model_name_or_path = "mmnga/japanese-stablelm-instruct-gamma-7b-gguf"
model_basename = "japanese-stablelm-instruct-gamma-7b-q8_0.gguf" 

if len(sys.argv) > 2:
    model_name_or_path = sys.argv[1]
    model_basename = sys.argv[2]

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
#        repeat_penalty=1.1,
        repeat_penalty=1.8,
        max_tokens=1024,
        stop=[
            "ASSISTANT:",
            "USER:",
            "SYSTEM:",
        ],
        stream=True,
    )
    for out in output:
        stream = copy.deepcopy(out)
        temp += stream["choices"][0]["text"]
        yield temp

    history = ["init", input_prompt]


demo = gr.ChatInterface(
    generate_text,
    title="Japanese chatbot using llama-cpp-python",
    description="",
    examples=["日本の四国にある県名を挙げてください。"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Remove last",
    clear_btn="Clear all",
)
demo.queue(max_size=5)
demo.launch(debug=True, share=True)
