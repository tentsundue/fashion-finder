from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class Product(BaseModel):
    product_id: str
    product_url: str

    name: str
    brand: str
    gender: str
    
    price: float
    currency: str
    
    category: str

    rating: Optional[float] = None
    rating_count: Optional[int] = None
    

    model_config = ConfigDict(
        from_attributes=True, 
        json_schema_extra={
            "product_id": "12345",
            "product_url": "https://www.example.com/product/12345",
            "name": "Example Product",
            "brand": "Example Brand",
            "gender": "Unisex",
            "price": 99.99,
            "currency": "USD",
            "category": "Shoes",
            "rating": 4.5,
            "rating_count": 100
        }
    )

class ProductColor(BaseModel):
    color: str
    s3_url: str


class ProductSize(BaseModel):
    size: str


class GetProductResponseModel(BaseModel):
    product: Product
    colors: List[ProductColor]
    sizes: List[ProductSize]