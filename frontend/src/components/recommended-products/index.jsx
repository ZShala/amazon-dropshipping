import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './recommended-products.styles.scss';

const LoadingState = () => (
    <div className="loading-state">
        <div className="loading-spinner"></div>
        <p>Loading recommendations...</p>
    </div>
);

const ErrorState = ({ message }) => (
    <div className="error-state">
        <p>{message}</p>
    </div>
);

const ProductCard = ({ product }) => (
    <Link 
        to={`/product/${product.ProductId}`}
        className="recommendation-card"
    >
        <div className="product-image-container">
            <img 
                src={product.ImageURL} 
                alt={product.ProductTitle || product.ProductType}
                onError={(e) => {
                    e.target.src = "http://localhost:5001/static/images/product-placeholder.jpg";
                }}
            />
            <div className="hover-overlay">
                <span>View Details</span>
            </div>
        </div>
        <div className="product-info">
            <h3>{product.ProductTitle || product.ProductType}</h3>
            <div className="rating-container">
                <div className="stars">
                    {[...Array(5)].map((_, index) => (
                        <span key={index} className={index < Math.round(product.Rating) ? 'star filled' : 'star'}>
                            ★
                        </span>
                    ))}
                </div>
                <span className="rating-text">{product.Rating.toFixed(1)}</span>
            </div>
            <div className="price">
                <span className="currency">€</span>
                <span className="amount">
                    {product.price ? product.price.toFixed(2) : '0.00'}
                </span>
            </div>
        </div>
    </Link>
);

const RecommendedProducts = ({ currentProductId }) => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchRecommendations = async () => {
            if (!currentProductId) return;
            
            setLoading(true);
            setError(null);
            
            try {
                console.log(`Fetching recommendations for product: ${currentProductId}`);
                
                const response = await fetch(
                    `http://localhost:5001/api/products/recommendations/${currentProductId}`
                );

                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Failed to fetch recommendations');
                }

                if (data.recommendations && data.recommendations.length > 0) {
                    console.log(`Received ${data.recommendations.length} recommendations`);
                    setRecommendations(data.recommendations);
                } else {
                    console.log('No recommendations available');
                    setRecommendations([]);
                    setError("No recommendations available for this product");
                }
            } catch (error) {
                console.error('Error fetching recommendations:', error);
                setError(error.message);
                setRecommendations([]);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, [currentProductId]);

    if (loading) return <LoadingState />;
    if (error) return <ErrorState message={error} />;
    if (!recommendations.length) return null;

    return (
        <section className="recommended-products">
            <div className="section-header">
                <h2>Recommended For You</h2>
                <p>Products similar to what you're viewing</p>
            </div>
            <div className="recommendations-grid">
                {recommendations.map((product) => (
                    <ProductCard 
                        key={product.ProductId} 
                        product={product} 
                    />
                ))}
            </div>
        </section>
    );
};

export default RecommendedProducts; 