import React from "react";
import CategoryProducts from '../../components/category-products';

import "./makeup.styles.scss";

const Makeup = () => {
    return (
        <div className="makeup-page">
            <CategoryProducts categoryType="makeup" />
        </div>
    )
}

export default Makeup;