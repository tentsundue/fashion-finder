import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

const config = defineConfig({
  theme: {
    tokens: {
      fonts: {
        body: { value: "sans-serif" },
      },
    },
    semanticTokens: {
      colors: {
        siteBg: {
          value: {
            _light: "{colors.gray.300}",
            _dark: "{colors.gray.800}",
          },
        },
        cardBg: {
          value: {
            _light: "{colors.gray.100}",
            _dark: "{colors.gray.700}",
          },
        },
        secondaryTextColor: {
          value: {
            _light: "{colors.gray.500}",
            _dark: "{colors.white}",
          },
        },
      },
    },
  },
});

export const system = createSystem(defaultConfig, config);
