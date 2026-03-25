export interface ProductInfo {
  product_id: string;
  product_url: string;

  name: string;
  brand: string;
  gender: string;

  price: number;
  currency: string;

  category: string;

  rating: number;
  rating_count: number;

  color_to_s3_url: Record<string, string>; // {color name: s3 url, ...}
}