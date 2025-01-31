import React from "react";
import { Link } from "react-router";
import "./menu-item.styles.scss";

const MenuItem = ({ imageUrl, productCategory, linkUrl }) => {
  return (
    <div className="menu-item">
      <div
        className="background-image"
        style={{
          backgroundImage: `url(${imageUrl})`,
        }}
      >
        <div className="overlay"></div>
      </div>
      <Link to={linkUrl} className="menu-button">
        {productCategory}
      </Link>
    </div>
  );
};

export default MenuItem;
