import React from "react";
import CategoryProducts from '../../components/category-products';

import "./haircare.styles.scss";

const Haircare = () => {
    return (
        <div className="haircare-page">
            <CategoryProducts categoryType="haircare" />
        </div>
    )
}

export default Haircare;