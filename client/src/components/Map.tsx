import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  ZoomControl,
} from "react-leaflet";
import LocationMarker, { customIcon } from "./LocationMarker";
import { useShopsQuery } from "../hooks/useShopsQuery";
import { Alert, AlertDescription, AlertTitle } from "@chakra-ui/react";
import {
  defaultLocation,
  useLocationOnMapContext,
} from "../context/locationContextProvider";

function Map() {
  const { locationOnMap } = useLocationOnMapContext();

  const { data: shops, isError, error } = useShopsQuery(locationOnMap);
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
