import React, { useEffect, useMemo } from 'react';
import { MapContainer as LeafletMap, MapLayer, TileLayer } from 'react-leaflet';

import './Map.css'

const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";


function Map({ height }) {
  
  return (
      <div style={{ height: height ? height : "100vh" }}>
        <LeafletMap
          key={(new Date()).getSeconds()}
          style={{ width: "100%", height: "100%" }}
          zoom={13}
          maxZoom={20}
          zoomControl={false}
          center={[6.136629, 1.222186]}
          onClick={() => {
            alert("ok")
          }}
        >
          <TileLayer
            url={url}
          />
        
        </LeafletMap>
      </div>
  );
}

export default Map 