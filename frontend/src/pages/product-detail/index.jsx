import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Toast from '../../components/toast';
import './product-detail.styles.scss';

const ProductDetail = () => {
    const { productId } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedImage, setSelectedImage] = useState(0);
    const [showToast, setShowToast] = useState(false);

    useEffect(() => {
        const fetchProductDetails = async () => {
            try {
                setLoading(true);
                const response = await fetch(`http://localhost:5001/api/products/details/${productId}`);
                
                if (!response.ok) {
                    throw new Error('Failed to fetch product details');
                }
                
                const data = await response.json();
                
                if (data && data.product) {
                    setProduct(data.product);
                } else {
                    throw new Error('Product not found');
                }
            } catch (err) {
                console.error('Error fetching product:', err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        if (productId) {
            fetchProductDetails();
        }
    }, [productId]);

    const handleAddToCart = () => {
        if (!product) return;

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
        window.dispatchEvent(new Event('cartUpdated'));
        setShowToast(true);
        
        setTimeout(() => {
            setShowToast(false);
        }, 3000);
    };

    if (loading) {
        return (
            <div className="product-detail-loading">
                <div className="loading-spinner"></div>
                <p>Loading product details...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="product-detail-error">
                <h2>Error Loading Product</h2>
                <p>{error}</p>
                <button onClick={() => window.location.reload()}>
                    Try Again
                </button>
            </div>
        );
    }

    if (!product) {
        return (
            <div className="product-detail-not-found">
                <h2>Product Not Found</h2>
                <p>The product you're looking for doesn't exist.</p>
            </div>
        );
    }

    const getImageFormats = (asin) => [
        product.ImageURL,
        `https://m.media-amazon.com/images/I/${asin}._AC_SX466_.jpg`,
        `https://m.media-amazon.com/images/I/${asin}._AC_SL1500_.jpg`,
        `https://m.media-amazon.com/images/I/${asin}._AC_SX425_.jpg`,
        `https://m.media-amazon.com/images/I/${asin}._AC_SX522_.jpg`,
        `https://m.media-amazon.com/images/I/${asin}.jpg`
    ];

    const images = getImageFormats(product.ASIN);

    return (
        <>
            <div className="product-detail">
                <div className="product-images">
                    <div className="main-image">
                        <img 
                            src={images[selectedImage]} 
                            alt={product.ProductType}
                            onError={(e) => {
                                if (selectedImage < images.length - 1) {
                                    setSelectedImage(selectedImage + 1);
                                }
                            }}
                        />
                    </div>
                    <div className="image-thumbnails">
                        {images.map((img, index) => (
                            <img 
                                key={index}
                                src={img}
                                alt={`${product.ProductType} view ${index + 1}`}
                                className={selectedImage === index ? 'active' : ''}
                                onClick={() => setSelectedImage(index)}
                                onError={(e) => e.target.style.display = 'none'}
                            />
                        ))}
                    </div>
                </div>

                <div className="product-info">
                    <h1>{product.ProductType}</h1>
                    
                    <div className="rating">
                        <span className="stars">{'★'.repeat(Math.round(product.Rating))}</span>
                        <span className="rating-value">{product.Rating}</span>
                        {product.ReviewCount && (
                            <span className="review-count">({product.ReviewCount} reviews)</span>
                        )}
                    </div>

                    <div className="product-actions">
                        <button 
                            className="add-to-cart"
                            onClick={handleAddToCart}
                        >
                            Add to Cart
                        </button>
                    </div>

                    <div className="product-description">
                        <h2>Product Description</h2>
                        <p>{product.Description || 'No description available.'}</p>
                    </div>
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

export default ProductDetail; 