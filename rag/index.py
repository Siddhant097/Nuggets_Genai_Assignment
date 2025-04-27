import os
import torch
import json
import faiss
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer

MODEL_NAME = 'facebook/dpr-ctx_encoder-single-nq-base'
EMBED_DIM    = 768

# ─── adjust DATA_DIR to point at PROJECT_ROOT/data/processed ──────────────────
# __file__: PROJECT_ROOT/rag/index.py
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR     = os.path.join(PROJECT_ROOT, 'data', 'processed')
INDEX_PATH   = os.path.join(DATA_DIR, 'faiss.index')
DOCS_PATH    = os.path.join(DATA_DIR, 'docs.json')

def load_docs():
    with open(DOCS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_index():
    tokenizer = DPRContextEncoderTokenizer.from_pretrained(MODEL_NAME)
    model     = DPRContextEncoder.from_pretrained(MODEL_NAME)
    model.eval()

    docs  = load_docs()
    texts = [doc['text'] for doc in docs]

    # Batched embedding
    embeddings = []
    batch_size = 16
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            inputs      = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )
            batch_emb   = model(**inputs).pooler_output
            embeddings.append(batch_emb.cpu())

    embeddings = torch.cat(embeddings, dim=0).numpy()

    # Build and save FAISS index
    index = faiss.IndexFlatIP(EMBED_DIM)
    index.add(embeddings)

    os.makedirs(DATA_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    print(f"✅ FAISS index rebuilt and saved to {INDEX_PATH}")

if __name__ == '__main__':
    build_index()
