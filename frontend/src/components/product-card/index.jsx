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
        
        // Ensure price is a number
        const price = typeof product.price === 'string' 
            ? parseFloat(product.price) 
            : (typeof product.price === 'number' ? product.price : 29.99);
        
        const productToAdd = {
            ...product,
            price: price
        };
        
        if (existingProduct) {
            existingProduct.quantity += 1;
            existingProduct.price = price; // Update price if it changed
        } else {
            cart.push({
                ...productToAdd,
                quantity: 1
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        window.dispatchEvent(new Event('cartUpdated'));
        setShowToast(true);
        
        setTimeout(() => {
            setShowToast(false);
        }, 3000);
    };

    return (
        <>
            <div className="product-card">
                <Link 
                    to={`/product/${product.ProductId}`}
                    state={{ imageUrl: product.ImageURL }}
                >
                    <div className="image-container">
                        <img 
                            src={imageError ? defaultImage : (product.ImageURL || defaultImage)}
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
                    {console.log('product', product)}
                    <h3>{product.ProductTitle}</h3>
                    <div className="rating">
                        <span>★</span> {product.Rating}
                        {product.ReviewCount && (
                            <span className="review-count">({product.ReviewCount} reviews)</span>
                        )}
                    </div>
                    
                    {/* Modify the price section */}
                    {product.price !== undefined && (
                        <div className="price">
                            <span className="currency">€</span>
                            <span className="amount">
                                {typeof product.price === 'number' 
                                    ? product.price.toFixed(2) 
                                    : Number(product.price).toFixed(2)}
                            </span>
                        </div>
                    )}

                    {/* Trego scores të ndryshme bazuar në kontekstin */}
                    {similarityScore && (
                        <div className="similarity-score">
                            Similarity: {similarityScore (2)}
                        </div>
                    )}
                    {trendingScore && (
                        <div className="trending-score">
                            Trending Score: {trendingScore (2)}
                        </div>
                    )}
                    {recommendationReason && (
                        <div className="recommendation-reason">
                            {recommendationReason}
                        </div>
                    )}
                    {categoryScore && (
                        <div className="category-score">
                            Category Score: {categoryScore}
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