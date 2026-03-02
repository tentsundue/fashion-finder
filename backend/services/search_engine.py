import pandas as pd
from clip_model import embed_image, predict_category
from config import all_categories
import faiss


# Load FAISS index and metadata
metadata = pd.read_csv("data/metadata.csv")

def search(query_image_path: str, categories: list[str] = [], k: int = 5) -> list[pd.DataFrame]:
    category_faiss_mappings = {}
    all_results = []

    if not categories:
        likely_category, score = predict_category(query_image_path, all_categories)
        print(f"Predicted category: {likely_category} with confidence score: {score[likely_category]:.4f}")
        categories = [likely_category]

    for category in categories:
        assert category in all_categories, f"Category '{category}' not found. Available categories: {all_categories}"
        faiss_index = faiss.read_index(f"data/faiss/{category}.index")
        category_faiss_mappings[category] = faiss_index

    query_embedding = (
                        embed_image(query_image_path)
                        .flatten()
                        .astype('float32')
                        .reshape(1, -1)
                       )
    
    
    for category, faiss_index in category_faiss_mappings.items():
        distances, indices = faiss_index.search(query_embedding, k)
        category_results = metadata.iloc[indices[0]]
        all_results.append(category_results)

    return all_results

if __name__ == "__main__":
    query_image_path = "data/images/test_queries/work_pants.jpg"
    search_results = search(query_image_path, categories=[], k=5)
    print(search_results)
    