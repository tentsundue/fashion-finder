import type { ProductInfo } from "@/types/product";
import {
  Button,
  Image,
  CloseButton,
  Dialog,
  Flex,
  Portal,
  Separator,
  Box,
  Badge,
  Heading,
  Stack,
} from "@chakra-ui/react";
import ImageCarousel from "../ImageCarousel/ImageCarousel";
import uniqloLogo from "@/assets/uniqlo_logo.png";

interface InfoModalProps {
  productInfo: ProductInfo | null;
}

export default function ProductInfoModal({ productInfo }: InfoModalProps) {
  const UniqloCard = (
    <Image src={uniqloLogo} boxSize="100px" objectFit="contain" />
  );

  return (
    <Portal>
      <Dialog.Backdrop />
      <Dialog.Positioner>
        <Dialog.Content
          maxW="5xl"
          w="100%"
          maxH="75vh"
          overflow="hidden"
          borderRadius="md"
          p={5}
          bg="cardBg"
          mx="auto">
          <Dialog.Header>
            <Stack direction="column" gap={4}>
              <Stack direction="row" alignItems="center" gap={4}>
                <Dialog.Title fontSize="4xl" lineHeight={1}>
                  {productInfo?.name}
                </Dialog.Title>
                <Dialog.Description fontSize="md" color="secondaryTextColor">
                  {UniqloCard}
                </Dialog.Description>
              </Stack>

              <Stack direction="row">
                {productInfo?.sizes &&
                  productInfo.sizes.map((size) => (
                    <Badge key={size} variant="solid" size="lg">
                      {size}
                    </Badge>
                  ))}
              </Stack>
            </Stack>
          </Dialog.Header>
          <Separator my={4} />
          <Dialog.Body>
            <Flex direction="row" justifyContent="space-evenly" gap={20} mb={4}>
              {/* Vertical Image Carousel */}
              {productInfo && (
                <Box w="500px">
                  <ImageCarousel
                    color_to_s3_url={productInfo.color_to_s3_url}
                    productName={productInfo.name}
                    verticalView={true}
                  />
                </Box>
              )}
              {/* Product Info */}
              <Flex direction="column" alignItems="flex-end" gap={10}>
                <Heading fontSize="6xl" fontWeight="bold">
                  {productInfo?.price.toLocaleString("en-US", {
                    style: "currency",
                    currency: productInfo?.currency,
                  })}
                </Heading>
                <Flex
                  direction="column"
                  justifyContent="space-evenly"
                  h="100%"
                  alignItems="flex-end"
                  gap={4}>
                  <Heading fontSize="3xl" color="secondaryTextColor">
                    {productInfo?.category.toUpperCase()} |{" "}
                    {productInfo?.gender.toUpperCase()}
                  </Heading>
                  <Heading fontSize="3xl" color="secondaryTextColor">
                    ⭐{productInfo?.rating} ({productInfo?.rating_count}{" "}
                    reviews)
                  </Heading>
                </Flex>
              </Flex>
            </Flex>
          </Dialog.Body>
          <Dialog.Footer>
            <Dialog.ActionTrigger asChild>
              <Button colorPalette="red" variant="outline">
                Close
              </Button>
            </Dialog.ActionTrigger>
            <Button
              colorPalette="yellow"
              onClick={() =>
                (window.location.href = productInfo?.product_url || "#")
              }>
              Visit Product Page
            </Button>
          </Dialog.Footer>
          <Dialog.CloseTrigger asChild>
            <CloseButton size="sm" />
          </Dialog.CloseTrigger>
        </Dialog.Content>
      </Dialog.Positioner>
    </Portal>
  );
}
