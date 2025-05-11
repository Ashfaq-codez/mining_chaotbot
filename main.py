import openai
from fastapi import FastAPI
from pydantic import BaseModel
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (modify as needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load embedding model (Sentence Transformers)
model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')

# Load FAISS index and metadata
try:
    index_path = faiss.read_index("mining_index.faiss")
    with open("mining_chunks.json", "r") as f:
        chunks = json.load(f)
except Exception as e:
    print(f"Error loading FAISS index or chunks: {e}")
    index_path = None
    chunks = []

# Define the request model for the query
class QueryRequest(BaseModel):
    query: str

# Function to generate a response from OpenAI
async def generate_response(query):
    try:
        # Set OpenAI API key (move this to an environment variable in production)
        openai.api_key = ''

        # Use the new method for chat completions
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ]
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Define the endpoint for asking questions
@app.post("/ask")
async def ask_question(req: QueryRequest):
    # Generate response from OpenAI
    response = await generate_response(req.query)

    if index_path and chunks:
        # Query embedding and search FAISS index
        query_embedding = model.encode([req.query])
        D, I = index_path.search(np.array(query_embedding).astype("float32"), k=5)
        best_chunk = chunks[I[0][0]]

        return {
            "section": best_chunk['section'],
            "content": best_chunk['content'],
            "response": response
        }
    else:
        return {
            "section": "N/A",
            "content": "Index not loaded. Please generate FAISS index first.",
            "response": response
        }

# Run the FastAPI app with Uvicorn (if this file is executed directly)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
