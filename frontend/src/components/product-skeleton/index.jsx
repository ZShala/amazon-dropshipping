import React from 'react';
import './product-skeleton.styles.scss';

const ProductSkeleton = () => {
    return (
        <div className="product-skeleton">
            <div className="image-skeleton pulse"></div>
            <div className="content-skeleton">
                <div className="title-skeleton pulse"></div>
                <div className="rating-skeleton pulse"></div>
                <div className="review-skeleton pulse"></div>
            </div>
        </div>
    );
};

export default ProductSkeleton; 