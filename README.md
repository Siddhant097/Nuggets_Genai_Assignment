<h1 align="center">Zomato Gen AI Internship Assignment</h1>

# Restaurant Data Scraper & RAG-based Chatbot

-----

## 🎯 Overview
This project demonstrates an end-to-end Generative AI solution tailored for Zomato, marrying robust web scraping, data engineering, and advanced Retrieval-Augmented Generation (RAG) techniques. By extracting real-time restaurant data and indexing it into a vector store, we empower a chatbot to deliver precise, contextual responses to complex natural language queries about menus, dietary features, pricing, and more.
Nuggets_Gen_ai_Walkthrough Video-https://www.youtube.com/watch?v=1bnndOWC38M

Demo Rag Bot Video-https://youtu.be/oDLkKVLB3Dk

<details>
<summary><strong>Key Objectives</strong></summary>

1. **Comprehensive Web Scraping**: Gather menus, pricing, and features from 5–10 diverse restaurants.
2. **Data Processing & Knowledge Base**: Clean, normalize, embed, and efficiently index scraped data.
3. **RAG Chatbot**: Build a retrieval+generation system that answers user queries with situational awareness.
4. **User Interface**: Provide an accessible CLI or web interface for end-to-end interactions.
</details>

---

## 📦 Project Structure & File Flow
Below is the directory layout and the flow of data from scraping to user response:

```bash
.
├── scraper/                # Web scraping & parsing
│   ├── scraper.py          # Entry point for crawling sites per robots.txt
│   └── parse.py            # HTML parsing & structuring into JSON
├── data/                   # Storage of raw, parsed & processed data
│   ├── raw/                # Raw HTML or JSON dumps
│   ├── parsed/             # Parsed JSON/CSV intermediate files
│   └── processed/          # Tokenized, cleaned dataset + FAISS index
├── scripts/                # ETL from parsed -> processed
│   └── create_docs.py      # Cleans, normalizes, generates embeddings, builds FAISS index
├── rag/                    # RAG architecture implementation
│   ├── retriever.py        # FAISS + DPR retrieval logic
│   ├── generator.py        # RAG model generation logic
│   ├── index.py            # High-level orchestration: retrieve → generate
│   └── utils.py            # Shared helper functions
├── chatbot/                # User-facing interface
│   ├── __init__.py
│   └── chat.py             # CLI or Streamlit/Gradio integration
├── docs/                   # Supplementary design & diagrams
│   ├── design.md           # Architecture diagrams & design rationale
│   └── architecture_flow.png  # (Placeholder) System flow diagram
├── requirements.txt        # Python dependencies
└── README.md               # This document
```

> **Flowchart: End‑to‑End Process**  
> 1. **Scraper** → 2. **Parsing & Cleaning** → 3. **Embedding & Indexing** → 4. **Retrieval** → 5. **Generation** → 6. **User Response**

![System Architecture Flowchart](docs/architecture_flow.png)

---

## 🔍 Component Deep Dive

### 1. Web Scraper
- **Objective**: Extract comprehensive restaurant details, including:
  - Name, location, contact, and operating hours
  - Menu items: descriptions, prices, dietary flags (vegetarian, vegan, gluten‑free)
  - Special features: spice levels, allergen warnings
- **Key Files**:
  - `scraper/scraper.py`: Performs site-specific or generic crawling. Honors `robots.txt`, with retry logic and rate-limiting.
  - `scraper/parse.py`: Converts HTML to structured JSON, handling inconsistent markup with fallback parsers.
- **Error Handling**: Exponential backoff, logging of failures, and resilience to schema changes.

### 2. Knowledge Base Creation
- **Objective**: Transform parsed data into a searchable, vectorized knowledge base.
- **Steps**:
  1. **Cleaning**: Remove HTML artifacts, unify measurement units, correct typos.
  2. **Normalization**: Lowercasing, punctuation handling, stopword removal.
  3. **Embedding**: Use sentence-transformers to convert menu sections into dense vectors.
  4. **Indexing**: Store vectors in FAISS for sub-second similarity search.
- **Key File**: `scripts/create_docs.py` orchestrates the above pipeline and writes:
  - `data/processed/hf_dataset/` (Hugging Face dataset)
  - `data/processed/faiss.index`

### 3. RAG-based Chatbot
- **Architecture**:
  1. **Retriever** (`rag/retriever.py`): Given a query, fetch top‑k relevant passages from FAISS.
  2. **Generator** (`rag/generator.py`): Feed retrieved context and query into the RAG model (`facebook/rag-sequence-nq`).
  3. **Orchestrator** (`rag/index.py`): Manage end‑to‑end flow, including conversation history tracking.
- **Capabilities**:
  - **Menu Lookup**: Availability, descriptions, pricing
  - **Feature Comparison**: Veg vs. non‑veg, spice levels across restaurants
  - **Dietary Queries**: Gluten‑free, nut‑free, vegan options
  - **Follow‑Ups**: Uses prior dialogue for context
- **Edge Cases**: Detect out-of-scope queries and respond gracefully with fallback prompts.

### 4. User Interface
- **Options**:
  - **CLI**: Simple terminal-based input/output (`chatbot/chat.py`).
  - **Web UI** (optional): Gradio or Streamlit for richer interactions.
- **Features**:
  - Clear startup instructions, help command, and exit keywords.
  - Display of retrieved context snippets for transparency.

---

## ⚙️ Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/zomato-gen-ai-internship.git
   cd zomato-gen-ai-internship
   ```
2. **Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   .\\venv\\Scripts\\activate # Windows
   ```
3. **Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Scraper**
   ```bash
   python scraper/scraper.py
   ```
5. **Build Knowledge Base**
   ```bash
   python scripts/create_docs.py
   ```
6. **Launch Chatbot**
   ```bash
   python chatbot/chat.py
   ```

---

## 🛠️ Technical Highlights
- **Data Pipeline**: Modular ETL ensures easy extension to more sites.
- **Indexing**: FAISS integration for instant vector search.
- **Generative AI**: Leverages trusted public RAG models with minimal fine-tuning.
- **Scalability**: Incremental index updates and containerization-ready

---

## 🏆 Challenges & Solutions
| Challenge                             | Solution                                         |
|---------------------------------------|--------------------------------------------------|
| Heterogeneous HTML structures         | Built adaptable parsers with multiple fallback rules |
| Inconsistent menu formatting          | Applied regex-based normalization and schema validation |
| Query ambiguity and out-of-scope asks | Contextual fallbacks and clarifying follow-up prompts |

---

## 🚀 Future Work & Improvements
1. **Automated Scheduler**: Periodic scraping and index refreshing via cron or Airflow.
2. **Model Fine‑tuning**: Domain-specific training on Q&A pairs from restaurant chat logs.
3. **Web Deployment**: Dockerize and host on cloud for 24/7 availability.
4. **Analytics Dashboard**: Monitor query trends and system performance.

---

## 📦 Deliverables
- **GitHub Repo**: Complete, well-documented code.
- **Scraped Dataset**: JSON/CSV + FAISS index.
- **Docs**: Design, schemas, and developer notes.
- **Demo Video**: ≤3-minute walkthrough with sample interactions.


> **Supervisor**: garvit.bhardwaj@zomato.com

---

## 📄 License
Licensed under the MIT License. See [LICENSE](LICENSE) for details.

