import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  ZoomControl,
} from "react-leaflet";
import LocationMarker, { customIcon } from "./AddNewMarker";
import { createContext, useEffect, useState } from "react";

export type IMarker = {
  id: string;
  name: string;
  lng: number;
  lat: number;
  card_payment: boolean;
  flavors: string[];
};

export const MarkerSetter = createContext<(marker: IMarker) => void>(() => {});

export default function Map() {
  const Cracow = { lat: 50.061389, lng: 19.938333 };

  const [markers, setMarkers] = useState<IMarker[]>([]);
  const [newMarker, setNewMarker] = useState<IMarker | null>(null);

  const handleMarker = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/shops`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const data: IMarker[] = await response.json();
        setMarkers(data);
      } else {
        console.error("Failed to fetch marker:", response.statusText);
      }
    } catch (error) {
      console.error("An error occurred while fetching marker:", error);
    }
  };

  useEffect(() => {
    handleMarker().catch(console.error);
  }, [newMarker]);

  return (
    <MapContainer center={Cracow} zoom={14} zoomControl={false}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <MarkerSetter.Provider value={setNewMarker}>
        <LocationMarker />
      </MarkerSetter.Provider>
      {markers.map((marker, index) => (
        <Marker key={index} position={marker} icon={customIcon}>
          <Popup>{marker.name}</Popup>
        </Marker>
      ))}
      <ZoomControl position="topright" />
    </MapContainer>
  );
}
