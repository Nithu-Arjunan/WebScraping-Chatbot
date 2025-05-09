from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pinecone import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# -------------------- ENV SETUP ----------------------
load_dotenv()

# -------------------- FASTAPI INIT ----------------------
app = FastAPI(title="AI Chatbot Backend", description="Retrieve answers using RAG pipeline", version="1.0")

# -------------------- PINECONE & LLM SETUP ----------------------
pc = Pinecone(api_key="PINECONE_API_KEY")
index = pc.Index("ragchatbot") 
embeddings = SentenceTransformer('all-MiniLM-L6-v2')
llm = ChatGroq(
    model="llama3-70b-8192",  
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# -------------------- REQUEST MODEL ----------------------
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3  # Default top_k = 3, can be overridden by user


# -------------------- API ENDPOINT ----------------------
@app.post("/query")
def query_chatbot(request: QueryRequest):
    try:
        # Step 1: Embed user query
        #query_embedding = embeddings.embed_query(request.question)
        query_embedding = embeddings.encode(request.question).tolist()
        print(f"Type of query_embedding: {type(query_embedding)}")

        # Step 2: Query Pinecone
        result = index.query(
            vector=query_embedding,
            top_k=request.top_k,
            include_metadata=True
        )

        if not result.matches:
            raise HTTPException(status_code=404, detail="No relevant chunks found for this query.")

        # Step 3: Prepare context from retrieved chunks
        context = "\n\n".join([match.metadata["text"] for match in result.matches])

        # Step 4: Create Prompt Template
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are a helpful assistant. Use ONLY the provided context to answer the question. "
                "Do NOT use external knowledge.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer:"
            )
        )

        # Step 5: Call LLM with constructed prompt
        chain = prompt | llm
        response = chain.invoke({"context": context, "question": request.question})

        return {
            "question": request.question,
            "answer": response.content,
            "context_used": context
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))