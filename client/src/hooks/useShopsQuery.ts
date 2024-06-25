import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Shop } from "../App";
import { sendPostRequest } from "../utils/sendPostRequest";
import { NewShop } from "../components/NewShopForm";
import { LocationOnMap } from "../context/locationContextProvider";

const fetchSellersWithinRadius = ({ location, radius }: LocationOnMap) => {
  return sendPostRequest({
    url: "/shops/by_distance/",
    data: {
      ...location,
      radius,
    },
  });
};
export const useShopsQuery = (locationOnMap: LocationOnMap) =>
  useQuery({
    queryKey: ["shops", locationOnMap],
    queryFn: (): Promise<Array<Shop>> =>
      fetchSellersWithinRadius(locationOnMap),
    staleTime: 1000 * 60 * 5,
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
