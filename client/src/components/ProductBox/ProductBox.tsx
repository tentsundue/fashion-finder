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
      src={uniqloLogo}
      position="absolute"
      bottom="8px"
      right="8px"
      boxSize="100px"
      objectFit="contain"
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
            backgroundColor="cardBg"
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
            borderRadius="md"
            boxShadow="sm"
            maxH="xxl"
            maxW="lg"
            mx="auto">
            {/* Image Carousel */}
            <Box w="100%" h="lg" overflow="hidden">
              <ImageCarousel
                color_to_s3_url={productInfo.color_to_s3_url}
                productName={productInfo.name}
              />
            </Box>

            <Separator variant="solid" mt={7} size="sm" />

            {/* Product Info */}
            <Flex
              direction="column"
              mt={5}
              textAlign="left"
              justifyContent="left"
              gap={2}
              alignItems="left">
              <Text fontWeight="bold" fontSize="2xl">
                {productInfo.name}
              </Text>

              <Text fontSize="md" color="secondaryTextColor">
                {productInfo.category.toUpperCase()} |{" "}
                {productInfo.gender.toUpperCase()}
              </Text>
              {brand_to_card[productInfo.brand.toLowerCase()]}
              <Text
                color="black.500"
                fontSize="4xl"
                fontWeight="semibold"
                mt={2}
                p={1}>
                {productInfo.price.toLocaleString("en-US", {
                  style: "currency",
                  currency: productInfo.currency,
                })}
              </Text>

              <Box color="secondaryTextColor" letterSpacing={1} mt={2}>
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
