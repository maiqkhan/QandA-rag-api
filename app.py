from fastapi import FastAPI
import chromadb
import uuid
import os 
import logging 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"

if not USE_MOCK_LLM:
    import ollama

MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
logging.info(f"Using Model: {MODEL_NAME}")

app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
if not USE_MOCK_LLM:
    ollama_client = ollama.Client(host=OLLAMA_HOST)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query(q: str):
    logging.info(f"/query asked: {q}")
    
    results = collection.query(query_texts=[q], n_results= 1)
    context = results["documents"][0][0] if results["documents"] else ""

    if USE_MOCK_LLM:
        answer = {"response": context}
    else:
        answer = ollama_client.generate(
            model=MODEL_NAME,
            prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:",
            
        )

    return {"answer": answer['response']}

@app.post("/add")
def add(text: str):
    logging.info(f"/add received new text (id will be generated)")
    try:
        doc_id = str(uuid.uuid4())

        collection.add(documents = [text], ids=[doc_id])

        return {"status": "success", "message": "Content added to knowledge base", "id": doc_id}
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

