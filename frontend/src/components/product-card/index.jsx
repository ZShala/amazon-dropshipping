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
    
    // Lista e formateve të ndryshme të imazheve
    const getImageFormats = (asin) => [
        product.ImageURL, // Vendos URL-në kryesore të parën
        `https://m.media-amazon.com/images/I/${asin}._AC_SX466_.jpg`,
        `https://m.media-amazon.com/images/I/${asin}._AC_SL1500_.jpg`,
        `https://m.media-amazon.com/images/I/${asin}._AC_SX425_.jpg`,
        `https://m.media-amazon.com/images/I/${asin}._AC_SX522_.jpg`,
        `https://m.media-amazon.com/images/I/${asin}.jpg`,
        "https://via.placeholder.com/300x300?text=No+Image"
    ];

    const handleImageError = () => {
        console.log('Image error for:', product.ImageURL); // Shto logging
        const imageFormats = getImageFormats(product.ASIN);
        if (currentImageIndex < imageFormats.length - 1) {
            console.log('Trying next format:', imageFormats[currentImageIndex + 1]);
            setCurrentImageIndex(currentImageIndex + 1);
        } else {
            console.log('All formats failed, using placeholder');
            setImageError(true);
        }
    };

    const imageFormats = getImageFormats(product.ASIN);
    const currentImageUrl = !imageError ? imageFormats[currentImageIndex] : imageFormats[imageFormats.length - 1];

    console.log('Current image URL:', currentImageUrl); // Shto logging

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
                            src={currentImageUrl}
                            alt={product.ProductType}
                            className="product-image"
                            onError={handleImageError}
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