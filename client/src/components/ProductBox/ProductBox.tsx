import {
  Flex,
  Image,
  Box,
  Separator,
  Text,
  Dialog,
  HStack,
} from "@chakra-ui/react";

import { type JSX } from "react";

import { StarFilled } from "@ant-design/icons";
import uniqloLogo from "@/assets/uniqlo_logo.png";

import type { ProductInfo } from "@/types/product";
import ProductInfoModal from "@/components/ProductInfoModal/ProductInfoModal";
import ImageCarousel from "../ImageCarousel/ImageCarousel";

interface ProductBoxProps {
  productInfo: ProductInfo;
}

export default function ProductBox({ productInfo }: ProductBoxProps) {
  const UniqloCard = (
    <Image
      w="15%"
      h="15%"
      position="absolute"
      bottom={0}
      right={0}
      src={uniqloLogo}
    />
  );

  const brand_to_card: Record<string, JSX.Element> = {
    uniqlo: UniqloCard,
  };

  return (
    <HStack wrap="wrap" gap="2">
      <Dialog.Root
        key="center"
        placement="center"
        motionPreset="slide-in-bottom">
        <Dialog.Trigger asChild>
          <Flex
            data-state="open"
            _open={{
              animation: "fade-in 800ms, scale-in 1000ms",
            }}
            direction="column"
            cursor="pointer"
            alignItems="left"
            justifyContent="left"
            p={3}
            position="relative"
            _hover={{
              boxShadow: "md",
              filter: "brightness(0.95)",
              transform: "translateY(-1px)",
              transition: "0.3s ease",
            }}
            border="1px solid gray.300"
            borderWidth={1}
            borderRadius="md"
            boxShadow="sm"
            maxW="xl"
            mx="auto">
            {/* Image Carousel */}
            <ImageCarousel
              color_to_s3_url={productInfo.color_to_s3_url}
              productName={productInfo.name}
            />

            <Separator variant="solid" mt={7} size="sm" />

            {/* Product Info */}
            <Flex
              direction="column"
              mt={5}
              textAlign="left"
              justifyContent="left"
              gap={2}
              alignItems="left">
              <Text
                fontWeight="bold"
                fontSize="2xl"
                fontFamily="Georgia, sans-serif"
                letterSpacing={1}>
                {productInfo.name}
              </Text>

              <Text
                fontSize="md"
                color="gray.500"
                fontFamily="Georgia, sans-serif">
                {productInfo.category.toUpperCase()} |{" "}
                {productInfo.gender.toUpperCase()}
              </Text>
              {brand_to_card[productInfo.brand.toLowerCase()]}
              <Text
                color="black.500"
                fontSize="4xl"
                fontFamily="Roboto, sans-serif"
                fontWeight="semibold"
                mt={2}
                p={1}>
                {productInfo.price.toLocaleString("en-US", {
                  style: "currency",
                  currency: productInfo.currency,
                })}
              </Text>

              <Box
                color="gray.500"
                fontFamily="Roboto, sans-serif"
                letterSpacing={1}
                mt={2}>
                <StarFilled />{" "}
                <Text as="span" fontWeight="bold">
                  {productInfo.rating}
                </Text>{" "}
                ({productInfo.rating_count})
              </Box>
            </Flex>
          </Flex>
        </Dialog.Trigger>
        <ProductInfoModal productInfo={productInfo} />
      </Dialog.Root>
    </HStack>
  );
}
