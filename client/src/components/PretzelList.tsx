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

export default function PretzelList() {
  const [sellers, setSellers] = useState<Seller[]>([]);

  const handleSellers = async () => {
    try {
      const body = JSON.stringify({
        lat: 50.048774,
        lng: 19.965303,
        radius: 1000000,
      });
      const response = await fetch(`http://127.0.0.1:8000/shops/by_distance/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body,
      });
      if (response.ok) {
        const data: Seller[] = await response.json();
        setSellers(data);
        console.log("Sellers fetched:", data);
      } else {
        console.error("Failed to fetch sellers:", response.statusText);
      }
    } catch (error) {
      console.error("An error occurred while fetching sellers:", error);
    }
  };

  useEffect(() => {
    handleSellers().catch(console.error);
  }, []);

  return (
    <Box maxH="400px" overflowY="auto">
      {sellers.map((seller, index) => (
        <Box key={index} p="4" mb="4" borderWidth="1px" borderRadius="lg">
          <Flex direction="column">
            <Flex direction="row">
              <Text fontSize="s" fontWeight="bold" marginRight={3}>
                {`${seller.name}`}
              </Text>
              <Text>{`${(seller.distance / 1000).toFixed(2)} km`}</Text>
            </Flex>
            <Flex direction="row">
              {seller.flavors.map((flavor, index) => {
                let colorScheme;
                let border = "0px";
                switch (flavor) {
                  case "Ser":
                    colorScheme = "yellow";
                    break;
                  case "Mak":
                    colorScheme = "green";
                    break;
                  case "Mieszany":
                    colorScheme = "pink";
                    break;
                  case "Sól":
                    colorScheme = "white";
                    border = "1px";
                    break;
                  default:
                    colorScheme = "gray";
                }

                return (
                  <Badge
                    key={index}
                    colorScheme={colorScheme}
                    width="min"
                    border={border}
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
