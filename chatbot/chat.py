import os
from dotenv import load_dotenv
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
from datasets import load_from_disk

# Load Hugging Face token (if you need to authenticate private models)
load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')  # not used for public RAG checkpoints

MODEL_NAME = "facebook/rag-sequence-nq"

def init_rag():
    # Paths where your docs and FAISS index live
    dataset_path = os.path.join("data", "processed", "hf_dataset")
    index_path   = os.path.join("data", "processed", "faiss.index")

    # Load HF dataset (must contain an 'embeddings' float32[] column)
    dataset = load_from_disk(dataset_path)

    # Initialize RAG retriever over your custom passages + index
    retriever = RagRetriever.from_pretrained(
        MODEL_NAME,
        index_name="custom",
        passages_path=dataset_path,
        index_path=index_path,
    )

    # Load tokenizer + sequence generator with that retriever
    tokenizer = RagTokenizer.from_pretrained(MODEL_NAME)
    model     = RagSequenceForGeneration.from_pretrained(
        MODEL_NAME,
        retriever=retriever,
    )
    return tokenizer, model

def chat_loop(tokenizer, model):
    print("Welcome to the RAG Chatbot! (type 'exit' to quit)\n")
    while True:
        query = input("You: ")
        if query.strip().lower() in ('exit', 'quit'):
            print("Goodbye!")
            break

        # Prepare inputs for RAG with the standard tokenizer API
        inputs = tokenizer(
            [query],
            return_tensors='pt',
            truncation=True,
            padding=True,
            return_token_type_ids=False
        )

        # Generate answer (grounded in retrieved passages)
        generated = model.generate(**inputs)
        answer = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

        print(f"\nBot: {answer}\n")

if __name__ == '__main__':
    tokenizer, model = init_rag()
    chat_loop(tokenizer, model)
