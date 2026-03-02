import boto3
from botocore.exceptions import ClientError
from backend.config import settings

import os
import logging
from pathlib import Path
import glob


def _upload_file(file_name: str, bucket: str, object_path: str) -> bool:
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_path)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_images(all_images: str) -> None:
    image_paths = glob.glob(all_images, recursive=True)
    print("Found images:", len(image_paths))

    for image_path in image_paths:
        image_name = Path(image_path).stem
        product_info = image_name.split('_')
        
        if len(product_info) != 4:
            print(f"Image {image_name} does not follow 4 part standard")
            continue

        _, product_brand, product_id, product_color_id = product_info
        object_key = f"products/{product_brand}/{product_id}/{product_color_id}.jpg"

        uploaded = _upload_file(image_path, settings.S3_BUCKET, object_key)
        if uploaded:
            print("==" * 25)
            print(f"Successfully uploaded {image_path}.")
            print(f"Uploaded to: https://{settings.S3_BUCKET}.s3.amazonaws.com/{object_key}")
            print("==" * 25, "\n")



if __name__ == '__main__':
    all_images_path = 'data/images/**/*.jpg'
    upload_images(all_images=all_images_path)