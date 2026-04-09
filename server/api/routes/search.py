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
                        WITH ranked_products AS (
                            SELECT
                                ri.product_id,
                                MIN(distance) AS distance
                            FROM related_images AS ri
                            JOIN products AS p 
                                ON p.product_id = ri.product_id
                            {where_clause}
                            GROUP BY ri.product_id
                            ORDER BY MIN(distance)
                            LIMIT 200
                        ),
                        """
    related_images_table = """
                        related_images AS (
                            SELECT
                                p_img.product_id,
                                (p_img.embedding <=> :query_embedding) AS distance
                            FROM product_images AS p_img
                            WHERE (p_img.embedding <=> :query_embedding) < :max_distance
                        ),
                        """
    product_variant_mapping = """
                            product_variant_mapping AS (
                                SELECT
                                    pc.product_id,
                                    JSON_AGG(
                                        JSON_BUILD_OBJECT(
                                            'color', pc.color,
                                            'image', pi.s3_url
                                        )
                                        ORDER BY pc.color
                                    ) AS variants
                                FROM product_colors pc
                                JOIN product_images pi
                                    ON pc.product_id = pi.product_id
                                    AND pc.color_id = pi.color_id
                                GROUP BY pc.product_id
                            )
                            """
    product_sizes_agg = """
                        product_sizes_agg AS (
                            SELECT
                                ps.product_id,
                                array_agg(ps.size) AS sizes
                            FROM product_sizes ps
                            GROUP BY ps.product_id
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
                                        pvm.variants,
                                        psa.sizes,
                                        rp.distance
                                    FROM ranked_products AS rp
                                        JOIN products AS p
                                            ON p.product_id = rp.product_id
                                        LEFT JOIN product_variant_mapping AS pvm
                                            ON p.product_id = pvm.product_id
                                        LEFT JOIN product_sizes_agg AS psa
                                            ON p.product_id = psa.product_id
                                    ORDER BY rp.distance ASC;
                                    LIMIT :page_limit OFFSET :page_offset;
                                    """
    
    search_query = (
        related_images_table + 
        ranked_products_table + 
        product_variant_mapping + 
        product_sizes_agg + 
        unique_products_from_tables
    )
    
    search_sql = text(search_query)

    try:
        results = db.execute(search_sql, params).mappings().all()
        
        return {"products": results,
                "page": curr_page,
                "page_limit": request.page_limit,
                "has_next": len(results) == request.page_limit
               }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/new", response_model=BaseProductSearchResponseModel)
async def search_newest_k_products(db: Session = Depends(get_db), limit: int = 20):
    get_newest_k_products_query = """
                                WITH newest_products AS (
                                    SELECT *
                                    FROM products
                                    ORDER BY created_at DESC
                                    LIMIT :limit
                                ),
                                product_variant_mapping AS (
                                    SELECT
                                        pc.product_id,
                                        JSON_AGG(
                                            JSON_BUILD_OBJECT(
                                                'color', pc.color,
                                                'image', pi.s3_url
                                            )
                                            ORDER BY pc.color
                                        ) AS variants
                                    FROM product_colors AS pc
                                    JOIN product_images AS pi
                                        ON pc.product_id = pi.product_id
                                        AND pc.color_id = pi.color_id
                                    GROUP BY pc.product_id
                                ),
                                product_sizes_agg AS (
                                    SELECT
                                        ps.product_id,
                                        array_agg(ps.size) AS sizes
                                    FROM product_sizes ps
                                    WHERE ps.product_id IN (SELECT product_id FROM newest_products)
                                    GROUP BY ps.product_id
                                )
                                SELECT
                                    np.product_id,
                                    np.name,
                                    np.brand,
                                    np.gender,
                                    np.category,
                                    np.product_url,
                                    np.rating,
                                    np.rating_count,
                                    np.price,
                                    np.currency,
                                    pvm.variants,
                                    psa.sizes
                                FROM newest_products AS np
                                    LEFT JOIN product_variant_mapping AS pvm
                                        ON np.product_id = pvm.product_id
                                    LEFT JOIN product_sizes_agg AS psa
                                        ON np.product_id = psa.product_id
                                ORDER BY np.created_at DESC;
                            """
    get_newest_k_products_sql = text(get_newest_k_products_query)

    try:
      result = db.execute(get_newest_k_products_sql, {"limit": limit})
      
      return {
              "products": result.mappings().all(),
              "total": len(result.all()),
              "page": 1,
              "page_limit": limit,
              "has_next": False
             }
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))


@router.post("/brands/{brand}", response_model=BaseProductSearchResponseModel)
async def search_products_by_brand(request: ProductSearchByFilterRequestModel, db: Session = Depends(get_db)):
    search_by_brand_query = """
                            WITH filtered_products AS (
                                SELECT *
                                FROM products
                                WHERE brand = :brand
                                ORDER BY created_at DESC, rating_count DESC
                                LIMIT :page_limit OFFSET :page_offset
                            ),
                            product_variant_mapping AS (
                                SELECT
                                    pc.product_id,
                                    JSON_AGG(
                                        JSON_BUILD_OBJECT(
                                            'color', pc.color,
                                            'image', pi.s3_url
                                        )
                                        ORDER BY pc.color
                                    ) AS variants
                                FROM product_colors AS pc
                                JOIN product_images AS pi
                                    ON pc.product_id = pi.product_id
                                    AND pc.color_id = pi.color_id
                                WHERE pc.product_id IN (SELECT product_id FROM filtered_products)
                                GROUP BY pc.product_id
                            ),
                            product_sizes_agg AS (
                                    SELECT
                                        ps.product_id,
                                        array_agg(ps.size) AS sizes
                                    FROM product_sizes ps
                                    WHERE ps.product_id IN (SELECT product_id FROM filtered_products)
                                    GROUP BY ps.product_id
                            )
                            SELECT
                                fp.product_id,
                                fp.name,
                                fp.brand,
                                fp.gender,
                                fp.category,
                                fp.product_url,
                                fp.rating,
                                fp.rating_count,
                                fp.price,
                                fp.currency,
                                pvm.variants,
                                psa.sizes
                            FROM filtered_products AS fp
                            LEFT JOIN product_variant_mapping AS pvm
                                ON fp.product_id = pvm.product_id
                            LEFT JOIN product_sizes_agg AS psa
                                ON fp.product_id = psa.product_id
                            LIMIT :page_limit OFFSET :page_offset;
                          """
    total_brand_products_query = "SELECT COUNT(*) FROM products WHERE brand = :brand"
    
    search_by_brand_sql = text(search_by_brand_query)
    total_brand_products_sql = text(total_brand_products_query)
    curr_page = max(request.page, 1)
    offset = (curr_page - 1) * request.page_limit
    
    params = {"brand": request.filter_name, "page_limit": request.page_limit, "page_offset": (curr_page - 1) * request.page_limit}
    
    try:
        result = db.execute(search_by_brand_sql, params)
        total_brand_products_result = db.execute(total_brand_products_sql, {"brand": request.filter_name})
        
        return {
                "products": result.mappings().all(),
                "total": total_brand_products_result.scalar(),
                "page": curr_page,
                "page_limit": request.page_limit,
                "has_next": offset + request.page_limit < total_brand_products_result.scalar()
               }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

 
@router.post("/categories/{category}", response_model=BaseProductSearchResponseModel)
async def search_products_by_category(request: ProductSearchByFilterRequestModel, db: Session = Depends(get_db)):
    search_by_category_query = """
                            WITH filtered_products AS (
                                SELECT *
                                FROM products
                                WHERE category = :category
                                ORDER BY created_at DESC, rating_count DESC
                                LIMIT :page_limit OFFSET :page_offset
                            ),
                            product_variant_mapping AS (
                                SELECT
                                    pc.product_id,
                                    JSON_AGG(
                                        JSON_BUILD_OBJECT(
                                            'color', pc.color,
                                            'image', pi.s3_url
                                        )
                                        ORDER BY pc.color
                                    ) AS variants
                                FROM product_colors AS pc
                                JOIN product_images AS pi
                                    ON pc.product_id = pi.product_id
                                    AND pc.color_id = pi.color_id
                                WHERE pc.product_id IN (SELECT product_id FROM filtered_products)
                                GROUP BY pc.product_id
                            ),
                            product_sizes_agg AS (
                                SELECT
                                    ps.product_id,
                                    array_agg(ps.size) AS sizes
                                FROM product_sizes ps
                                WHERE ps.product_id IN (SELECT product_id FROM filtered_products)
                                GROUP BY ps.product_id
                            )
                            SELECT
                                fp.product_id,
                                fp.name,
                                fp.brand,
                                fp.gender,
                                fp.category,
                                fp.product_url,
                                fp.rating,
                                fp.rating_count,
                                fp.price,
                                fp.currency,
                                pvm.variants
                            FROM filtered_products AS fp
                            LEFT JOIN product_variant_mapping AS pvm
                                ON fp.product_id = pvm.product_id
                            LIMIT :page_limit OFFSET :page_offset;
                          """
    total_category_products_query = "SELECT COUNT(*) FROM products WHERE category = :category"

    search_by_category_sql = text(search_by_category_query)
    total_category_products_sql = text(total_category_products_query)
    curr_page = max(request.page, 1)
    offset = (curr_page - 1) * request.page_limit

    params = {"category": request.filter_name, "page_limit": request.page_limit, "page_offset": (curr_page - 1) * request.page_limit}
    
    try:
        result = db.execute(search_by_category_sql, params)
        total_category_products_result = db.execute(total_category_products_sql, {"category": request.filter_name})

        return {
                "products": result.mappings().all(),
                "total": total_category_products_result.scalar(),
                "page": curr_page,
                "page_limit": request.page_limit,
                "has_next": offset + request.page_limit < total_category_products_result.scalar()
               }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

