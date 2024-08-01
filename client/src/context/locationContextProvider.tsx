import { LatLngLiteral } from "leaflet";
import {
  Dispatch,
  ReactNode,
  SetStateAction,
  createContext,
  useContext,
  useState,
} from "react";

export type LocationOnMap = {
  location: LatLngLiteral;
  radius: number;
};

export const defaultLocation: LocationOnMap = {
  location: { lat: 50.048774, lng: 19.965303 },
  radius: 1000000,
};

const LocationOnMapContext = createContext<{
  locationOnMap: LocationOnMap;
  setLocationOnMap: Dispatch<SetStateAction<LocationOnMap>>;
}>({
  locationOnMap: defaultLocation,
  setLocationOnMap: () => {},
});

export function LocationOnMapProvider({ children }: { children: ReactNode }) {
  const [locationOnMap, setLocationOnMap] = useState(defaultLocation);

  return (
    <LocationOnMapContext.Provider value={{ locationOnMap, setLocationOnMap }}>
      {children}
    </LocationOnMapContext.Provider>
  );
}

export const useLocationOnMapContext = () => useContext(LocationOnMapContext);
