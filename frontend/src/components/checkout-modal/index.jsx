import React, { useState } from 'react';
import './checkout-modal.styles.scss';

const CheckoutModal = ({ isOpen, onClose, total }) => {
    const [formData, setFormData] = useState({
        fullName: '',
        email: '',
        address: '',
        city: '',
        zipCode: '',
        cardNumber: '',
        expiryDate: '',
        cvv: ''
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Order submitted:', formData);
        onClose();
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    if (!isOpen) return null;

    return (
        <div className="checkout-modal-overlay">
            <div className="checkout-modal">
                <button className="close-button" onClick={onClose}>×</button>
                <h2>Checkout</h2>
                <div className="total-amount">
                    Total Amount: €{total.toFixed(2)}
                </div>
                <form onSubmit={handleSubmit}>
                    <div className="form-section">
                        <h3>Personal Information</h3>
                        <div className="form-group">
                            <input
                                type="text"
                                name="fullName"
                                placeholder="Full Name"
                                value={formData.fullName}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <input
                                type="email"
                                name="email"
                                placeholder="Email Address"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-section">
                        <h3>Shipping Address</h3>
                        <div className="form-group">
                            <input
                                type="text"
                                name="address"
                                placeholder="Street Address"
                                value={formData.address}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-row">
                            <input
                                type="text"
                                name="city"
                                placeholder="City"
                                value={formData.city}
                                onChange={handleChange}
                                required
                            />
                            <input
                                type="text"
                                name="zipCode"
                                placeholder="ZIP Code"
                                value={formData.zipCode}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-section">
                        <h3>Payment Details</h3>
                        <div className="form-group">
                            <input
                                type="text"
                                name="cardNumber"
                                placeholder="Card Number"
                                value={formData.cardNumber}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-row">
                            <input
                                type="text"
                                name="expiryDate"
                                placeholder="MM/YY"
                                value={formData.expiryDate}
                                onChange={handleChange}
                                required
                            />
                            <input
                                type="text"
                                name="cvv"
                                placeholder="CVV"
                                value={formData.cvv}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>

                    <button type="submit" className="submit-button">
                        Complete Purchase
                    </button>
                </form>
            </div>
        </div>
    );
};

export default CheckoutModal; 