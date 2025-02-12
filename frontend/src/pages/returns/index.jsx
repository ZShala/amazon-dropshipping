import React from 'react';
import './returns.styles.scss';
import SEO from '../../components/seo';
import { FaBox, FaTruck, FaMoneyBillWave, FaShieldAlt } from 'react-icons/fa';

const Returns = () => {
    return (
        <div className="returns-page">
            <SEO 
                title="Returns & Refunds | Your Beauty Products"
                description="Learn about our returns and refunds policy for beauty products."
            />
            
            <div className="returns-container">
                <h1>Returns & Refunds</h1>
                <div className="last-updated">Last Updated: March 15, 2024</div>

                <div className="policy-highlights">
                    <div className="highlight-card">
                        <FaBox />
                        <h3>30-Day Returns</h3>
                        <p>Easy returns within 30 days of delivery</p>
                    </div>
                    <div className="highlight-card">
                        <FaTruck />
                        <h3>Free Return Shipping</h3>
                        <p>We cover return shipping costs</p>
                    </div>
                    <div className="highlight-card">
                        <FaMoneyBillWave />
                        <h3>Fast Refunds</h3>
                        <p>Refunds processed within 2-3 business days</p>
                    </div>
                    <div className="highlight-card">
                        <FaShieldAlt />
                        <h3>Money-Back Guarantee</h3>
                        <p>100% satisfaction guaranteed</p>
                    </div>
                </div>

                <section className="returns-section">
                    <h2>Return Policy</h2>
                    <p>We want you to be completely satisfied with your purchase. If you're not happy with your order, we accept returns within 30 days of delivery for a full refund.</p>
                    
                    <h3>Eligible Items</h3>
                    <ul>
                        <li>Items must be unused and in original packaging</li>
                        <li>Products must have all original tags and seals intact</li>
                        <li>Beauty products must not be opened for hygiene reasons</li>
                        <li>Items must be in resalable condition</li>
                    </ul>
                </section>

                <section className="returns-section">
                    <h2>How to Return</h2>
                    <div className="steps-container">
                        <div className="step">
                            <div className="step-number">1</div>
                            <h4>Initiate Return</h4>
                            <p>Log into your account and select the order you want to return</p>
                        </div>
                        <div className="step">
                            <div className="step-number">2</div>
                            <h4>Print Label</h4>
                            <p>Download and print your free return shipping label</p>
                        </div>
                        <div className="step">
                            <div className="step-number">3</div>
                            <h4>Pack Items</h4>
                            <p>Pack items securely in original packaging</p>
                        </div>
                        <div className="step">
                            <div className="step-number">4</div>
                            <h4>Ship</h4>
                            <p>Drop off package at any authorized shipping location</p>
                        </div>
                    </div>
                </section>

                <section className="returns-section">
                    <h2>Refund Process</h2>
                    <ul>
                        <li>Refunds are processed within 2-3 business days of receiving your return</li>
                        <li>Original payment method will be refunded</li>
                        <li>Shipping costs are refunded for defective items</li>
                        <li>You'll receive an email confirmation when refund is processed</li>
                    </ul>
                </section>

                <section className="returns-section">
                    <h2>Non-Returnable Items</h2>
                    <ul>
                        <li>Opened beauty products (for hygiene reasons)</li>
                        <li>Personal care items that have been used</li>
                        <li>Gift cards and digital products</li>
                        <li>Clearance items marked as final sale</li>
                    </ul>
                </section>

                <div className="contact-support">
                    <h2>Need Help?</h2>
                    <p>Our customer service team is here to assist you with returns and refunds.</p>
                    <div className="contact-methods">
                        <div className="contact-method">
                            <i className="fas fa-envelope"></i>
                            <p>Email: returns@glowaura.com</p>
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

export default Returns; 