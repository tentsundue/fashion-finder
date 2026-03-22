from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from sqlalchemy import text

from server.schemas.products import GetProductResponseModel, GetProductsResponseModel
from server.db.session import get_db

router = APIRouter()


@router.get("/{product_id}", response_model=GetProductResponseModel)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    get_product_query = """
                        SELECT
                          product_id,
                          name,
                          brand,
                          gender,
                          category,
                          product_url,
                          rating,
                          rating_count
                        FROM products AS p
                        WHERE p.product_id = :product_id;
                      """
    get_product_colors_query = """
                               SELECT
                                  p_col.product_id,
                                  p_col.color,
                                  p_img.s3_url
                               FROM product_colors as p_col
                               JOIN product_images as p_img
                                  ON p_col.product_id = :product_id
                                  AND p_img.product_id = :product_id
                                  AND p_col.color_id = p_img.color_id;
                              """

    get_product_sizes_query = """
                              SELECT
                                p_size.size
                              FROM product_sizes as p_size
                              WHERE p_size.product_id = :product_id;
                            """
    get_product_sql = text(get_product_query)
    get_product_colors_sql = text(get_product_colors_query)
    get_product_sizes_sql = text(get_product_sizes_query)

    try:
      product_res = db.execute(get_product_sql, {"product_id": product_id}).fetchone()
      product_color_res = db.execute(get_product_colors_sql, {"product_id": product_id}).mappings().all()
      product_size_res = db.execute(get_product_sizes_sql, {"product_id": product_id}).mappings().all()

      return {
              "product": product_res, 
              "colors": product_color_res,
              "sizes": product_size_res
             }
    
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
