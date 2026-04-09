import ProductBox from "@/components/ProductBox/ProductBox";
import Dropzone from "@/components/Dropzone/Dropzone";
import uniqlo1 from "@/assets/uniqlo1.jpg";
import uniqlo2 from "@/assets/uniqlo2.jpg";
import uniqlo3 from "@/assets/uniqlo3.jpg";
import { Box } from "@chakra-ui/react";

export default function Home() {
  const sampleProductInfo = {
    product_id: "1",
    product_url: "https://www.youtube.com",
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
    sizes: ["S", "M", "L", "XL"],
  };

  const products = Array(6).fill(sampleProductInfo);
  return (
    <>
      <Dropzone
        onFilesUploaded={(files) => {
          console.log("Files uploaded:", files);
        }}
      />
      <Box
        display="grid"
        gridTemplateColumns="repeat(auto-fill, minmax(350px, 1fr))"
        p={5}
        gap={5}>
        {products.map((product, index) => (
          <ProductBox key={index} productInfo={product} />
        ))}
      </Box>
    </>
  );
}
