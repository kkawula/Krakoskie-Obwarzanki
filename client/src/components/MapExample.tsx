import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  ZoomControl,
} from "react-leaflet";
import L from "leaflet";
import LocationMarker from "./AddNewMarker";
import icon from "/src/assets/icon_ob.png";
import { useEffect, useState } from "react";
// import LocationMarker from "./AddNewMarker";

const customIcon = new L.Icon({
  iconUrl: icon,
  iconSize: [36, 36],
});

interface Seller {
  id: string;
  name: string;
  longitude: number;
  latitude: number;
  card_payment: boolean;
  flavors: string[];
}

export default function MapExample() {
  const Cracow = { lat: 50.061389, lng: 19.938333 };
  const positions = [
    { lat: 50.061389, lng: 19.938333, popupText: "Pyszne obwarzaki" },
    { lat: 50.065723, lng: 19.919415, popupText: "Pyszne obwarzaki" },
    { lat: 50.064718, lng: 19.945654, popupText: "Pyszne obwarzaki" },
    { lat: 50.064389, lng: 19.91333, popupText: "Pyszne obwarzaki" },
    { lat: 50.069723, lng: 19.959415, popupText: "Pyszne obwarzaki" },
    { lat: 50.064418, lng: 19.95454, popupText: "Pyszne obwarzaki" },
  ];

  const [sellers, setSellers] = useState<Seller[]>([]);

  const handleSellers = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const data: Seller[] = await response.json();
        setSellers(data);
        console.log("Sellers fetched:", data);
      } else {
        console.error("Failed to fetch sellers:", response.statusText);
      }
    } catch (error) {
      console.error("An error occurred while fetching sellers:", error);
    }
  };

  useEffect(() => {
    handleSellers();
  }, []);

  return (
    <MapContainer
      center={Cracow}
      zoom={14}
      zoomControl={false}
      style={{ position: "relative" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <LocationMarker />
      {sellers.map((position, index) => (
        <Marker
          key={index}
          position={[position.longitude, position.latitude]}
          icon={customIcon}
        >
          <Popup>Pyszne obwarzaki</Popup>
        </Marker>
      ))}
      <ZoomControl position="topright" />
    </MapContainer>
  );
}
