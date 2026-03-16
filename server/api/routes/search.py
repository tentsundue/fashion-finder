from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from sqlalchemy import text

from server.schemas.search import SearchRequestModel, SearchResponseModel
from server.db.session import get_db

from server.services.clip_model import embed_image

router = APIRouter()


@router.post("/products", response_model=list[SearchResponseModel])
async def search_products(
                            request: SearchRequestModel,
                            db: Session = Depends(get_db)
):
    """
    Recieve image, compute embedding, and return top k most similar products 
    based on cosine similarity of the embeddings. 
    Optional filters for brands and categories can be applied.
    """
    query_embedding = (
                    embed_image(request.image_path)
                    .flatten()
                    .astype('float32')
                    .reshape(1, -1)
                    )
    params = {"query_embedding": query_embedding, "k": request.k}

    brand_filters = []
    category_filters = []
    clauses = []
    where_clause = ""

    if request.brands:
        brand_filters = [f"p.brand = :brand_{i}" for i in range(len(request.brands))]
        for i, brand in enumerate(request.brands):
            params[f"brand_{i}"] = brand
        clauses.append("(" + " OR ".join(brand_filters) + ")")

    if request.categories:
        category_filters = [f"p.category = :category_{i}" for i in range(len(request.categories))]
        for i, category in enumerate(request.categories):
            params[f"category_{i}"] = category
        clauses.append("(" + " OR ".join(category_filters) + ")")

    where_clause = ""
    if clauses:
        where_clause = "WHERE " + " AND ".join(clauses)
    
    ranked_products_table = f"""
                        ranked_products AS (
                            SELECT
                                ri.product_id,
                                MIN(distance) AS distance
                            FROM related_images AS ri
                            JOIN products AS p 
                                ON p.product_id = ri.product_id
                            {where_clause}
                            GROUP BY ri.product_id
                            ORDER BY MIN(distance)
                            LIMIT :k
                        ),
                        """
    related_images_table = """
                        WITH related_images AS (
                            SELECT
                                p_img.product_id,
                                (p_img.embedding <=> :query_embedding) AS distance
                            FROM product_images AS p_img
                        ),
                        """
    product_color_agg_table = """
                            product_color_agg AS (
                                SELECT
                                    pc.product_id,
                                    ARRAY_AGG(DISTINCT pc.color ORDER BY pc.color) AS colors
                                FROM product_colors AS pc
                                GROUP BY pc.product_id
                            ),
                            """
    product_image_agg_table = """
                            product_image_agg AS (
                                SELECT
                                    pi.product_id,
                                    ARRAY_AGG(DISTINCT pi.s3_url ORDER BY pi.s3_url) AS s3_urls
                                FROM product_images AS pi
                                GROUP BY pi.product_id  
                            )
                            """
    
    unique_products_from_tables = """
                                    SELECT
                                        p.product_id,
                                        p.name,
                                        p.brand,
                                        p.gender,
                                        p.category,
                                        p.product_url,
                                        p.rating,
                                        p.rating_count,
                                        p.price,
                                        p.currency,
                                        pca.colors,
                                        pia.s3_urls,
                                        rp.distance
                                    FROM ranked_products AS rp
                                            JOIN products AS p
                                                ON p.product_id = rp.product_id
                                            LEFT JOIN product_color_agg AS pca
                                                    ON p.product_id = pca.product_id
                                            LEFT JOIN product_image_agg AS pia
                                                    ON p.product_id = pia.product_id
                                    ORDER BY rp.distance ASC;
                                    """
    
    search_query = related_images_table + ranked_products_table + product_color_agg_table + product_image_agg_table + unique_products_from_tables

    search_sql = text(search_query)

    try:
        top_k_results = db.execute(search_sql, params).mappings().all()
        return top_k_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
