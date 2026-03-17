import { Flex, Text, Icon, Button, Portal, Menu } from "@chakra-ui/react";
import { Link } from "react-router-dom";
import { useColorMode } from "../ui/color-mode";
import { useNavigate } from "react-router-dom";
import { AiFillCaretDown, AiFillBulb, AiOutlineBulb } from "react-icons/ai";

export default function Navbar() {
  const { colorMode, toggleColorMode } = useColorMode();
  const navigate = useNavigate();

  return (
    <Flex
      as="nav"
      justify="space-between"
      align="center"
      padding="12px 24px"
      borderBottom="1px solid #ddd"
      backgroundColor={colorMode === "light" ? "#fff" : "#333"}>
      <Text
        _hover={{
          color: "blue.500",
          transform: "scale(1.01)",
        }}
        transition="all 0.3s ease"
        fontWeight="bold"
        cursor="pointer"
        onClick={() => navigate("/")}
        fontSize="lg"
        color={colorMode === "light" ? "gray.800" : "gray.300"}>
        Fashion Finder
      </Text>

      <Flex gap="16px">
        <Menu.Root positioning={{ placement: "bottom-end" }}>
          <Menu.Trigger asChild>
            <Button
              size="lg"
              variant="ghost"
              borderRadius="0"
              fontWeight="normal">
              Categories <Icon as={AiFillCaretDown} boxSize={4} />
            </Button>
          </Menu.Trigger>

          <Portal>
            <Menu.Positioner>
              <Menu.Content minW="160px">
                <Menu.Item asChild value="tops">
                  <Link
                    to="/products/categories/tops"
                    style={{ textDecoration: "none", color: "inherit" }}>
                    Tops
                  </Link>
                </Menu.Item>
                <Menu.Item asChild value="bottoms">
                  <Link
                    to="/products/categories/bottoms"
                    style={{ textDecoration: "none", color: "inherit" }}>
                    Bottoms
                  </Link>
                </Menu.Item>
                <Menu.Item asChild value="outerwear">
                  <Link
                    to="/products/categories/outerwear"
                    style={{ textDecoration: "none", color: "inherit" }}>
                    Outerwear
                  </Link>
                </Menu.Item>
                <Menu.Item asChild value="shoes">
                  <Link
                    to="/products/categories/shoes"
                    style={{ textDecoration: "none", color: "inherit" }}>
                    Shoes
                  </Link>
                </Menu.Item>
              </Menu.Content>
            </Menu.Positioner>
          </Portal>
        </Menu.Root>

        <Menu.Root positioning={{ placement: "bottom-end" }}>
          <Menu.Trigger asChild>
            <Button
              size="lg"
              variant="ghost"
              borderRadius="0"
              fontWeight="normal">
              Brands <Icon as={AiFillCaretDown} boxSize={4} />
            </Button>
          </Menu.Trigger>

          <Portal>
            <Menu.Positioner>
              <Menu.Content minW="160px">
                <Menu.Item asChild value="tops">
                  <Link
                    to="/products/brands/uniqlo"
                    style={{ textDecoration: "none", color: "inherit" }}>
                    Uniqlo
                  </Link>
                </Menu.Item>
                <Menu.Item asChild value="bottoms">
                  <Link
                    to="/products/brands/hm"
                    style={{ textDecoration: "none", color: "inherit" }}>
                    H&M
                  </Link>
                </Menu.Item>
                <Menu.Item asChild value="outerwear">
                  <Link
                    to="/products/brands/tbd"
                    style={{ textDecoration: "none", color: "inherit" }}>
                    TBD
                  </Link>
                </Menu.Item>
                <Menu.Item asChild value="shoes">
                  <Link
                    to="/products/brands/tbd"
                    style={{ textDecoration: "none", color: "inherit" }}>
                    TBD
                  </Link>
                </Menu.Item>
              </Menu.Content>
            </Menu.Positioner>
          </Portal>
        </Menu.Root>
      </Flex>

      <Icon
        as={colorMode === "light" ? AiOutlineBulb : AiFillBulb}
        boxSize={6}
        cursor="pointer"
        onClick={toggleColorMode}
        color={colorMode === "light" ? "gray.800" : "gray.300"}
      />
    </Flex>
  );
}
