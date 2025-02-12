import React from 'react';
import './support.styles.scss';
import SEO from '../../components/seo';
import { Link } from 'react-router-dom';
import { FaHeadset, FaEnvelope, FaPhone, FaComments, FaWhatsapp, FaClock, FaGlobe } from 'react-icons/fa';

const Support = () => {
    return (
        <div className="support-page">
            <SEO 
                title="24/7 Customer Support | Your Beauty Products"
                description="Get help anytime with our 24/7 customer support service."
            />
            
            <div className="support-container">
                <div className="hero-section">
                    <FaHeadset className="support-icon" />
                    <h1>24/7 Customer Support</h1>
                    <p>We're here to help you anytime, anywhere</p>
                </div>

                <div className="contact-methods">
                    <div className="method-card">
                        <FaPhone />
                        <h3>Phone Support</h3>
                        <p>1-800-BEAUTY</p>
                        <span className="availability">24/7 Available</span>
                        <button className="contact-button">Call Now</button>
                    </div>
                    <div className="method-card">
                        <FaEnvelope />
                        <h3>Email Support</h3>
                        <p>support@yourbeauty.com</p>
                        <span className="availability">Response within 2 hours</span>
                        <button className="contact-button">Send Email</button>
                    </div>
                    <div className="method-card">
                        <FaComments />
                        <h3>Live Chat</h3>
                        <p>Chat with our experts</p>
                        <span className="availability">Instant Response</span>
                        <button className="contact-button">Start Chat</button>
                    </div>
                    <div className="method-card">
                        <FaWhatsapp />
                        <h3>WhatsApp</h3>
                        <p>Message us anytime</p>
                        <span className="availability">24/7 Available</span>
                        <button className="contact-button">WhatsApp Us</button>
                    </div>
                </div>

                <section className="support-features">
                    <h2>Why Choose Our Support?</h2>
                    <div className="features-grid">
                        <div className="feature">
                            <FaClock />
                            <h3>24/7 Availability</h3>
                            <p>Round-the-clock support for all your needs</p>
                        </div>
                        <div className="feature">
                            <FaGlobe />
                            <h3>Global Support</h3>
                            <p>Support available in multiple languages</p>
                        </div>
                        <div className="feature">
                            <i className="fas fa-bolt"></i>
                            <h3>Quick Response</h3>
                            <p>Average response time under 2 minutes</p>
                        </div>
                        <div className="feature">
                            <i className="fas fa-user-shield"></i>
                            <h3>Expert Team</h3>
                            <p>Trained beauty and product specialists</p>
                        </div>
                    </div>
                </section>

                <section className="support-categories">
                    <h2>How Can We Help You?</h2>
                    <div className="categories-grid">
                        <div className="category">
                            <h3>Orders & Shipping</h3>
                            <ul>
                                <li>Track your order</li>
                                <li>Shipping information</li>
                                <li>Order modifications</li>
                                <li>Delivery issues</li>
                            </ul>
                        </div>
                        <div className="category">
                            <h3>Returns & Refunds</h3>
                            <ul>
                                <li>Return policy</li>
                                <li>Start a return</li>
                                <li>Refund status</li>
                                <li>Damaged items</li>
                            </ul>
                        </div>
                        <div className="category">
                            <h3>Product Support</h3>
                            <ul>
                                <li>Product information</li>
                                <li>Usage guidelines</li>
                                <li>Product recommendations</li>
                                <li>Authenticity verification</li>
                            </ul>
                        </div>
                        <div className="category">
                            <h3>Account & Payment</h3>
                            <ul>
                                <li>Account issues</li>
                                <li>Payment problems</li>
                                <li>Security concerns</li>
                                <li>Password reset</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <section className="faq-preview">
                    <h2>Frequently Asked Questions</h2>
                    <div className="faq-grid">
                        <div className="faq-item">
                            <h3>How do I track my order?</h3>
                            <p>You can track your order by clicking on 'Track Order' in your account or using the tracking number sent to your email.</p>
                        </div>
                        <div className="faq-item">
                            <h3>What is your return policy?</h3>
                            <p>We offer a 30-day return policy for most items. Products must be unused and in original packaging.</p>
                        </div>
                        <div className="faq-item">
                            <h3>How long does shipping take?</h3>
                            <p>Prime shipping takes 2-5 business days. Standard shipping takes 5-7 business days.</p>
                        </div>
                        <div className="faq-item">
                            <h3>Are your products authentic?</h3>
                            <p>Yes, all our products are 100% authentic and sourced directly through Amazon's verified channels.</p>
                        </div>
                    </div>
                    <div className="view-more">
                        <Link to="/faq" className="view-more-button">View All FAQs</Link>
                    </div>
                </section>

                <div className="support-commitment">
                    <h2>Our Support Commitment</h2>
                    <div className="commitment-content">
                        <div className="commitment-text">
                            <p>We're committed to providing you with the best possible support experience:</p>
                            <ul>
                                <li>24/7 availability across all time zones</li>
                                <li>Multilingual support team</li>
                                <li>Personalized assistance</li>
                                <li>Quick resolution guarantee</li>
                            </ul>
                        </div>
                        <div className="commitment-badge">
                            <FaHeadset />
                            <span>Always Here<br />For You</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Support; 