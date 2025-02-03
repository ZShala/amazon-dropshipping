import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import visaLogo from '../../assets/visa-logo.webp';
import mastercardLogo from '../../assets/mastercard-logo.png';
import paypalLogo from '../../assets/paypal-logo.png';
import './cart.styles.scss';

const Cart = () => {
    const [cartItems, setCartItems] = useState([]);
    const [subtotal, setSubtotal] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadCart();
    }, []);

    const loadCart = () => {
        try {
            const items = JSON.parse(localStorage.getItem('cart') || '[]');
            setCartItems(items);
            calculateTotals(items);
            setLoading(false);
        } catch (error) {
            console.error('Error loading cart:', error);
            setLoading(false);
        }
    };

    const calculateTotals = (items) => {
        const total = items.reduce((sum, item) => {
            const price = item.price || 29.99;
            return sum + (price * item.quantity);
        }, 0);
        setSubtotal(total);
    };

    const updateQuantity = (productId, newQuantity) => {
        if (newQuantity < 1) return;
        
        const updatedItems = cartItems.map(item => {
            if (item.ProductId === productId) {
                return { ...item, quantity: newQuantity };
            }
            return item;
        });
        
        setCartItems(updatedItems);
        localStorage.setItem('cart', JSON.stringify(updatedItems));
        calculateTotals(updatedItems);
    };

    const removeItem = (productId) => {
        const updatedItems = cartItems.filter(item => item.ProductId !== productId);
        setCartItems(updatedItems);
        localStorage.setItem('cart', JSON.stringify(updatedItems));
        calculateTotals(updatedItems);
    };

    const getProductImage = (productType) => {
        const productType_lower = productType.toLowerCase();
        
        if (productType_lower.includes('lipstick') || productType_lower.includes('lip')) {
            return "https://m.media-amazon.com/images/I/61bwqXwdPWL._SX522_.jpg";
        }
        if (productType_lower.includes('mascara') || productType_lower.includes('eye')) {
            return "https://m.media-amazon.com/images/I/71yM0xUAetL._SX522_.jpg";
        }
        if (productType_lower.includes('foundation') || productType_lower.includes('concealer')) {
            return "https://m.media-amazon.com/images/I/71Pp8KFNKBL._SX522_.jpg";
        }
        if (productType_lower.includes('cream') || productType_lower.includes('moisturizer')) {
            return "https://m.media-amazon.com/images/I/71J5c8yR90L._SX522_.jpg";
        }
        if (productType_lower.includes('serum') || productType_lower.includes('oil')) {
            return "https://m.media-amazon.com/images/I/61VYQRUjwwL._SX522_.jpg";
        }
        if (productType_lower.includes('shampoo') || productType_lower.includes('hair')) {
            return "https://m.media-amazon.com/images/I/71qlR7nICdL._SX522_.jpg";
        }
        if (productType_lower.includes('perfume') || productType_lower.includes('fragrance')) {
            return "https://m.media-amazon.com/images/I/61MYnlrmHyL._SX522_.jpg";
        }
        // Default image if no match
        return "https://m.media-amazon.com/images/I/61w-ZYmf6WL._SX522_.jpg";
    };

    if (loading) {
        return <div className="cart-loading">Loading cart...</div>;
    }

    return (
        <div className="cart-container">
            <div className="cart-header">
                <h1>Your Shopping Cart</h1>
                <div className="amazon-badges">
                    <div className="amazon-prime">
                        <i className="fab fa-amazon"></i>
                        Prime Shipping
                    </div>
                    <div className="delivery-time">
                        <i className="fas fa-truck"></i>
                        2-5 Day Delivery
                    </div>
                </div>
            </div>

            <div className="cart-content">
                <div className="cart-main">
                    {cartItems.length === 0 ? (
                        <div className="empty-cart">
                            <div className="empty-icon">🛒</div>
                            <h2>Your cart is empty</h2>
                            <p>Browse our AI-recommended Amazon products</p>
                            <Link to="/" className="continue-shopping">
                                Continue Shopping
                            </Link>
                        </div>
                    ) : (
                        <div className="cart-items">
                            {cartItems.map(item => (
                                <div key={item.ProductId} className="cart-item">
                                    <div className="item-image">
                                        <img 
                                            src={getProductImage(item.ProductType)} 
                                            alt={item.ProductType} 
                                        />
                                        <div className="amazon-tag">Amazon Product</div>
                                    </div>
                                    
                                    <div className="item-details">
                                        <h3>{item.ProductType}</h3>
                                        <div className="item-meta">
                                            <div className="rating">
                                                <span className="stars">★</span> 
                                                <span>{item.Rating}</span>
                                                <span className="reviews">({item.ReviewCount} reviews)</span>
                                            </div>
                                            <div className="shipping-info">
                                                <i className="fas fa-check"></i>
                                                In Stock & Ready to Ship
                                            </div>
                                        </div>
                                        <div className="amazon-prime-info">
                                            <i className="fab fa-amazon"></i>
                                            Prime Delivery Available
                                        </div>
                                    </div>

                                    <div className="item-actions">
                                        <div className="price-info">
                                            <span className="price">${(item.price || 29.99).toFixed(2)}</span>
                                            <span className="shipping">Free Prime Shipping</span>
                                        </div>
                                        
                                        <div className="quantity-controls">
                                            <button 
                                                onClick={() => updateQuantity(item.ProductId, item.quantity - 1)}
                                                disabled={item.quantity <= 1}
                                            >
                                                −
                                            </button>
                                            <span>{item.quantity}</span>
                                            <button 
                                                onClick={() => updateQuantity(item.ProductId, item.quantity + 1)}
                                            >
                                                +
                                            </button>
                                        </div>
                                        
                                        <div className="item-total">
                                            <span>Subtotal:</span>
                                            <span>${((item.price || 29.99) * item.quantity).toFixed(2)}</span>
                                        </div>
                                        
                                        <button 
                                            className="remove-btn"
                                            onClick={() => removeItem(item.ProductId)}
                                        >
                                            <i className="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {cartItems.length > 0 && (
                    <div className="cart-sidebar">
                        <div className="order-summary">
                            <h2>Order Summary</h2>
                            
                            <div className="summary-rows">
                                <div className="summary-row">
                                    <span>Items ({cartItems.length}):</span>
                                    <span>${subtotal.toFixed(2)}</span>
                                </div>
                                <div className="summary-row">
                                    <span>Prime Shipping:</span>
                                    <span className="free">FREE</span>
                                </div>
                                <div className="summary-row">
                                    <span>Estimated Tax:</span>
                                    <span>${(subtotal * 0.15).toFixed(2)}</span>
                                </div>
                            </div>

                            <div className="total-row">
                                <span>Order Total:</span>
                                <span>${(subtotal + (subtotal * 0.15)).toFixed(2)}</span>
                            </div>

                            <button className="checkout-btn">
                                <i className="fas fa-lock"></i>
                                Proceed to Checkout
                            </button>

                            <div className="dropship-info">
                                <div className="info-item">
                                    <i className="fab fa-amazon"></i>
                                    <div>
                                        <h4>Amazon Direct</h4>
                                        <p>Ships directly from Amazon</p>
                                    </div>
                                </div>
                                <div className="info-item">
                                    <i className="fas fa-shield-alt"></i>
                                    <div>
                                        <h4>Secure Shopping</h4>
                                        <p>Protected by Amazon</p>
                                    </div>
                                </div>
                                <div className="info-item">
                                    <i className="fas fa-undo"></i>
                                    <div>
                                        <h4>Easy Returns</h4>
                                        <p>30-day return policy</p>
                                    </div>
                                </div>
                            </div>

                            <div className="payment-methods">
                                <p>We Accept:</p>
                                <div className="methods">
                                    <img src={visaLogo} alt="Visa" />
                                    <img src={mastercardLogo} alt="Mastercard" />
                                    <img src={paypalLogo} alt="PayPal" />
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Cart; 