import React from "react";
import CategoryProducts from '../../components/category-products';

import "./miscellaneous.styles.scss";

const Miscellaneous = () => {
    return (
        <div className="miscellaneous-page">
            <CategoryProducts categoryType="miscellaneous" />
        </div>
    )
}

export default Miscellaneous;