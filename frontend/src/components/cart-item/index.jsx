import React from 'react';
import './cart-item.styles.scss';

const CartItem = ({ item }) => {
    return (
        <div className="cart-item">
            <img src={item.URL} alt={item.ProductType} />
            <div className="item-details">
                <h3>{item.ProductType}</h3>
                <div className="rating">
                    <span>★</span> {item.Rating}
                </div>
                <div className="quantity-controls">
                    <button>-</button>
                    <span>{item.quantity}</span>
                    <button>+</button>
                </div>
            </div>
            <div className="price-section">
                <span className="price">${item.price}</span>
                <button className="remove-item">×</button>
            </div>
        </div>
    );
};

export default CartItem; 