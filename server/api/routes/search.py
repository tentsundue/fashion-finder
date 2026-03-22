from fastapi import APIRouter, HTTPException, Depends

from server.schemas.search import BaseProductSearchResponseModel, ProductSearchByFilterRequestModel, SimilarProductsSearchRequestModel, SimilarProductsSearchResponseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from server.db.session import get_db

from server.services.clip_model import embed_image

router = APIRouter()


@router.post("/products", response_model=SimilarProductsSearchResponseModel)
async def search_products(
                            request: SimilarProductsSearchRequestModel,
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
    curr_page = max(request.page, 1)
    params = {"query_embedding": query_embedding, "page_limit": request.page_limit, "page_offset": (curr_page - 1) * request.page_limit}

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
                            LIMIT 200;
                        ),
                        """
    related_images_table = """
                        WITH related_images AS (
                            SELECT
                                p_img.product_id,
                                (p_img.embedding <=> :query_embedding) AS distance
                            FROM product_images AS p_img
                            WHERE distance < :max_distance
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
                                    LIMIT :page_limit OFFSET :page_offset;
                                    """
    
    search_query = related_images_table + ranked_products_table + product_color_agg_table + product_image_agg_table + unique_products_from_tables
    
    search_sql = text(search_query)

    try:
        top_k_results = db.execute(search_sql, params).mappings().all()
        
        return {"products": top_k_results,
                "page": curr_page,
                "page_limit": request.page_limit,
                "has_next": len(top_k_results) == request.page_limit
               }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/new", response_model=BaseProductSearchResponseModel)
async def search_newest_k_products(db: Session = Depends(get_db), k=20):
    get_newest_k_products_query = """
                              WITH newest_products AS (
                                SELECT product_id
                                FROM products
                                ORDER BY created_at DESC
                                LIMIT :k
                              ),
                              product_color_images AS (
                                SELECT
                                  p_col.product_id,
                                  p_col.color,
                                  p_img.s3_url
                                FROM product_colors p_col
                                JOIN product_images p_img
                                  ON p_col.product_id = p_img.product_id
                                  AND p_col.color_id = p_img.color_id
                                WHERE p_col.product_id IN (SELECT product_id FROM newest_products)
                              )

                              SELECT
                                p.product_id,
                                p.name,
                                p.brand,
                                p.gender,
                                p.category,
                                p.product_url,
                                p.rating,
                                p.rating_count,

                                ARRAY_AGG(DISTINCT pci.color) AS colors,
                                ARRAY_AGG(DISTINCT pci.s3_url) AS s3_urls

                              FROM products p
                              JOIN product_color_images pci
                                ON p.product_id = pci.product_id

                              GROUP BY
                                p.product_id,
                                p.name,
                                p.brand,
                                p.gender,
                                p.category,
                                p.product_url,
                                p.rating,
                                p.rating_count

                              ORDER BY p.created_at DESC;
                              """
    get_newest_k_products_sql = text(get_newest_k_products_query)

    try:
      newest_products_result = db.execute(get_newest_k_products_sql, {"k": k})
      
      return {
              "products": newest_products_result.mappings().all(),
              "total": len(newest_products_result.all()),
              "page": 1,
              "page_limit": k,
              "has_next": False
             }
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))


@router.post("/brand/{brand}", response_model=BaseProductSearchResponseModel)
async def search_products_by_brand(request: ProductSearchByFilterRequestModel, db: Session = Depends(get_db)):
    search_by_brand_query = """
                            WITH product_color_images AS (
                                SELECT
                                    p_col.product_id,
                                    p_col.color,
                                    p_img.s3_url
                                FROM product_colors AS p_col
                                JOIN product_images AS p_img
                                    ON p_col.color_id = p_img.color_id
                                    AND p_col.product_id = p_img.product_id
                                WHERE p_col.product_id IN (SELECT product_id FROM products WHERE brand = :brand)
                            )
                            SELECT
                                p.product_id,
                                p.name,
                                p.brand,
                                p.gender,
                                p.category,
                                p.product_url,
                                p.rating,
                                p.rating_count,

                                ARRAY_AGG(DISTINCT pci.color) AS colors,
                                ARRAY_AGG(DISTINCT pci.s3_url) AS s3_urls
                            FROM products AS p
                            JOIN product_color_images AS pci
                                ON p.product_id = pci.product_id
                            GROUP BY
                                p.product_id,
                                p.name,
                                p.brand,
                                p.gender,
                                p.category,
                                p.product_url,
                                p.rating,
                                p.rating_count
                            ORDER BY p.created_at DESC, p.rating_count DESC
                            LIMIT :page_limit OFFSET :page_offset;
                          """
    total_brand_products_query = "SELECT COUNT(*) FROM products WHERE brand = :brand"
    
    search_by_brand_sql = text(search_by_brand_query)
    total_brand_products_sql = text(total_brand_products_query)
    curr_page = max(request.page, 1)
    offset = (curr_page - 1) * request.page_limit
    
    params = {"brand": request.filter_name, "page_limit": request.page_limit, "page_offset": (curr_page - 1) * request.page_limit}
    try:
        brand_products_result = db.execute(search_by_brand_sql, params)
        total_brand_products_result = db.execute(total_brand_products_sql, {"brand": request.filter_name})
        
        return {
                "products": brand_products_result.mappings().all(),
                "total": total_brand_products_result.scalar(),
                "page": curr_page,
                "page_limit": request.page_limit,
                "has_next": offset + request.page_limit < total_brand_products_result.scalar()
               }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
