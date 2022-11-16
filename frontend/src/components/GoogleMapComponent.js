import React from 'react';
import { Wrapper, Status } from '@googlemaps/react-wrapper';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const containerStyle = {
  width: '700px',
  height: '600px',
};
const center = {
  lat: 51.1077,
  lng: 17.0625,
};

const onLoad = (marker) => {
  console.log('marker: ', marker);
};

const GoogleMapComponent = (props) => {
  //console.log(props.pinCategories);
  return (
    <center>
      <br /> <br />
      <div>
        <Wrapper apiKey="AIzaSyBr6cQlTB8LQ1Rwf9ZZqIFfc7vl-2gxduk">
          <GoogleMap
            id="map1"
            mapContainerStyle={containerStyle}
            center={center}
            zoom={10}
          >
            {props.markerList.map((pin) => {
              if (props.pinCategories.includes(pin.cat))
                return <Marker id={pin} position={pin.position} />;
            })}
          </GoogleMap>
        </Wrapper>
      </div>
      <div></div>
    </center>
  );
};

export default GoogleMapComponent;
