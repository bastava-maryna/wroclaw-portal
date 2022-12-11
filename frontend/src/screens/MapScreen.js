/* eslint-disable prettier/prettier */
import React from 'react';
import axios from 'axios';
import GoogleMapComponent from '../components/map/GoogleMapComponent';
import GooglePins from '../components/map/GooglePins';
import { useState, useEffect } from 'react';

const pinCategories = {
  uni: {
    key: 'uni',
    name: 'Universities',
    icon: 'http://maps.gstatic.com/mapfiles/ms2/micons/red.png',
  },
  gov: {
    key: 'gov',
    name: 'Governmental buildings',
    icon: 'http://maps.gstatic.com/mapfiles/ms2/micons/lightblue.png',
  },
  dorm: {
    key: 'dorm',
    name: 'Dormentories',
    icon: 'http://maps.gstatic.com/mapfiles/ms2/micons/purple.png',
  },
};

const MapScreen = () => {
  const [pindata, setPinData] = useState();
  const [selectedPinCategories, setSelectedPinCategories] = useState([
    pinCategories.uni.key,
    pinCategories.gov.key,
    pinCategories.dorm.key,
  ]);

  console.log(pindata);
  useEffect(() => {
    const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';
    axios.get(`${API_URL}/map/map`).then((resp) => {
      setPinData(resp.data);
    });
  }, []);
  return (
    <div>
      <center>
        
        <GoogleMapComponent
          pinCategories={selectedPinCategories}
          markerList={pindata}
          rawPinCategories={pinCategories}
        />
        <GooglePins
          pinCategories={pinCategories}
          selectedPinCategories={selectedPinCategories}
          onPinSelection={setSelectedPinCategories}
        />
      </center>
    </div>
  );
};

export default MapScreen;
