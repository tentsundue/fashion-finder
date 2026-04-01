import { CaretLeftFilled, CaretRightFilled } from "@ant-design/icons";
import { Box, Carousel, IconButton, Image } from "@chakra-ui/react";
import { useState } from "react";

interface ImageCarouselProps {
  color_to_s3_url: Record<string, string>;
  productName: string;
  verticalView?: boolean;
}

export default function ImageCarousel({
  color_to_s3_url,
  productName,
  verticalView = false,
}: ImageCarouselProps) {
  const [carouselPage, setCarouselPage] = useState(0);

  const carouselIndicators = (
    <Carousel.IndicatorGroup gap={5} justifyContent="center">
      {Object.entries(color_to_s3_url).map(([color, _], index) => (
        <Carousel.Indicator
          key={index}
          index={index}
          cursor="pointer"
          unstyled
          _current={{
            outline: `2px solid ${color}`,
            rounded: "full",
            outlineOffset: "2px",
          }}
          onClick={(e) => e.stopPropagation()}>
          <Box
            width="20px"
            height="20px"
            borderRadius="50%"
            backgroundColor={color}
            opacity={carouselPage === index ? 1 : 0.5}
            _hover={{ opacity: 0.8 }}
          />
        </Carousel.Indicator>
      ))}
    </Carousel.IndicatorGroup>
  );
  return (
    <Carousel.Root
      autoplay={verticalView ? { delay: 3000 } : false}
      orientation={verticalView ? "vertical" : "horizontal"}
      slideCount={Object.keys(color_to_s3_url).length}
      position="relative"
      h={verticalView ? "600px" : "500px"}
      w={verticalView ? "800px" : "360px"}
      maxH="100%"
      maxW="100%"
      mx="auto"
      pb="20px"
      page={carouselPage}
      onPageChange={(e) => setCarouselPage(e.page)}
      allowMouseDrag>
      {verticalView ? (
        <>
          {carouselIndicators}
          <Carousel.ItemGroup>
            {Object.entries(color_to_s3_url).map(([color, url], index) => (
              <Carousel.Item key={index} index={index}>
                <Image
                  aspectRatio="16/9"
                  src={url}
                  alt={"Image of " + productName + " in " + color}
                  w="100%"
                  h="100%"
                  objectFit="cover"
                />
              </Carousel.Item>
            ))}
          </Carousel.ItemGroup>
        </>
      ) : (
        <>
          <Carousel.Control
            h="100%"
            justifyContent="space-between"
            gap="10"
            width="full">
            <Carousel.PrevTrigger asChild>
              <IconButton
                position="absolute"
                left="8px"
                top="50%"
                transform="translateY(-50%)"
                zIndex={2}
                size="sm"
                variant="ghost"
                bg="rgba(255,255,255,0.6)"
                _hover={{ bg: "rgba(255,255,255,0.9)" }}
                onClick={(e) => e.stopPropagation()}>
                <CaretLeftFilled />
              </IconButton>
            </Carousel.PrevTrigger>
            <Carousel.ItemGroup>
              {Object.entries(color_to_s3_url).map(([color, url], index) => (
                <Carousel.Item key={index} index={index}>
                  <Image
                    src={url}
                    alt={"Image of " + productName + " in " + color}
                    w="100%"
                    h="100%"
                    objectFit="cover"
                  />
                </Carousel.Item>
              ))}
            </Carousel.ItemGroup>
            <Carousel.NextTrigger asChild>
              <IconButton
                position="absolute"
                right="8px"
                top="50%"
                transform="translateY(-50%)"
                zIndex={2}
                size="sm"
                variant="ghost"
                bg="rgba(255,255,255,0.6)"
                _hover={{ bg: "rgba(255,255,255,0.9)" }}
                onClick={(e) => e.stopPropagation()}>
                <CaretRightFilled />
              </IconButton>
            </Carousel.NextTrigger>
          </Carousel.Control>
          {carouselIndicators}
        </>
      )}
    </Carousel.Root>
  );
}
