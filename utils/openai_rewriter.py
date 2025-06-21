# Gọi API, chia chunk, cache, viết lại text
# utils/openai_rewriter.py
import os
import time
import json
import openai
from typing import Dict
import tiktoken

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
Rewrite the following text in a {style_description} style, keeping the original meaning and structure, but using fresh language:

{text}
"""

def load_cache(cache_path: str) -> Dict[int, str]:
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache_path: str, cache_data: Dict[int, str]):
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

def call_openai_api(prompt: str, max_tokens: int = 1500, temperature: float = 0.4, top_p: float = 1.0) -> str:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
            )
            return response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            print(f"OpenAI API error on attempt {attempt + 1}: {e}")
            time.sleep(2 ** attempt)
    raise Exception("Failed after retries.")

def rewrite_text_with_style(raw_text: str, style_description: str, cache_path: str) -> str:
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(raw_text)
    max_tokens_per_chunk = 1500
    cache = load_cache(cache_path)
    rewritten_chunks = []

    total_chunks = (len(tokens) + max_tokens_per_chunk - 1) // max_tokens_per_chunk
    print(f"Total chunks to process: {total_chunks}")

    for i in range(total_chunks):
        if str(i) in cache:
            rewritten_chunks.append(cache[str(i)])
            print(f"Chunk {i+1}/{total_chunks} loaded from cache")
            continue

        chunk_tokens = tokens[i*max_tokens_per_chunk:(i+1)*max_tokens_per_chunk]
        chunk_text = enc.decode(chunk_tokens)

        prompt = PROMPT_TEMPLATE.format(style_description=style_description, text=chunk_text)
        rewritten = call_openai_api(prompt)
        cache[str(i)] = rewritten
        rewritten_chunks.append(rewritten)
        save_cache(cache_path, cache)
        print(f"Chunk {i+1}/{total_chunks} rewritten and saved to cache")

    return "\n\n".join(rewritten_chunks)


def generate_summary(text: str, max_tokens=500):
    prompt = f"Write a concise summary of the following text:\n\n{text}"
    return call_openai_api(prompt, max_tokens=max_tokens, temperature=0.3)
