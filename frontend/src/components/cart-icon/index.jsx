import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaShoppingCart } from 'react-icons/fa';
import './cart-icon.styles.scss';

const CartIcon = () => {
    const [itemCount, setItemCount] = useState(0);

    useEffect(() => {
        // Funksioni për të përditësuar numrin e produkteve
        const updateCartCount = () => {
            try {
                const cart = JSON.parse(localStorage.getItem('cart') || '[]');
                const count = cart.reduce((total, item) => total + (item.quantity || 0), 0);
                setItemCount(count);
            } catch (error) {
                console.error('Error updating cart count:', error);
                setItemCount(0);
            }
        };

        // Përditëso numrin fillestar
        updateCartCount();

        // Dëgjo për ndryshime në localStorage
        const handleStorageChange = (e) => {
            if (e.key === 'cart') {
                updateCartCount();
            }
        };

        window.addEventListener('storage', handleStorageChange);
        
        // Dëgjo për një event custom për përditësime lokale
        window.addEventListener('cartUpdated', updateCartCount);

        return () => {
            window.removeEventListener('storage', handleStorageChange);
            window.removeEventListener('cartUpdated', updateCartCount);
        };
    }, []);

    return (
        <Link to="/cart" className="cart-icon-container">
            <FaShoppingCart className="shopping-icon" />
            {itemCount > 0 && <span className="item-count">{itemCount}</span>}
        </Link>
    );
};

export default CartIcon; 