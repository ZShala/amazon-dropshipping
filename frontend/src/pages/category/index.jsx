import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import ProductRecommendations from '../../components/product-recommendation';
import './category.styles.scss';

const CategoryPage = () => {
    const { categoryId } = useParams();
    const [categoryProducts, setCategoryProducts] = useState([]);
    const [topRatedProduct, setTopRatedProduct] = useState(null);

    return (
        <div className="category-page">
            {/* Category header */}
            <div className="category-header">
                <h1>{categoryName}</h1>
            </div>

            {/* Products grid */}
            <div className="products-grid">
                {categoryProducts.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>

            {/* Recommendations based on top-rated product in category */}
            {topRatedProduct && (
                <div className="category-recommendations">
                    <h3>Produkte të ngjashme të vlerësuara lart</h3>
                    <ProductRecommendations 
                        productId={topRatedProduct.id}
                        limit={5}
                    />
                </div>
            )}
        </div>
    );
};

export default CategoryPage; 