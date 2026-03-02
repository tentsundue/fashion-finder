from clip_model import encode_image

image_path = "data/images/UNIQLO/1_uniqlo_E484812-000_COL62.jpg"
embedding = encode_image(image_path)
print("Embedding shape:", embedding.shape)
