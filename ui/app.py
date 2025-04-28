import streamlit as st
from chatbot import init_rag

st.set_page_config(page_title="🍽️ Restaurant RAG Chatbot")
st.title("🍽️ Restaurant RAG Chatbot")

# Load model once
@st.cache(allow_output_mutation=True)
def load_model():
    return init_rag()

tokenizer, model = load_model()

if 'history' not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask about any restaurant:")
if st.button("Send") and query:
    st.session_state.history.append(("You", query))
    inputs = tokenizer([query], padding=True, truncation=True, return_tensors='pt')
    print(inputs)
    inputs.pop("token_type_ids", None)
    outputs = model.generate(**inputs)
    answer = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    st.session_state.history.append(("Jarvis(Bot)", answer))

for speaker, text in st.session_state.history:
    st.markdown(f"**{speaker}:** {text}")


# — Sidebar —
with st.sidebar:
    st.title("🍽️ Zomato RAG Bot")
    st.write("""
    **How to use:**
    1. Ask anything about the restaurants in Lucknow.
    2. Menus, prices, veg/non-veg, hours, contacts—all covered.
    3. Examples:
       - *“Veg appetizers under ₹200”*  
       - *“Address of Barbeque Nation Gomti Nagar”*
    """)
    st.write("---")
    st.write("**Made by:** Siddhant Mukund")


    st.markdown(
    """
    <style>
      /* 1) Color Palette */
      :root {
        --bg: #1e1e1e;
        --surface: #2c2c2c;
        --primary: #bb86fc;
        --on-surface: #e0e0e0;
        --border: #3c3c3c;
      }

      /* 2) Global background and font */
      html, body, .stApp {
        background-color: var(--bg);
        color: var(--on-surface);
        font-family: 'Segoe UI', sans-serif;
      }

      /* 3) Sidebar styling */
      [data-testid="stSidebar"] {
        background-color: var(--surface);
        color: var(--on-surface);
      }
      [data-testid="stSidebar"] a, [data-testid="stSidebar"] .stMarkdown a {
        color: var(--primary) !important;
      }
      [data-testid="stSidebar"] .stButton>button {
        background-color: var(--primary) !important;
        color: var(--bg) !important;
        border: none;
      }

      /* 4) Header bar */
      header, .css-12oz5g7.e1fqkh3o3 {
        background-color: var(--surface) !important;
      }
      header .css-1v0mbdj.ehz0tkn1, header .css-1v0mbdj.ehz0tkn1 * {
        color: var(--on-surface) !important;
      }

      /* 5) Main content area padding */
      .css-18e3th9 {
        padding: 2rem 3rem;
      }

      /* 6) Chat container */
      .chat-container {
        max-height: 65vh;
        overflow-y: auto;
        padding: 1.5rem;
        background: var(--surface);
        border-radius: 12px;
        border: 1px solid var(--border);
      }

      /* 7) Message bubbles */
      .bubble {
        padding: 0.75rem 1rem;
        border-radius: 16px;
        margin: 0.5rem 0;
        max-width: 70%;
        line-height: 1.4;
      }
      .user {
        background-color: var(--primary);
        color: var(--bg);
        margin-left: auto;
      }
      .bot {
        background-color: var(--border);
        color: var(--on-surface);
        margin-right: auto;
      }

      /* 8) Text input box */
      .stTextInput>div>div>input {
        background: var(--surface);
        color: var(--on-surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.5rem 1rem;
      }
      .stTextInput>div>div>input:focus {
        outline: none;
        border-color: var(--primary);
      }

      /* 9) Send button */
      .stButton>button {
        background-color: var(--primary) !important;
        color: var(--bg) !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
      }
      .stButton>button:hover {
        background-color: #9b6ce1 !important;
      }

      /* 10) Scrollbar styling */
      ::-webkit-scrollbar {
        width: 8px;
      }
      ::-webkit-scrollbar-track {
        background: var(--surface);
        border-radius: 4px;
      }
      ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
      }
    </style>
    """,
    unsafe_allow_html=True
)
