import React from "react";
import CategoryProducts from '../../components/category-products';

import "./skincare.styles.scss";

const Skincare = () => {
    return (
        <div className="skincare-page">
            <CategoryProducts categoryType="skincare" />
        </div>
    )
}

export default Skincare;