from pydantic import BaseModel


class GetSearchProductsModel(BaseModel):
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

    colors: list[str]
    s3_urls: list[str]

    distance: float


class SearchRequestModel(BaseModel):
    image_path: str
    k: int = 30
    brands: list[str] | None = None
    categories: list[str] | None = None