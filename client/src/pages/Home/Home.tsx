import ProductBox from "@/components/ProductBox/ProductBox";
import uniqlo1 from "@/assets/uniqlo1.jpg";
import uniqlo2 from "@/assets/uniqlo2.jpg";
import uniqlo3 from "@/assets/uniqlo3.jpg";
import { Flex } from "@chakra-ui/react";

export default function Home() {
  return (
    <Flex
      direction="row"
      alignItems="left"
      justifyContent="left"
      p={5}
      gap={5}
      wrap="wrap">
      <ProductBox
        productInfo={{
          product_id: "1",
          product_url: "/product/1",
          name: "Sample Product With a Really Long Name to Test Text Wrapping",
          brand: "UNIQLO",
          gender: "Unisex",
          price: 19.99,
          currency: "USD",
          category: "bottoms",
          rating: 4.5,
          rating_count: 100,
          color_to_s3_url: {
            Red: uniqlo1,
            Blue: uniqlo2,
            Green: uniqlo3,
          },
        }}
      />
      <ProductBox
        productInfo={{
          product_id: "1",
          product_url: "/product/1",
          name: "Sample Product With a Really Long Name to Test Text Wrapping",
          brand: "UNIQLO",
          gender: "Unisex",
          price: 19.99,
          currency: "USD",
          category: "bottoms",
          rating: 4.5,
          rating_count: 100,
          color_to_s3_url: {
            Red: uniqlo1,
            Blue: uniqlo2,
            Green: uniqlo3,
          },
        }}
      />
    </Flex>
  );
}
