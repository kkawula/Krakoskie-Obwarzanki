import { useState } from "react";
import { Marker, Popup, useMapEvents } from "react-leaflet";
import AddShop from "./AddShop";
import L, { LatLngLiteral } from "leaflet";
import icon from "../assets/icon_ob.png";

export const customIcon = new L.Icon({
  iconUrl: icon,
  iconSize: [36, 36],
});

let position: LatLngLiteral | null = null;

function LocationMarker() {
  const [isAddingNewShopOpen, setIsAddingNewShopOpen] = useState(false);

  const map = useMapEvents({
    click(e) {
      position = e.latlng;
      map.flyTo(e.latlng, map.getZoom());
      setIsAddingNewShopOpen(true);
    },
  });

  return (
    position && (
      <>
        <Marker key={position.lat} position={position} icon={customIcon}>
          <Popup>You are here</Popup> {/* gdzie ten popup? */}
        </Marker>
        <AddShop
          position={position}
          isOpen={isAddingNewShopOpen}
          onClose={() => {
            setIsAddingNewShopOpen(false);
            position = null;
          }}
        />
      </>
    )
  );
}

export default LocationMarker;
