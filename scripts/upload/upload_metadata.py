import os

from sqlalchemy import text
from sqlalchemy.orm import Session

import pandas as pd
from tqdm import tqdm

import json

from backend.db.session import get_db
from backend.config import settings
from backend.services.clip_model import embed_image



metadata = metadata = pd.read_csv("data/metadata.csv")
base_image_path = "data\\images\\"

product_insert_query = """
                        INSERT INTO products (product_id, name, brand, gender, category, price, currency, rating, rating_count, product_url)
                        VALUES ((:product_id), (:name), (:brand), (:gender), (:category), (:price), (:currency), (:rating), (:rating_count), (:product_url))
                        ON CONFLICT (product_id) DO UPDATE SET
                            name = EXCLUDED.name,
                            brand = EXCLUDED.brand,
                            gender = EXCLUDED.gender,
                            category = EXCLUDED.category,
                            price = EXCLUDED.price,
                            currency = EXCLUDED.currency,
                            rating = EXCLUDED.rating,
                            rating_count = EXCLUDED.rating_count,
                            product_url = EXCLUDED.product_url
                        """
product_colors_insert_query = """
                                INSERT INTO product_colors (product_id, color_id, color)
                                VALUES ((:product_id), (:color_id), (:color))
                                ON CONFLICT (product_id, color_id) DO UPDATE SET
                                color = EXCLUDED.color
                              """
product_images_insert_query = """
                                INSERT INTO product_images (product_id, color_id, embedding, s3_url)
                                VALUES ((:product_id), (:color_id), (:embedding), (:s3_url))
                                ON CONFLICT (product_id, color_id, s3_url) DO UPDATE SET
                                    product_id = EXCLUDED.product_id,
                                    color_id = EXCLUDED.color_id,
                                    embedding = EXCLUDED.embedding,
                                    s3_url = EXCLUDED.s3_url
                              """
product_sizes_insert_query = """
                                INSERT INTO product_sizes (product_id, size)
                                VALUES ((:product_id), (:size))
                                ON CONFLICT (product_id, size) DO NOTHING
                             """


def upload_metadata(db: Session) -> dict:
    rows_updated = {"products": 0, "product_colors": 0, "product_images": 0, "product_sizes": 0}

    products_sql = text(product_insert_query)
    product_colors_sql = text(product_colors_insert_query)
    product_sizes_sql = text(product_sizes_insert_query)
    product_images_sql = text(product_images_insert_query)

    products_added = set()
    
    products_batch = []
    colors_batch = []
    images_batch = []
    sizes_batch = []

    # NOTE: metadata has dupes. E.g. same p_id, c_id, image_url, etc. but diff category.
    for _, row in tqdm(metadata.iterrows(), total=len(metadata)):
        sizes = json.loads(row["sizes"])

        product_id = row['product_id']
        image_id = row['image_id']
        color_id = row['variant_id']
        brand = row['brand']

        filename = f"{image_id}_{product_id}_{color_id}.jpg"
      
        if filename not in os.listdir(os.path.join(base_image_path, brand)):
            print(f"Image file {filename} not found in {os.path.join(base_image_path, brand)}. Skipping.")
            continue
        
        image_path = os.path.join(base_image_path, brand, filename)
        image_embedding = embed_image(image_path)

        if product_id not in products_added:
            products_batch.append({
                                "product_id": product_id, 
                                "name": row['name'],
                                "brand": brand,
                                "gender": row['gender'],
                                "category": row['category'],
                                "price": row['price'],
                                "currency": row['currency'],
                                "rating": row['rating'],
                                "rating_count": row['rating_count'],
                                "product_url": row['product_url']
                            })

            for size in sizes:
                sizes_batch.append({
                                    "product_id": product_id,
                                    "size": size
                                })

            products_added.add(row['product_id'])

        colors_batch.append({
                            "product_id": product_id,
                            "color_id": color_id,
                            "color": row["color"]
                        })
        
        images_batch.append({
                            "product_id": product_id,
                            "color_id": color_id,
                            "embedding": image_embedding.flatten().tolist(), # Convert numpy array to list for JSON serialization
                            "s3_url": f"https://{settings.S3_BUCKET}.s3.amazonaws.com/products/{brand}/{product_id}/{color_id}.jpg"
                        })


    try:
        products_res = db.execute(products_sql, products_batch)
        colors_res = db.execute(product_colors_sql, colors_batch)
        sizes_res = db.execute(product_sizes_sql, sizes_batch)
        images_res = db.execute(product_images_sql, images_batch)
        db.commit()
    except Exception:
        db.rollback()
        raise

    rows_updated["products"] = products_res.rowcount
    rows_updated["product_colors"] = colors_res.rowcount
    rows_updated["product_images"] = images_res.rowcount
    rows_updated["product_sizes"] = sizes_res.rowcount

    return rows_updated


if __name__ == '__main__':
    session = db = next(get_db())
    print("Connected to session successfully.")
    res = upload_metadata(session)
    print(res) # can verify the counts in sanity_check.txt (Just make sure that it is updated with the most recent metadata.csv)
    