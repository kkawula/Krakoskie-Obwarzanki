import "./App.css";
import { Center } from "@chakra-ui/react";
import Map from "./components/Map.tsx";
import Widget from "./components/Widget";
function App() {
  return (
    <Center>
      <Map />
      <Widget />
    </Center>
  );
}

export default App;
