import React from "react";
import { Center, Text, VStack, HStack } from "@chakra-ui/react";

import {
  PieChart,
  Pie,
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#F28042",
  "#9fd3c7",
  "#142d4c",
  "#feff9a",
  "#ffb6b9",
  "#fae3d9",
  "#bbded6",
  "#61c0bf",
];

export default function Visualization({ rollups }) {
  return (
    <Center>
      <VStack>
        <Text>Cost vs Equity</Text>
        <BarChart
          width={600}
          height={300}
          data={rollups}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <XAxis dataKey="symbol" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="total_equity" fill="#00C49F" />
          <Bar dataKey="total_cost" fill="#FFBB28" />
        </BarChart>
        <HStack>
          <VStack>
            <Text>Cost Distribution</Text>
            <PieChart width={250} height={250}>
              <Pie data={rollups} dataKey="total_cost" nameKey="symbol">
                {rollups.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Legend></Legend>
              <Tooltip></Tooltip>
            </PieChart>
          </VStack>
          <VStack>
            <Text>Equity Distribution</Text>
            <PieChart width={250} height={250}>
              <Pie data={rollups} dataKey="total_equity" nameKey="symbol">
                {rollups.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Legend></Legend>
              <Tooltip></Tooltip>
            </PieChart>
          </VStack>
        </HStack>
      </VStack>
    </Center>
  );
}
