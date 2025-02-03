import React from "react";
import CategoryProducts from '../../components/category-products';
import SEO from '../../components/seo';

import "./skincare.styles.scss";

const Skincare = () => {
    return (
        <>
            <SEO 
                title="Skincare Products | Luxury Skincare Collection"
                description="Discover luxury skincare products for radiant, healthy skin. Shop cleansers, moisturizers, serums and treatments with Amazon Prime shipping."
            />
            <div className="skincare-page">
                <CategoryProducts categoryType="skincare" />
            </div>
        </>
    )
}

export default Skincare;