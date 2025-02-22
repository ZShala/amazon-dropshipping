import React from "react";
import CategoryProducts from '../../components/category-products';
import SEO from '../../components/seo';
const Miscellaneous = () => {
    return (
        <>
            <SEO
                title="Miscellaneous Products | Luxury Beauty Collection"
                description="Discover luxury beauty products for radiant, healthy skin. Shop cleansers, moisturizers, serums and treatments with Amazon Prime shipping."
            />
            <div>
                <CategoryProducts categoryType="miscellaneous" />
            </div>
        </>
    )
}

export default Miscellaneous;