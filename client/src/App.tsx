import "./App.css";
import { Center } from "@chakra-ui/react";
import Map from "./components/Map.tsx";
import Widget from "./components/Widget";
import { useState } from "react";
import { Toaster } from "react-hot-toast";
import {
  LocationOnMapContext,
  defaultLocation,
} from "./context/locationContext.ts";

export type Shop = {
  id: string;
  name: string;
  lng: number;
  lat: number;
  card_payment: boolean;
  flavors: string[];
  distance: number;
};

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
