"use client";

import { ChakraProvider, defaultSystem } from "@chakra-ui/react";
import { ThemeProvider } from "next-themes";
import { system } from "./theme";

export function Provider(props: { children: React.ReactNode }) {
  return (
    <ChakraProvider value={system || defaultSystem}>
      <ThemeProvider attribute="class">{props.children}</ThemeProvider>
    </ChakraProvider>
  );
}
