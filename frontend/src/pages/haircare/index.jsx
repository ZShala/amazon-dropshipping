import React from "react";
import CategoryProducts from '../../components/category-products';
import SEO from '../../components/seo';

import "./haircare.styles.scss";

const Haircare = () => {
    return (
        <>
            <SEO 
                title="Hair Care Products | Professional Hair Solutions"
                description="Shop professional haircare products from Amazon. Find shampoos, conditioners, treatments and styling products with Prime delivery."
            />
            <div className="haircare-page">
                <CategoryProducts categoryType="haircare" />
            </div>
        </>
    )
}

export default Haircare;