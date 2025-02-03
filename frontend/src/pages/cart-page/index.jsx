import React from 'react';
import Cart from '../../components/cart';
import './cart-page.styles.scss';
import SEO from '../../components/seo';

const CartPage = () => {
    return (
        <>
            <SEO 
                title="Shopping Cart | Your Beauty Products"
                description="Review your shopping cart of premium beauty products. Secure checkout with Amazon protection and fast Prime shipping."
            />
            <div className="cart-page">
                <Cart />
            </div>
        </>
    );
};

export default CartPage; 