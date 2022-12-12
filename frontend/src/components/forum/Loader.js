import React from 'react';
import './style.css';

const Loader = (props) => {
  return (
    <div className={props.className || 'loader'}>
      <div className="loader-spinning-wheel" />
    </div>
  );
};
export default Loader;
