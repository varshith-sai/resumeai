import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def call_llm(prompt):
    api_key = os.getenv("HF_API_TOKEN")
    if not api_key:
        raise ValueError("HF_API_TOKEN is not set. Add your Hugging Face token in Settings.")

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.3
    )
    return response.choices[0].message.content
