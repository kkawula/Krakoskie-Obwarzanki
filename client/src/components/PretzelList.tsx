import { Box, Text, Flex, Badge } from "@chakra-ui/react";
import { useContext, useEffect } from "react";
import { useFetchShops } from "../hooks/useFetchShops";
import { LocationOnMapContext } from "../App";
import toast from "react-hot-toast";

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
  const { locationOnMap } = useContext(LocationOnMapContext);

  const {
    data: shops,
    isLoading,
    isError,
    error,
  } = useFetchShops(locationOnMap);

  useEffect(() => {
    if (isError) {
      toast.error(`Something went wrong: ${error.message}`);
    }
  }, [isError]);

  if (isLoading)
    return (
      <Box>
        <Text>Loading...</Text>
      </Box>
    );
  if (isError)
    return (
      <Box>
        <Text>Error: {error.message}</Text>
      </Box>
    );

  return (
    <Box maxH="400px" overflowY="auto">
      {shops?.map((seller, index) => (
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
