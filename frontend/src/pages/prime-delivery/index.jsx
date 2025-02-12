import React from 'react';
import './prime-delivery.styles.scss';
import SEO from '../../components/seo';
import { FaTruck, FaClock, FaMapMarkedAlt, FaBox, FaShieldAlt } from 'react-icons/fa';

const PrimeDelivery = () => {
    return (
        <div className="prime-delivery-page">
            <SEO 
                title="Prime Delivery 2-5 Days | Your Beauty Products"
                description="Learn about our fast Prime delivery service and shipping benefits."
            />
            
            <div className="prime-delivery-container">
                <div className="hero-section">
                    <FaTruck className="prime-icon" />
                    <h1>Prime Delivery</h1>
                    <p>Fast, Free Shipping on Orders Over $25</p>
                    <div className="delivery-time">2-5 Business Days</div>
                </div>

                <div className="features-grid">
                    <div className="feature-card">
                        <FaClock />
                        <h3>Fast Processing</h3>
                        <p>Orders processed within 24 hours</p>
                    </div>
                    <div className="feature-card">
                        <FaMapMarkedAlt />
                        <h3>Wide Coverage</h3>
                        <p>Available throughout the US</p>
                    </div>
                    <div className="feature-card">
                        <FaBox />
                        <h3>Free Shipping</h3>
                        <p>On orders over $25</p>
                    </div>
                    <div className="feature-card">
                        <FaShieldAlt />
                        <h3>Full Protection</h3>
                        <p>Package insurance included</p>
                    </div>
                </div>

                <section className="delivery-info-section">
                    <h2>Prime Delivery Benefits</h2>
                    <div className="benefits-grid">
                        <div className="benefit">
                            <h3>Fast & Reliable</h3>
                            <ul>
                                <li>2-5 business days delivery</li>
                                <li>Real-time tracking</li>
                                <li>Weekend delivery available</li>
                                <li>Delivery notifications</li>
                            </ul>
                        </div>
                        <div className="benefit">
                            <h3>Shipping Coverage</h3>
                            <ul>
                                <li>All 50 US states</li>
                                <li>US territories</li>
                                <li>APO/FPO addresses</li>
                                <li>PO boxes</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <section className="delivery-timeline">
                    <h2>Delivery Process</h2>
                    <div className="timeline">
                        <div className="timeline-item">
                            <div className="timeline-icon">
                                <FaBox />
                            </div>
                            <div className="timeline-content">
                                <h4>Order Placed</h4>
                                <p>Order confirmed and payment processed</p>
                            </div>
                        </div>
                        <div className="timeline-item">
                            <div className="timeline-icon">
                                <i className="fas fa-warehouse"></i>
                            </div>
                            <div className="timeline-content">
                                <h4>Processing</h4>
                                <p>Order picked and packed at Amazon warehouse</p>
                            </div>
                        </div>
                        <div className="timeline-item">
                            <div className="timeline-icon">
                                <FaTruck />
                            </div>
                            <div className="timeline-content">
                                <h4>In Transit</h4>
                                <p>Package on its way to delivery address</p>
                            </div>
                        </div>
                        <div className="timeline-item">
                            <div className="timeline-icon">
                                <i className="fas fa-home"></i>
                            </div>
                            <div className="timeline-content">
                                <h4>Delivered</h4>
                                <p>Package safely delivered to your door</p>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="shipping-rates">
                    <h2>Shipping Rates</h2>
                    <div className="rates-grid">
                        <div className="rate-card">
                            <div className="rate-header">
                                <h3>Prime Shipping</h3>
                                <div className="price">FREE</div>
                            </div>
                            <ul>
                                <li>Orders over $25</li>
                                <li>2-5 business days</li>
                                <li>Full tracking</li>
                                <li>Insurance included</li>
                            </ul>
                        </div>
                        <div className="rate-card">
                            <div className="rate-header">
                                <h3>Standard Shipping</h3>
                                <div className="price">$4.99</div>
                            </div>
                            <ul>
                                <li>Orders under $25</li>
                                <li>5-7 business days</li>
                                <li>Basic tracking</li>
                                <li>Basic insurance</li>
                            </ul>
                        </div>
                        <div className="rate-card">
                            <div className="rate-header">
                                <h3>Express Shipping</h3>
                                <div className="price">$9.99</div>
                            </div>
                            <ul>
                                <li>Any order value</li>
                                <li>1-2 business days</li>
                                <li>Priority tracking</li>
                                <li>Premium insurance</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <div className="delivery-support">
                    <h2>Need Help with Delivery?</h2>
                    <p>Our shipping specialists are here to assist you</p>
                    <div className="contact-methods">
                        <div className="contact-method">
                            <i className="fas fa-envelope"></i>
                            <p>Email: shipping@glowaura.com</p>
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

export default PrimeDelivery; 