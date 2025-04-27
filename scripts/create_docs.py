# File: scripts/create_docs.py

import os
import json
import torch
from datasets import Dataset
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer

# 1. Paths
PARSED_DIR    = os.path.join("data", "parsed")
PROCESSED_DIR = os.path.join("data", "processed")
DOCS_JSON     = os.path.join(PROCESSED_DIR, "docs.json")
HF_DS_DIR     = os.path.join(PROCESSED_DIR, "hf_dataset")

# 2. Ensure output dir exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 3. Load each parsed JSON into a record with title & text
records = []
for fn in os.listdir(PARSED_DIR):
    if not fn.endswith(".json"):
        continue
    with open(os.path.join(PARSED_DIR, fn), "r", encoding="utf-8") as f:
        data = json.load(f)
    records.append({
        "title": fn.replace(".json", ""),
        "text": data["text"]
    })
print(f"🔍 Loaded {len(records)} documents from {PARSED_DIR}")

# 4. Create a HuggingFace Dataset
ds = Dataset.from_list(records)

# 5. Load DPR context encoder & tokenizer (768-dim embeddings)
ctx_tok = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
ctx_enc = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

# 6. Compute embeddings for each document
def encode(example):
    inputs = ctx_tok(
        example["text"],
        return_tensors="pt",
        truncation=True,
        padding="longest",
        max_length=512,
    )
    with torch.no_grad():
        out = ctx_enc(**inputs)
    # pooler_output is shape [1, 768]
    return {"embeddings": out.pooler_output.squeeze().tolist()}

ds = ds.map(encode)

# 7. Write out a plain JSON list of {"title","text","embeddings"}
final = [
    {"title": d["title"], "text": d["text"], "embeddings": d["embeddings"]}
    for d in ds
]
with open(DOCS_JSON, "w", encoding="utf-8") as f:
    json.dump(final, f, indent=2, ensure_ascii=False)
print(f"✅ Wrote {len(final)} records to {DOCS_JSON}")

# 8. Save the Dataset for RAG
ds.save_to_disk(HF_DS_DIR)
print(f"✅ HuggingFace Dataset saved to {HF_DS_DIR}")
