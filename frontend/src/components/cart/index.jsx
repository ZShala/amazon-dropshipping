import React, { useState, useEffect } from 'react';
import './cart.styles.scss';

const Cart = () => {
    const [cartItems, setCartItems] = useState([]);
    const [total, setTotal] = useState(0);

    useEffect(() => {
        // Ngarko produktet nga localStorage
        const loadCart = () => {
            try {
                const cart = JSON.parse(localStorage.getItem('cart') || '[]');
                setCartItems(cart);
                
                // Llogarit totalin
                const cartTotal = cart.reduce((sum, item) => 
                    sum + (item.price || 0) * item.quantity, 0);
                setTotal(cartTotal);
            } catch (error) {
                console.error('Error loading cart:', error);
                setCartItems([]);
            }
        };

        loadCart();
        window.addEventListener('storage', loadCart);
        
        return () => window.removeEventListener('storage', loadCart);
    }, []);

    const updateQuantity = (productId, newQuantity) => {
        const updatedCart = cartItems.map(item => {
            if (item.ProductId === productId) {
                return { ...item, quantity: Math.max(0, newQuantity) };
            }
            return item;
        }).filter(item => item.quantity > 0);

        setCartItems(updatedCart);
        localStorage.setItem('cart', JSON.stringify(updatedCart));
    };

    const removeItem = (productId) => {
        const updatedCart = cartItems.filter(item => item.ProductId !== productId);
        setCartItems(updatedCart);
        localStorage.setItem('cart', JSON.stringify(updatedCart));
    };

    if (!Array.isArray(cartItems)) {
        return (
            <div className="cart-empty">
                <h2>Your cart is empty</h2>
                <p>Add some products to your cart</p>
            </div>
        );
    }

    return (
        <div className="cart">
            <h2>Your Cart</h2>
            <div className="cart-items">
                {cartItems.map(item => (
                    <div key={item.ProductId} className="cart-item">
                        <img 
                            src={item.ImageURL} 
                            alt={item.ProductType} 
                            className="item-image"
                        />
                        <div className="item-details">
                            <h3>{item.ProductType}</h3>
                            <div className="quantity-controls">
                                <button 
                                    onClick={() => updateQuantity(item.ProductId, item.quantity - 1)}
                                >
                                    -
                                </button>
                                <span>{item.quantity}</span>
                                <button 
                                    onClick={() => updateQuantity(item.ProductId, item.quantity + 1)}
                                >
                                    +
                                </button>
                            </div>
                        </div>
                        <button 
                            className="remove-btn"
                            onClick={() => removeItem(item.ProductId)}
                        >
                            Remove
                        </button>
                    </div>
                ))}
            </div>
            <div className="cart-summary">
                <div className="total">
                    Total Items: {cartItems.reduce((sum, item) => sum + item.quantity, 0)}
                </div>
            </div>
        </div>
    );
};

export default Cart; 