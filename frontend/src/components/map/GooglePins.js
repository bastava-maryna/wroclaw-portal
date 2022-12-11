/* eslint-disable prettier/prettier */
import React from 'react';

const GooglePins = (props) => {
  const handleChange = (e) => {
    //let activeCategories = [...props.selectedPinCategories];
    if (props.selectedPinCategories.includes(e)) {
      props.onPinSelection(
        props.selectedPinCategories.filter((pin) => {
          return pin !== e;
        })
      );
    } else {
      props.onPinSelection([...props.selectedPinCategories, e]);
    }
  };
  //console.log(props);
  return (
    <div>
      <h3>Markers</h3>

      {Object.entries(props.pinCategories).map((entry) => {
        console.log(entry[1].key);
        return (
          <div>
            <input
              type="checkbox"
              key={entry[1].key}
              checked={props.selectedPinCategories.includes(entry[1].key)}
              onChange={() => handleChange(entry[1].key)}
            ></input>
            <label className="ml-2"> {entry[1].name} </label>
          </div>
        );
        //console.log(entry, entry.key, entry.value);
      })}
    </div>
  );
};

export default GooglePins;
