import numpy as np
import faiss
import pandas as pd
import os
from global_vars import all_categories

"""
Purpose:
    - Load the saved CLIP embeddings and metadata.
    
    - Build a FAISS index using the embeddings for similarity search.
        - Should allow us to retrieve the top-k most similar images based on cosine similarity between embeddings
        - I don't think too hard about this...we just add the embeddings and FAISS will handle the rest to make it efficient for search lol
    
    - Save the FAISS index to disk for later use during user search queries.
"""

metadata = pd.read_csv("data/metadata.csv")
base_faiss_index_path = "data\\faiss\\"
embeddings_path = "data\\embeddings\\"

def build_faiss_index() -> None:
    """
    Builds a FAISS index for each clothing category using the corresponding CLIP embeddings.
    All indices are saved under data/faiss/...
    (i.e. FAISS index for tops uses embeddings in the tops.npy file and saved as tops.index)
    """

    os.makedirs(base_faiss_index_path, exist_ok=True)

    for category in all_categories:
        embedding_file = os.path.join(embeddings_path, f"{category}.npy")
        if not os.path.exists(embedding_file):
            print(f"Embedding file for category '{category}' not found at {embedding_file}. Skipping.")
            continue

        embeddings = np.load(embedding_file).astype('float32')
        dimension = embeddings.shape[1]
        faiss_index = faiss.IndexFlatIP(dimension) # Telling FAISS the size of each vector...used for cosine similarity search.

        faiss_index.add(embeddings)
        faiss_index_path = os.path.join(base_faiss_index_path, f"{category}.index")
        faiss.write_index(faiss_index, faiss_index_path)

        print(f"FAISS index built and saved successfully to {faiss_index_path}.")

if __name__ == "__main__":
    build_faiss_index()
