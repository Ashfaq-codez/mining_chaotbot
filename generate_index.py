import json
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os

json_path = "mining_chunks.json"
faiss_index_path = "mining_index.faiss"

def generate_faiss():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["content"] for item in data]

    # Disable parallelism to prevent multiprocessing issues on macOS
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Load sentence transformer model
    model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')
    embeddings = model.encode(texts, show_progress_bar=True)

    # Convert to float32 numpy array for FAISS
    embeddings_np = np.array(embeddings).astype("float32")

    # Create a flat L2 index and add embeddings
    index = faiss.IndexFlatL2(embeddings_np.shape[1])
    index.add(embeddings_np)

    # Save index to a single file
    faiss.write_index(index, faiss_index_path)
    print(f"✅ FAISS index saved as '{faiss_index_path}'")

# ✅ Ensure this block exists
if __name__ == "__main__":
    generate_faiss()
