import open_clip
import torch
from PIL import Image

# Use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model & preprocess
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",  # Model size (good balance)
    pretrained="laion2b_s34b_b79k"
)
model = model.to(device)

def encode_image(image_path):
    """
    Loads an image, preprocesses it, generates a normalized CLIP embedding
    """
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)  # normalize for cosine similarity

    return embedding.cpu().numpy()
