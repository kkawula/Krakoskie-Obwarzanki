import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Shop } from "../App";
import { NewShop } from "../components/NewShopForm";
import { LocationOnMap } from "../context/locationContextProvider";
import { sendPostRequest } from "../utils/sendPostRequest";

const fetchSellersWithinRadius = ({ location, radius }: LocationOnMap) =>
  sendPostRequest({
    url: "/shops/by_distance/",
    data: {
      ...location,
      radius,
    },
  });

export const useShopsQuery = (locationOnMap: LocationOnMap) =>
  useQuery({
    queryKey: ["shops", locationOnMap],
    queryFn: (): Promise<Array<Shop>> =>
      fetchSellersWithinRadius(locationOnMap),
    staleTime: 1000 * 60 * 5,
    retry: 1,
  });

const addShop = (shop: NewShop) =>
  sendPostRequest({ url: "/shops", data: shop });

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
