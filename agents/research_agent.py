from .base import call_llm

def run(query: str) -> str:
    prompt = f"Answer this question factually and concisely:\n{query}"
    return call_llm(prompt)