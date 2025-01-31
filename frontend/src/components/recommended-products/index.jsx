import React from 'react';
import ProductCard from '../product-card';
import './recommended-products.styles.scss';

const RecommendedProducts = ({ products, type }) => {
    return (
        <div className={`recommended-products ${type}`}>
            {products.map(product => (
                <ProductCard
                    key={product.ProductId}
                    product={product}
                    bundleDiscount={type === 'crosssell' ? product.bundleDiscount : null}
                    comparisonFeatures={type === 'upsell' ? product.upgradeReason : null}
                />
            ))}
        </div>
    );
};

export default RecommendedProducts; 