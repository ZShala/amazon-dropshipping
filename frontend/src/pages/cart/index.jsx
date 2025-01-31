import React, { useState, useEffect } from 'react';
import ProductRecommendations from '../../components/product-recommendation';
import './cart.styles.scss';

const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    const [crossSellProducts, setCrossSellProducts] = useState([]);
    const [upSellProducts, setUpSellProducts] = useState([]);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                // Merr rekomandimet për cross-selling bazuar në items në cart
                const productIds = cartItems.map(item => item.productId).join(',');
                const response = await fetch(`/api/recommendations/cart?products=${productIds}`);
                const data = await response.json();
                
                // Ndaj rekomandimet në cross-sell dhe up-sell
                setCrossSellProducts(data.crossSell); // Produkte komplementare
                setUpSellProducts(data.upSell);     // Produkte më të shtrenjta/premium
            } catch (error) {
                console.error('Error:', error);
            }
        };

        if (cartItems.length > 0) {
            fetchRecommendations();
        }
    }, [cartItems]);

    return (
        <div className="cart-page">
            {/* Cart Summary */}
            <div className="cart-summary">
                <h2>Your Cart ({cartItems.length} items)</h2>
                <div className="cart-items">
                    {cartItems.map(item => (
                        <CartItem key={item.id} item={item} />
                    ))}
                </div>
                <div className="cart-total">
                    <h3>Total: ${calculateTotal()}</h3>
                    <button className="checkout-button">Proceed to Checkout</button>
                </div>
            </div>

            {/* Up-sell Section - Produkte më premium */}
            {upSellProducts.length > 0 && (
                <div className="upsell-section">
                    <h3>Upgrade Your Selection</h3>
                    <div className="products-grid">
                        {upSellProducts.map(product => (
                            <ProductCard 
                                key={product.id}
                                product={product}
                                comparisonFeatures={product.advantagesOverCart}
                                priceComparison={product.priceDifference}
                            />
                        ))}
                    </div>
                </div>
            )}

            {/* Cross-sell Section - Produkte komplementare */}
            {crossSellProducts.length > 0 && (
                <div className="cross-sell-section">
                    <h3>Frequently Bought Together</h3>
                    <div className="bundle-offers">
                        {crossSellProducts.map(product => (
                            <div key={product.id} className="bundle-card">
                                <ProductCard 
                                    product={product}
                                    bundleDiscount={product.bundleDiscount}
                                    complementaryReason={product.complementaryReason}
                                />
                                <button className="add-bundle">
                                    Add to Cart (Save {product.bundleDiscount}%)
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Emergency Offers - Për të parandaluar braktisjen e cart */}
            <div className="emergency-offers">
                <h4>Special Offers Ending Soon</h4>
                <div className="time-limited-deals">
                    {/* Oferta me kohë të limituar */}
                </div>
            </div>
        </div>
    );
}; 