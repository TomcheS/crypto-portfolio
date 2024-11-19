import React from "react";
import { Container, Text, VStack, HStack } from "@chakra-ui/react";

export default function Summary({
  portfolioCost,
  portfolioValue,
  absoluteGain,
  totalGainPercent,
}) {
  return (
    <HStack spacing={6}>
      <Container bg="tomato">
        <VStack width={40}>
          <Text fontSize="2xl">
            $ {Number(portfolioCost.toFixed(2)).toLocaleString()}
          </Text>
          <Text fontSize="xs" size="md">
            Portfolio Cost
          </Text>
        </VStack>
      </Container>
      <Container bg="tomato">
        <VStack width={40}>
          <Text fontSize="2xl">
            $ {Number(portfolioValue.toFixed(2)).toLocaleString()}
          </Text>
          <Text fontSize="xs">Portfolio Value</Text>
        </VStack>
      </Container>
      <Container bg="tomato">
        <VStack width={40}>
          <Text fontSize="2xl">
            $ {Number(absoluteGain.toFixed(2)).toLocaleString()}
          </Text>
          <Text fontSize="xs"> Absolute Gain / Loss </Text>
        </VStack>
      </Container>
      <Container bg="tomato">
        <VStack width={40}>
          <Text fontSize="2xl">{totalGainPercent.toFixed(2)} %</Text>
          <Text fontSize="xs">Gain / Loss %</Text>
        </VStack>
      </Container>
    </HStack>
  );
}
