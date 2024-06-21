import { useState } from "react";
import { Marker, Popup, useMapEvents } from "react-leaflet";
import AddShop from "./AddShop";
import L, { type LatLngLiteral } from "leaflet";
import icon from "../assets/icon_ob.png";

export const customIcon = new L.Icon({
  iconUrl: icon,
  iconSize: [36, 36],
});

function LocationMarker() {
  const [position, setPosition] = useState<LatLngLiteral | null>(null);
  const [setupOpen, setSetupOpen] = useState(false);

  const map = useMapEvents({
    click(e) {
      setPosition(e.latlng);
      map.flyTo(e.latlng, map.getZoom());
      setSetupOpen(true);
    },
  });

  return (
    position && (
      <>
        <Marker key={position.lat} position={position} icon={customIcon}>
          <Popup>You are here</Popup>
        </Marker>
        <AddShop
          position={position}
          isOpen={setupOpen}
          onClose={() => {
            setSetupOpen(false);
          }}
        />
      </>
    )
  );
}

export default LocationMarker;
