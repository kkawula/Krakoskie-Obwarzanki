import { LatLngLiteral } from "leaflet";
import { Dispatch, SetStateAction, createContext } from "react";

export type LocationOnMap = {
  location: LatLngLiteral;
  radius: number;
};

export const defaultLocation: LocationOnMap = {
  location: { lat: 50.048774, lng: 19.965303 },
  radius: 1000000,
};

export const LocationOnMapContext = createContext<{
  locationOnMap: LocationOnMap;
  setLocationOnMap: Dispatch<SetStateAction<LocationOnMap>>;
}>({
  locationOnMap: defaultLocation,
  setLocationOnMap: () => {
    throw new Error("setLocationOnMap not implemented");
  },
});
