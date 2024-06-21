import { Box, Text, Flex, Badge } from "@chakra-ui/react";
import { useEffect, useState } from "react";

type Seller = {
  id: string;
  name: string;
  lng: number;
  lat: number;
  card_payment: boolean;
  flavors: string[];
  distance: number;
};

enum Flavor {
  Ser = "Ser",
  Mak = "Mak",
  Mieszany = "Mieszany",
  Sól = "Sól",
}

const colorSchemeMap: { [key in Flavor]?: string } = {
  [Flavor.Ser]: "yellow",
  [Flavor.Mak]: "green",
  [Flavor.Mieszany]: "pink",
  [Flavor.Sól]: "white",
};

const borderMap: { [key in Flavor]?: string } = {
  [Flavor.Sól]: "1px",
};

export default function PretzelList() {
  const [sellers, setSellers] = useState<Seller[]>([]);
  const radius: number = 1000000;

  const fetchSellersWithinRadius = async (radius: number) => {
    try {
      const body = JSON.stringify({
        lat: 50.048774,
        lng: 19.965303,
        radius,
      });
      const response = await fetch("http://127.0.0.1:8000/shops/by_distance/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body,
      });
      if (response.ok) {
        const data: Seller[] = await response.json();
        setSellers(data);
      } else {
        console.error("Failed to fetch sellers:", response.statusText);
      }
    } catch (error) {
      console.error("An error occurred while fetching sellers:", error);
    }
  };

  useEffect(() => {
    fetchSellersWithinRadius(radius).catch(console.error);
  }, [radius]);

  return (
    <Box maxH="400px" overflowY="auto">
      {sellers.map((seller, index) => (
        <Box key={index} p="4" mb="4" borderWidth="1px" borderRadius="lg">
          <Flex direction="column">
            <Flex direction="row">
              <Text fontSize="s" fontWeight="bold" marginRight={3}>
                {seller.name}
              </Text>
              <Text>{`${(seller.distance / 1000).toFixed(2)} km`}</Text>
            </Flex>
            <Flex direction="row">
              {seller.flavors.map((flavor, index) => {
                return (
                  <Badge
                    key={index}
                    colorScheme={colorSchemeMap[flavor as Flavor] || "gray"}
                    width="min"
                    border={borderMap[flavor as Flavor] || "0px"}
                    marginRight={1}
                  >
                    {flavor}
                  </Badge>
                );
              })}
            </Flex>
          </Flex>
        </Box>
      ))}
    </Box>
  );
}
