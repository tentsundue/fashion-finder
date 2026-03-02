import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from backend.services.clip_model import embed_image
# from backend.config import all_categories # gonna need to change once db is up

"""
Purpose:
 - Load metadata CSV
    - For each image, generate CLIP embedding and store it in a list
 
 - Save the list of embeddings as a .npy file. 
   This will be used for fast retrieval during search.
 
 - Save the metadata (including image paths and product info) 
   in a new CSV for reference during search results display.

"""

# Load metadata CSV and define headers
metadata = pd.read_csv("data/metadata.csv")

# Image path setup --> Each path follows the same structure: data/images/{brand}/{image_id}_{brand}_{product_id}_{variant_id}.jpg
base_image_path = "data\\images\\"
base_embeddings_path = "data\\embeddings\\"

embedding_categories = {}
all_categories = ["tops", "bottoms", "innerwear", "outerwear"]

def build_embeddings_map() -> None:
    """
    Initialize an empty list for each category to store the corresponding image embeddings.
    This will allow us to group embeddings by category and save them separately.
    """
    for category in all_categories:
        embedding_categories[category] = []


def save_and_write_embeddings(embeddings: list[np.ndarray], category: str) -> None:
    """
    Saves the list of embeddings for a given category as a .npy file.
    All embeddings are saved under data/embeddings/...
    (i.e. embeddings for tops are saved in data/embeddings/tops.npy)
    """
    print(f"\nCategory: {category}, Number of embeddings: {len(embeddings)}")
      
    embeddings_array = np.array(embeddings).astype('float32')
    embedding_path = os.path.join(base_embeddings_path, f"{category}.npy")

    np.save(embedding_path, embeddings_array)

    print(f"Embeddings built and saved successfully to {embedding_path}.")


def build_embeddings() -> None:
  """
  Builds CLIP embeddings for each image in the metadata and saves them by category.
  """
  # Iterate through metadata and generate embeddings for each image
  for _, row in tqdm(metadata.iterrows(), total=len(metadata)):
      image_id, product_id, variant_id, brand, category = (
                                                            row['image_id'], 
                                                            row['product_id'], 
                                                            row['variant_id'], 
                                                            row['brand'], 
                                                            row['category']
                                                            )
          
      filename = f"{image_id}_{product_id}_{variant_id}.jpg"
      
      if filename not in os.listdir(os.path.join(base_image_path, brand)):
          print(f"Image file {filename} not found in {os.path.join(base_image_path, brand)}. Skipping.")
          continue
      
      image_path = os.path.join(base_image_path, brand, filename)
      
      image_embedding = embed_image(image_path)
      embedding_categories[category].append(image_embedding.flatten())

  # Save embeddings and metadata
  for category, embeddings in embedding_categories.items():
      save_and_write_embeddings(embeddings, category)
      

if __name__ == "__main__":
    os.makedirs(base_embeddings_path, exist_ok=True)
    build_embeddings_map()
    build_embeddings()