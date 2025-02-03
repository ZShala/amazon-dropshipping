import React from 'react';
import CategoryProducts from '../../components/category-products';
import SEO from '../../components/seo';

const Fragrance = () => {
    return (
        <>
            <SEO 
                title="Fragrances | Luxury Perfumes Collection"
                description="Explore our collection of luxury perfumes and fragrances from Amazon. Shop designer scents with authentic product guarantee and Prime shipping."
            />
            <div className="fragrance-page">
                <CategoryProducts categoryType="fragrance" />
            </div>
        </>
    );
};

export default Fragrance;
