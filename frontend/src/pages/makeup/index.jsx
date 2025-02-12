import React from "react";
import CategoryProducts from '../../components/category-products';
import SEO from '../../components/seo';

const Makeup = () => {
    return (
        <>
            <SEO 
                title="Makeup Products | Premium Cosmetics Collection"
                description="Shop premium makeup and cosmetics from top Amazon brands. Find lipsticks, mascaras, foundations and more with fast Prime delivery."
            />
            <div>
                <CategoryProducts categoryType="makeup" />
            </div>
        </>
    )
}

export default Makeup;