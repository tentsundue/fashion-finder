import numpy as np
import faiss
import pandas as pd


metadata = pd.read_csv("data/metadata.csv")
embeddings = np.load("data/embeddings.npy").astype('float32')
assert embeddings.shape[0] == len(metadata)

print("Embeddings shape:", embeddings.shape)

dimension = embeddings.shape[1]
faiss_index = faiss.IndexFlatIP(dimension)

faiss_index.add(embeddings)
faiss.write_index(faiss_index, "data/faiss.index")