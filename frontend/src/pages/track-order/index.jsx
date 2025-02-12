import React, { useState } from 'react';
import './track-order.styles.scss';
import SEO from '../../components/seo';
import { FaSearch, FaBox, FaTruck, FaCheckCircle, FaMapMarkerAlt } from 'react-icons/fa';

const TrackOrder = () => {
    const [orderNumber, setOrderNumber] = useState('');
    const [email, setEmail] = useState('');
    const [showDemo, setShowDemo] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setShowDemo(true);
    };

    return (
        <div className="track-order-page">
            <SEO 
                title="Track Your Order | Your Beauty Products"
                description="Track your order status and shipping information."
            />
            
            <div className="track-order-container">
                <h1>Track Your Order</h1>
                <p className="subtitle">Enter your order details below</p>

                <div className="track-form-container">
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label>Order Number</label>
                            <input
                                type="text"
                                placeholder="Enter your order number"
                                value={orderNumber}
                                onChange={(e) => setOrderNumber(e.target.value)}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Email Address</label>
                            <input
                                type="email"
                                placeholder="Enter your email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <button type="submit" className="track-button">
                            <FaSearch /> Track Order
                        </button>
                    </form>
                </div>

                {showDemo && (
                    <div className="order-status">
                        <div className="order-info">
                            <h2>Order #12345678</h2>
                            <p className="estimated-delivery">
                                Estimated Delivery: March 20, 2024
                            </p>
                        </div>

                        <div className="tracking-timeline">
                            <div className="timeline-item completed">
                                <div className="timeline-icon">
                                    <FaBox />
                                </div>
                                <div className="timeline-content">
                                    <h3>Order Confirmed</h3>
                                    <p>March 15, 2024 - 9:30 AM</p>
                                    <span className="status">Completed</span>
                                </div>
                            </div>

                            <div className="timeline-item completed">
                                <div className="timeline-icon">
                                    <FaCheckCircle />
                                </div>
                                <div className="timeline-content">
                                    <h3>Order Processed</h3>
                                    <p>March 15, 2024 - 2:45 PM</p>
                                    <span className="status">Completed</span>
                                </div>
                            </div>

                            <div className="timeline-item active">
                                <div className="timeline-icon">
                                    <FaTruck />
                                </div>
                                <div className="timeline-content">
                                    <h3>In Transit</h3>
                                    <p>March 16, 2024 - 10:15 AM</p>
                                    <span className="status">In Progress</span>
                                </div>
                            </div>

                            <div className="timeline-item">
                                <div className="timeline-icon">
                                    <FaMapMarkerAlt />
                                </div>
                                <div className="timeline-content">
                                    <h3>Out for Delivery</h3>
                                    <p>Expected: March 20, 2024</p>
                                    <span className="status">Pending</span>
                                </div>
                            </div>
                        </div>

                        <div className="shipping-details">
                            <h3>Shipping Details</h3>
                            <div className="details-grid">
                                <div className="detail-item">
                                    <span className="label">Carrier:</span>
                                    <span className="value">Amazon Logistics</span>
                                </div>
                                <div className="detail-item">
                                    <span className="label">Tracking Number:</span>
                                    <span className="value">AMZ123456789</span>
                                </div>
                                <div className="detail-item">
                                    <span className="label">Service:</span>
                                    <span className="value">Prime Shipping</span>
                                </div>
                                <div className="detail-item">
                                    <span className="label">Status:</span>
                                    <span className="value status-in-transit">In Transit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                <div className="tracking-help">
                    <h2>Need Help?</h2>
                    <p>If you need assistance tracking your order, please contact our customer service:</p>
                    <div className="contact-methods">
                        <div className="contact-method">
                            <i className="fas fa-envelope"></i>
                            <p>Email: support@yourbeauty.com</p>
                        </div>
                        <div className="contact-method">
                            <i className="fas fa-phone"></i>
                            <p>Phone: 1-800-BEAUTY</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TrackOrder; 