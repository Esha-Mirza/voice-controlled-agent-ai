from .base import call_llm

def run(text: str) -> str:
    prompt = f"Summarize this in 3 bullet points:\n{text}"
    return call_llm(prompt)