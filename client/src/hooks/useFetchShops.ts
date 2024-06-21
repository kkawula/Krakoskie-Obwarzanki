import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { LocationOnMap, Shop } from "../App";
import { usePost } from "./usePost";
import { NewShop } from "../components/AddShop";

const post = usePost();
const fetchSellersWithinRadius = ({ location, radius }: LocationOnMap) => {
  return post("/shops/by_distance/", {
    ...location,
    radius,
  });
};
export const useFetchShops = (locationOnMap: LocationOnMap) =>
  useQuery({
    queryKey: ["shops", locationOnMap],
    queryFn: (): Promise<Array<Shop>> =>
      fetchSellersWithinRadius(locationOnMap),
    staleTime: 1000 * 60 * 5,
  });

const addShop = (shop: NewShop) => post("/shops", shop);

export const useAddShopMutation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: addShop,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["shops"] });
    },
    onError: (error) => {
      console.error(error);
    },
  });
};
