import React from 'react';
import './shipping.styles.scss';
import SEO from '../../components/seo';
import { FaTruck, FaClock, FaGlobe, FaShieldAlt } from 'react-icons/fa';

const Shipping = () => {
    return (
        <div className="shipping-page">
            <SEO 
                title="Shipping Information | Your Beauty Products"
                description="Learn about our shipping methods, delivery times, and costs."
            />
            
            <div className="shipping-container">
                <h1>Shipping Information</h1>
                <div className="last-updated">Last Updated: March 15, 2024</div>

                <div className="shipping-highlights">
                    <div className="highlight-card">
                        <FaTruck />
                        <h3>Free Prime Shipping</h3>
                        <p>On orders over $25</p>
                    </div>
                    <div className="highlight-card">
                        <FaClock />
                        <h3>Fast Delivery</h3>
                        <p>2-5 business days</p>
                    </div>
                    <div className="highlight-card">
                        <FaGlobe />
                        <h3>International</h3>
                        <p>Shipping worldwide</p>
                    </div>
                    <div className="highlight-card">
                        <FaShieldAlt />
                        <h3>Order Protection</h3>
                        <p>Full tracking available</p>
                    </div>
                </div>

                <section className="shipping-section">
                    <h2>Domestic Shipping</h2>
                    <div className="shipping-options">
                        <div className="option">
                            <h3>Prime Shipping</h3>
                            <ul>
                                <li>Free on orders over $25</li>
                                <li>2-5 business days delivery</li>
                                <li>Full tracking included</li>
                                <li>Available throughout US</li>
                            </ul>
                        </div>
                        <div className="option">
                            <h3>Standard Shipping</h3>
                            <ul>
                                <li>$4.99 flat rate</li>
                                <li>5-7 business days</li>
                                <li>Tracking included</li>
                                <li>Available for all orders</li>
                            </ul>
                        </div>
                        <div className="option">
                            <h3>Express Shipping</h3>
                            <ul>
                                <li>$9.99 flat rate</li>
                                <li>1-2 business days</li>
                                <li>Priority handling</li>
                                <li>Guaranteed delivery</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <section className="shipping-section">
                    <h2>International Shipping</h2>
                    <p>We ship to most countries worldwide through our global shipping network.</p>
                    <div className="international-info">
                        <div className="info-block">
                            <h3>Delivery Times</h3>
                            <ul>
                                <li>Europe: 7-14 business days</li>
                                <li>Asia: 10-15 business days</li>
                                <li>Australia: 10-15 business days</li>
                                <li>Other regions: 14-21 business days</li>
                            </ul>
                        </div>
                        <div className="info-block">
                            <h3>Shipping Costs</h3>
                            <ul>
                                <li>Europe: Starting from $14.99</li>
                                <li>Asia: Starting from $16.99</li>
                                <li>Australia: Starting from $19.99</li>
                                <li>Other regions: Starting from $24.99</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <section className="shipping-section">
                    <h2>Important Information</h2>
                    <ul>
                        <li>Orders are processed within 24 hours</li>
                        <li>Tracking number provided via email</li>
                        <li>Signature may be required for delivery</li>
                        <li>No deliveries on weekends and holidays</li>
                        <li>Additional fees may apply for remote areas</li>
                        <li>Import duties and taxes not included</li>
                    </ul>
                </section>

                <div className="contact-support">
                    <h2>Shipping Support</h2>
                    <p>Need help tracking your order or have shipping questions?</p>
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

export default Shipping; 