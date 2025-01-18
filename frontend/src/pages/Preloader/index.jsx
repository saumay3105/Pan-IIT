import React from "react";
import "./Preloader.css";

function Preloader() {
  return (
    <div className="preloader">
      <div className="preloader-logo">
        <span className="preloader-text">ReadMe</span>
        <span className="preloader-dot">.ai</span>
      </div>
      <div className="loader-bar"></div>
    </div>
  );
}

export default Preloader;
