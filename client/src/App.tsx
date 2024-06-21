import "./App.css";
import { Center } from "@chakra-ui/react";
import Map from "./components/Map.tsx";
import Widget from "./components/Widget";
import { Dispatch, SetStateAction, createContext, useState } from "react";
import { Toaster } from "react-hot-toast";
import { LatLngLiteral } from "leaflet";

export type Shop = {
  id: string;
  name: string;
  lng: number;
  lat: number;
  card_payment: boolean;
  flavors: string[];
  distance: number;
};
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

function App() {
  const [locationOnMap, setLocationOnMap] = useState(defaultLocation);
  return (
    <Center>
      <Toaster />
      <LocationOnMapContext.Provider
        value={{
          locationOnMap,
          setLocationOnMap,
        }}
      >
        <Map />
        <Widget />
      </LocationOnMapContext.Provider>
    </Center>
  );
}

export default App;
