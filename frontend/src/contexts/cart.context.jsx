import React, { createContext, useState, useEffect } from 'react';

export const CartContext = createContext({
    cartItems: [],
    addToCart: () => {},
    removeFromCart: () => {},
    updateQuantity: () => {},
    clearCart: () => {},
    itemCount: 0,
    total: 0,
});

export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState([]);
    const [itemCount, setItemCount] = useState(0);
    const [total, setTotal] = useState(0);

    useEffect(() => {
        const savedCart = JSON.parse(localStorage.getItem('cart')) || [];
        setCartItems(savedCart);
    }, []);

    useEffect(() => {
        // Përditëso itemCount dhe total sa herë që ndryshon cart
        const count = cartItems.reduce((total, item) => total + item.quantity, 0);
        const newTotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        setItemCount(count);
        setTotal(newTotal);
        localStorage.setItem('cart', JSON.stringify(cartItems));
    }, [cartItems]);

    const addToCart = (product) => {
        setCartItems(prevItems => {
            const existingItem = prevItems.find(item => item.ProductId === product.ProductId);
            
            if (existingItem) {
                return prevItems.map(item => 
                    item.ProductId === product.ProductId
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            }
            
            return [...prevItems, { ...product, quantity: 1 }];
        });
    };

    const value = {
        cartItems,
        addToCart,
        removeFromCart: (productId) => {
            setCartItems(prevItems => 
                prevItems.filter(item => item.ProductId !== productId)
            );
        },
        updateQuantity: (productId, quantity) => {
            setCartItems(prevItems =>
                prevItems.map(item =>
                    item.ProductId === productId
                        ? { ...item, quantity: Math.max(0, quantity) }
                        : item
                )
            );
        },
        clearCart: () => {
            setCartItems([]);
            localStorage.removeItem('cart');
        },
        itemCount,
        total
    };

    return (
        <CartContext.Provider value={value}>
            {children}
        </CartContext.Provider>
    );
}; 