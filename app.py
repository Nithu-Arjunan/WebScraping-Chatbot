### ✅ Frontend: Streamlit (frontend/app.py)

import streamlit as st
import requests
import os

st.set_page_config(page_title="⚙️ AI Chat with Scraped Data ", page_icon="🧠", layout="wide")
st.title("⚙️ AI Chat with Scraped Data")
st.caption("💬 Ask anything about the webpage we processed.")
st.markdown("---")

with st.sidebar:
    st.header("🔧 Control Panel")
    show_context = st.toggle("📜 Show Context Used for Answer", value=False)
    top_k = st.slider("📈 Number of Chunks to Fetch (Top-K)", min_value=1, max_value=5, value=3)

st.subheader("💬 Ask Your Question")
query = st.text_input("Type your question below 👇", placeholder="E.g., What is this book about?")
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000/query") # Change in production

def get_answer_from_backend(question, top_k):
    try:
        response = requests.post(API_URL, json={"question": question, "top_k": top_k})
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return None, f"Request failed: {str(e)}"

if st.button("🚀 Get Answer"):
    if not query.strip():
        st.error("❌ Please type a valid question!")
    else:
        with st.spinner("🤖 Thinking..."):
            data, error = get_answer_from_backend(query, top_k)
        if error:
            st.error(error)
        else:
            st.success("✅ Answer Generated:")
            st.markdown(f"**💡 Answer:** {data['answer']}")
            if show_context:
                st.subheader("📜 Context Used to Generate Answer")
                st.write(data['context_used'])
st.markdown("---")
st.markdown("🎓  AI-Powered Web Scraping**")