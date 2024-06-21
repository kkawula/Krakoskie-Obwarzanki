import { Box, Text, Flex, Badge } from "@chakra-ui/react";
import { useContext, useEffect } from "react";
import { useFetchShops } from "../hooks/useFetchShops";
import { LocationOnMapContext } from "../App";
import toast from "react-hot-toast";

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
                {`${seller.name}`}
              </Text>
              <Text>{`${(seller.distance / 1000).toFixed(2)} km`}</Text>
            </Flex>
            <Flex direction="row">
              {seller.flavors.map((flavor, index) => {
                let colorScheme: string;
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
