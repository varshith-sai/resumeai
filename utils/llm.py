import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_API_TOKEN"),
)

def call_llm(prompt):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.3
    )
    return response.choices[0].message.content
