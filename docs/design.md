# System Design & Assumptions

## 1. Scraper Module
- Uses `requests` + `BeautifulSoup`.
- Respects `robots.txt` (to add: `robotsparser` checks).
- Writes raw HTML to `/data/raw`.

## 2. Data Processing
- Parse raw HTML → extract menu items, normalize prices, tag dietary flags.
- Output JSON list of docs: `[ { id, text, meta... } ]` in `/data/processed/docs.json`.

## 3. RAG Indexing
- Embeddings via `all-MiniLM-L6-v2`.
- FAISS `IndexFlatIP` for similarity search.

## 4. Chatbot
- HF’s `facebook/rag-token-base` with custom retriever.
- CLI and optional Streamlit UI.
- Basic fallback if no relevant doc is found.

## 5. Future Improvements
- Add images & ratings support.
- Pagination & login-handling for complex sites.
- Caching retrieval layer.