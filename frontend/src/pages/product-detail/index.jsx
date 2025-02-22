import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import Toast from '../../components/toast';
import './product-detail.styles.scss';
import { useCart } from '../../contexts/cart.context';
import RecommendedProducts from '../../components/recommended-products';

const ProductDetail = () => {
    const { productId } = useParams();
    const location = useLocation();
    const imageUrl = location.state?.imageUrl;
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedImage, setSelectedImage] = useState(0);
    const [showToast, setShowToast] = useState(false);
    const [selectedQuantity, setSelectedQuantity] = useState(1);
    const [deliveryDate, setDeliveryDate] = useState('');
    const { addToCart } = useCart();
    const navigate = useNavigate();

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

        const calculateDeliveryDate = () => {
            const date = new Date();
            date.setDate(date.getDate() + 5);
            setDeliveryDate(date.toLocaleDateString('en-US', { 
                weekday: 'long', 
                month: 'long', 
                day: 'numeric' 
            }));
        };

        if (productId) {
            fetchProductDetails();
            calculateDeliveryDate();
        }
    }, [productId]);

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const handleAddToCart = () => {
        if (!product) return;

        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const existingProduct = cart.find(item => item.ProductId === product.ProductId);
        
        const currentImage = imageUrl || images[selectedImage];
        
        if (existingProduct) {
            existingProduct.quantity += selectedQuantity;
        } else {
            cart.push({
                ...product,
                quantity: selectedQuantity,
                ImageURL: currentImage
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        window.dispatchEvent(new Event('cartUpdated'));
        setShowToast(true);
        
        setTimeout(() => {
            setShowToast(false);
        }, 3000);
    };

    const handleBuyNow = () => {
        addToCart({
            ProductId: product.ProductId,
            ProductType: product.ProductType,
            Price: product.Price,
            ImageURL: imageUrl || images[selectedImage],
            quantity: selectedQuantity
        });
        navigate('/cart');
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
        <div className="product-detail-page">
            <div className="product-detail-container">
                <div className="product-main">
                    <div className="product-image-section">
                        <div className="main-image">
                            <img 
                                src={imageUrl || images[selectedImage]} 
                                alt={product.ProductType}
                                onError={(e) => {
                                    if (selectedImage < images.length - 1) {
                                        setSelectedImage(selectedImage + 1);
                                    }
                                }}
                            />
                            <div className="amazon-badge">
                                <i className="fab fa-amazon"></i>
                                Amazon's Choice
                            </div>
                            <div className="prime-badge">
                                <i className="fab fa-amazon"></i>
                                Prime
                            </div>
                        </div>
                        <div className="product-badges">
                            <div className="badge authentic">
                                <i className="fas fa-check-circle"></i>
                                100% Authentic
                            </div>
                            <div className="badge returns">
                                <i className="fas fa-undo"></i>
                                Easy Returns
                            </div>
                            <div className="badge shipping">
                                <i className="fas fa-truck"></i>
                                Prime Shipping
                            </div>
                        </div>
                    </div>

                    <div className="product-info">
                        <div className="product-header">
                            <h1>{product.ProductType}</h1>
                            <div className="product-meta">
                                <div className="rating">
                                    <div className="stars">
                                        {'★'.repeat(Math.round(product.Rating))}
                                        {'☆'.repeat(5 - Math.round(product.Rating))}
                                    </div>
                                    <span className="rating-count">
                                        {product.Rating} ({product.ReviewCount} verified reviews)
                                    </span>
                                </div>
                                <div className="stock-status">
                                    <i className="fas fa-check-circle"></i>
                                    In Stock
                                </div>
                            </div>
                        </div>

                        <div className="price-section">
                            <div className="price-box">
                                <div className="current-price">
                                    <span className="currency">$</span>
                                    <span className="amount">{(product.price || 29.99).toFixed(2)}</span>
                                </div>
                                <div className="original-price">
                                    ${((product.price || 29.99) * 1.2).toFixed(2)}
                                </div>
                                <div className="discount">
                                    Save 20%
                                </div>
                            </div>
                            <div className="prime-delivery">
                                <i className="fab fa-amazon"></i>
                                FREE Prime Delivery
                            </div>
                        </div>

                        <div className="delivery-info">
                            <div className="delivery-date">
                                <i className="fas fa-truck-fast"></i>
                                <div>
                                    <span className="label">Delivery:</span>
                                    <span className="date">{deliveryDate}</span>
                                </div>
                            </div>
                            <div className="delivery-options">
                                <div className="option">
                                    <i className="fas fa-box"></i>
                                    Ships from Amazon
                                </div>
                                <div className="option">
                                    <i className="fas fa-map-marker-alt"></i>
                                    Delivers to your location
                                </div>
                            </div>
                        </div>

                        <div className="purchase-section">
                            <div className="quantity-selector">
                                <label>Quantity:</label>
                                <select 
                                    value={selectedQuantity} 
                                    onChange={(e) => setSelectedQuantity(Number(e.target.value))}
                                >
                                    {[1,2,3,4,5,6,7,8,9,10].map(num => (
                                        <option key={num} value={num}>{num}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="action-buttons">
                                <button className="add-to-cart" onClick={handleAddToCart}>
                                    <i className="fas fa-shopping-cart"></i>
                                    Add to Cart
                                </button>
                                <button className="buy-now" onClick={handleBuyNow}>
                                    <i className="fas fa-bolt"></i>
                                    Buy Now
                                </button>
                            </div>
                        </div>

                        <div className="product-features">
                            <h3>Product Features</h3>
                            <ul>
                                <li>
                                    <i className="fas fa-check"></i>
                                    Premium Quality Product
                                </li>
                                <li>
                                    <i className="fas fa-check"></i>
                                    Authentic Amazon Item
                                </li>
                                <li>
                                    <i className="fas fa-check"></i>
                                    Fast Prime Shipping
                                </li>
                                <li>
                                    <i className="fas fa-check"></i>
                                    30-Day Returns
                                </li>
                            </ul>
                        </div>

                        <div className="trust-badges">
                            <div className="badge">
                                <i className="fas fa-shield-alt"></i>
                                <div>
                                    <h4>Secure Payment</h4>
                                    <p>Your data is protected</p>
                                </div>
                            </div>
                            <div className="badge">
                                <i className="fas fa-truck"></i>
                                <div>
                                    <h4>Fast Delivery</h4>
                                    <p>2-5 day shipping</p>
                                </div>
                            </div>
                            <div className="badge">
                                <i className="fas fa-box-open"></i>
                                <div>
                                    <h4>Amazon Fulfilled</h4>
                                    <p>Direct from warehouse</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <RecommendedProducts currentProductId={productId} />
            
            <Toast 
                message="Product added to cart!"
                isVisible={showToast}
                onClose={() => setShowToast(false)}
            />
        </div>
    );
};

export default ProductDetail; 