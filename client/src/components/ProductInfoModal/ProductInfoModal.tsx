import type { ProductInfo } from "@/types/product";
import {
  Button,
  Text,
  CloseButton,
  Dialog,
  Flex,
  Portal,
  Separator,
} from "@chakra-ui/react";
import ImageCarousel from "../ImageCarousel/ImageCarousel";

interface InfoModalProps {
  productInfo: ProductInfo | null;
}

export default function ProductInfoModal({ productInfo }: InfoModalProps) {
  return (
    <Portal>
      <Dialog.Backdrop />
      <Dialog.Positioner>
        <Dialog.Content
          maxW="5xl"
          w="100%"
          h="50%"
          borderRadius="md"
          p={5}
          bg="white"
          mx="auto">
          <Dialog.Header>
            <Dialog.Title fontSize="4xl" lineHeight={1}>
              {productInfo?.name}
            </Dialog.Title>
          </Dialog.Header>
          <Separator my={4} />
          <Dialog.Body>
            <Flex direction="row" alignItems="center" gap={10} mb={4}>
              {productInfo && (
                <ImageCarousel
                  color_to_s3_url={productInfo.color_to_s3_url}
                  productName={productInfo.name}
                  verticalView={true}
                />
              )}
              <Flex direction="column" gap={2}>
                <Text fontSize="lg" fontWeight="bold">
                  {productInfo?.brand}
                </Text>
                <Text fontSize="md" color="gray.600"></Text>
              </Flex>
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
                eiusmod tempor incididunt ut labore et dod
              </p>
            </Flex>
          </Dialog.Body>
          <Dialog.Footer>
            <Dialog.ActionTrigger asChild>
              <Button colorPalette="red" variant="outline">
                Close
              </Button>
            </Dialog.ActionTrigger>
            <Button colorPalette="yellow">Visit Product Page</Button>
          </Dialog.Footer>
          <Dialog.CloseTrigger asChild>
            <CloseButton size="sm" />
          </Dialog.CloseTrigger>
        </Dialog.Content>
      </Dialog.Positioner>
    </Portal>
  );
}
