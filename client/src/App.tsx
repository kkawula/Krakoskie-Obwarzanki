import "./App.css";
import { Center } from "@chakra-ui/react";
import Map from "./components/Map.tsx";
import Widget from "./components/Widget";
import { Toaster } from "react-hot-toast";
import { LocationOnMapProvider } from "./context/locationContextProvider.tsx";
import AuthProvider from "react-auth-kit/AuthProvider";
import createStore from "react-auth-kit/createStore";
import UserAvatar from "./components/auth/UserAvatar.tsx";

const store = createStore({
  authName: "_auth",
  authType: "cookie",
  cookieDomain: window.location.hostname,
  cookieSecure: window.location.protocol === "https:",
});
function App() {
  return (
    <Center>
      <AuthProvider store={store}>
        <Toaster />
        <LocationOnMapProvider>
          <UserAvatar />
          <Map />
          <Widget />
        </LocationOnMapProvider>
      </AuthProvider>
    </Center>
  );
}

export default App;
