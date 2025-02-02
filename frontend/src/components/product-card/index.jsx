import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Toast from '../toast';
import './product-card.styles.scss';

const ProductCard = ({ 
    product, 
    similarityScore, 
    trendingScore,
    recommendationReason,
    categoryScore,
    bundleDiscount,
    comparisonFeatures
}) => {
    const [imageError, setImageError] = useState(false);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [showToast, setShowToast] = useState(false);
    
    const defaultImage = "https://via.placeholder.com/300x300?text=Beauty+Product";
    
    const handleImageError = () => {
        console.log('Image failed to load:', product.image_url);
        setImageError(true);
    };

    const handleAddToCart = () => {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const existingProduct = cart.find(item => item.ProductId === product.ProductId);
        
        if (existingProduct) {
            existingProduct.quantity += 1;
        } else {
            cart.push({
                ...product,
                quantity: 1
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        
        // Lësho një event për të njoftuar ndryshimin në shportë
        window.dispatchEvent(new Event('cartUpdated'));
        
        // Shfaq toast-in
        setShowToast(true);
        
        // Fshije toast-in pas 3 sekondash
        setTimeout(() => {
            setShowToast(false);
        }, 3000);
    };

    return (
        <>
            <div className="product-card">
                <Link to={`/product/${product.ProductId}`} className="product-link">
                    <div className="image-container">
                        <img 
                            src={imageError ? defaultImage : (product.image_url || defaultImage)}
                            alt={product.ProductType}
                            className="product-image"
                            onError={handleImageError}
                            loading="lazy"
                        />
                        <div className="view-details">
                            <span>View Details</span>
                        </div>
                    </div>
                </Link>
                <div className="product-info">
                    <h3>{product.ProductType}</h3>
                    <div className="rating">
                        <span>★</span> {product.Rating}
                        {product.ReviewCount && (
                            <span className="review-count">({product.ReviewCount} reviews)</span>
                        )}
                    </div>
                    
                    {/* Trego scores të ndryshme bazuar në kontekstin */}
                    {similarityScore && (
                        <div className="similarity-score">
                            Similarity: {similarityScore.toFixed(2)}
                        </div>
                    )}
                    {trendingScore && (
                        <div className="trending-score">
                            Trending Score: {trendingScore.toFixed(2)}
                        </div>
                    )}
                    {recommendationReason && (
                        <div className="recommendation-reason">
                            {recommendationReason}
                        </div>
                    )}
                    {categoryScore && (
                        <div className="category-score">
                            Category Score: {categoryScore.toFixed(2)}
                        </div>
                    )}
                    {bundleDiscount && (
                        <div className="bundle-discount">
                            Save {bundleDiscount}% in bundle
                        </div>
                    )}
                    {comparisonFeatures && (
                        <div className="comparison-features">
                            {comparisonFeatures}
                        </div>
                    )}
                    <button 
                        className="add-to-cart-btn"
                        onClick={handleAddToCart}
                    >
                        Add to Cart
                    </button>
                </div>
            </div>
            
            <Toast 
                message="Produkti u shtua në shportë!"
                isVisible={showToast}
                onClose={() => setShowToast(false)}
            />
        </>
    );
};

export default ProductCard; 