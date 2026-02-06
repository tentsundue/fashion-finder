from clip_model import encode_image

image_path = "data/uniqlo/images/1_uniqlo_E479000-000_COL00.jpg"
embedding = encode_image(image_path)
print("Embedding shape:", embedding.shape)

