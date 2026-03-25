from typing import Optional

from pydantic import BaseModel

class ProductSearchItem(BaseModel):
    product_id: str
    product_url: str

    name: str
    brand: str
    gender: str
    
    price: float
    currency: str
    
    category: str

    rating: float
    rating_count: int

    color_to_s3_url: dict[str, str] # Color name -> s3_url

class BaseProductSearchResponseModel(BaseModel):
    products: list[ProductSearchItem]
    total: Optional[int]
    page: int
    page_limit: int
    has_next: bool


class BaseProductSearchRequestModel(BaseModel):
    page_limit: int = 15
    page: int = 1


class ProductSearchByFilterRequestModel(BaseProductSearchRequestModel):
    filter_name: str
    

class SimilarProductSearchItem(ProductSearchItem):
    distance: float

class SimilarProductsSearchResponseModel(BaseModel):
    products: list[SimilarProductSearchItem]


class SimilarProductsSearchRequestModel(BaseProductSearchRequestModel):
    image_path: str
    max_distance: float = 0.4
    brands: list[str] | None = None
    categories: list[str] | None = None
