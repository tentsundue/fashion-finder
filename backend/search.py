import pandas as pd
from clip_model import embed_image
from build_faiss_index import categories
from global_vars import categories
import faiss


# Load FAISS index and metadata
metadata = pd.read_csv("data/metadata.csv")

def search(query_image_path, category, k=5):
    assert category in categories, f"Category '{category}' not found. Available categories: {categories}"

    faiss_index = faiss.read_index(f"data/faiss/{category}.index")
    
    query_embedding = (
                        embed_image(query_image_path)
                        .flatten()
                        .astype('float32')
                        .reshape(1, -1)
                       )
    
    distances, indices = faiss_index.search(query_embedding, k)
    results = metadata.iloc[indices[0]]

    return results

if __name__ == "__main__":
    query_image_path = "data/images/test_queries/work_pants.jpg"
    search_results = search(query_image_path, category="bottoms", k=5)
    print(search_results)
    