import "./App.css";
import { Center } from "@chakra-ui/react";
import Map from "./components/Map.tsx";
import Widget from "./components/Widget";
import { Toaster } from "react-hot-toast";
import { LocationOnMapProvider } from "./context/locationContextProvider.tsx";

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
  return (
    <Center>
      <Toaster />
      <LocationOnMapProvider>
        <Map />
        <Widget />
      </LocationOnMapProvider>
    </Center>
  );
}

export default App;
