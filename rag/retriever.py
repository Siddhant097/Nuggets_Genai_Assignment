import json
import torch
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer
from sklearn.metrics.pairwise import cosine_similarity

class Retriever:
    def __init__(self, doc_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
        self.encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base").to(self.device)

        with open(doc_path, "r", encoding="utf-8") as f:
            self.docs = json.load(f)

        self.embeddings = torch.tensor([doc["embeddings"] for doc in self.docs])

    def retrieve(self, query, top_k=3):
        inputs = self.tokenizer(query, return_tensors="pt", truncation=True, padding=True, max_length=64).to(self.device)
        with torch.no_grad():
            q_emb = self.encoder(**inputs).pooler_output.cpu()

        sims = cosine_similarity(q_emb, self.embeddings)[0]
        top_indices = sims.argsort()[-top_k:][::-1]

        results = []
        for i in top_indices:
            results.append(self.docs[i])
        return results
