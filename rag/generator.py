from transformers import pipeline

class Generator:
    def __init__(self):
        self.generator = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=150)

    def generate(self, context, query):
        prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        response = self.generator(prompt)[0]['generated_text']
        return response.strip()
