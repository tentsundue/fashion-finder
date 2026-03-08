from fastapi import FastAPI
from api.routes import products, search


# For openapi auto-generated documentation. Will I do it? Idk but this is pretty cool.
tags_metadata = [
    {
        "name": "products",
        "description": "Operations with products.",
    },
    {
        "name": "search",
        "description": "Operations for the search implementation",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(search.router, prefix="/search", tags=["search"])
