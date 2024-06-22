import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  ZoomControl,
} from "react-leaflet";
import LocationMarker, { customIcon } from "./AddNewMarker";
import { useContext } from "react";
import { LocationOnMapContext, defaultLocation } from "../App";
import { useFetchShops } from "../hooks/useFetchShops";
import { Alert, AlertDescription, AlertTitle } from "@chakra-ui/react";

// export type IMarker = {
//   id: string;
//   name: string;
//   lng: number;
//   lat: number;
//   card_payment: boolean;
//   flavors: string[];
// };

// export const MarkerSetter = createContext<(marker: IMarker) => void>(() => {
//   throw new Error("MarkerSetter not implemented");
// });

function Map() {
  const { locationOnMap } = useContext(LocationOnMapContext);

  const { data: shops, isError, error } = useFetchShops(locationOnMap);

  return (
    <MapContainer
      center={defaultLocation.location}
      zoom={14}
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <LocationMarker />

      {isError && (
        <Alert>
          <AlertTitle> Error when fetching </AlertTitle>
          <AlertDescription>Error: {error.message}</AlertDescription>
        </Alert>
      )}

      {shops?.map((shop, index) => (
        <Marker key={index} position={shop} icon={customIcon}>
          <Popup>{shop.name}</Popup>
        </Marker>
      ))}
      <ZoomControl position="topright" />
    </MapContainer>
  );
}

export default Map;
