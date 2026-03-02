import open_clip
import torch
from PIL import Image

# Use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model, preprocess, and tokenizer
model, _, preprocess = open_clip.create_model_and_transforms(
                            "ViT-B-32",
                            pretrained="laion2b_s34b_b79k"
                        )

model = model.to(device)
tokenizer = open_clip.get_tokenizer("ViT-B-32")


def embed_image(image_path: str) -> torch.Tensor:
    """
    Loads an image, preprocesses it, generates a normalized CLIP embedding
    """
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)  # normalize for cosine similarity

    return embedding.cpu().numpy()


def embed_text(text: str) -> torch.Tensor:
    """
    Generates a normalized CLIP embedding for the input text
    """
    templates = [
        "a photo of {}",
        "a photo of a person wearing {}",
        "a photo of a piece of clothing: {}",
        "a product photo of {}",
        "a stock photo of {}",
        "a studio photo of {}",
    ]
    texts = [template.format(text) for template in templates]
    tokens = tokenizer(texts).to(device)

    with torch.no_grad():
        text_embedding = model.encode_text(tokens)
        text_embedding /= text_embedding.norm(dim=-1, keepdim=True)  # normalize for cosine similarity

    text_embedding = text_embedding.mean(dim=0, keepdim=True)  # average over templates
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)  # re-normalize after averaging
    
    return text_embedding.cpu().numpy()


def predict_category(image_path: str, categories: list[str]) -> tuple[str, dict]:
    """
    Predicts the category of an image based on its CLIP embedding and 
    a list of candidate categories.
    """

    image_embedding = embed_image(image_path)

    scores = {}
    for cat in categories:
        text_embedding = embed_text(cat)
        score = float((image_embedding @ text_embedding.T).item())
        scores[cat] = score

    best = max(scores, key=scores.get)
    return best, scores