import React from 'react';
import './authentic.styles.scss';
import SEO from '../../components/seo';
import { FaCheckCircle, FaShieldAlt, FaAmazon, FaBoxOpen } from 'react-icons/fa';

const AuthenticProducts = () => {
    return (
        <div className="authentic-page">
            <SEO 
                title="Authentic Amazon Products | Your Beauty Products"
                description="Learn about our authentic product guarantee and partnership with Amazon."
            />
            
            <div className="authentic-container">
                <div className="hero-section">
                    <FaAmazon className="amazon-icon" />
                    <h1>Authentic Amazon Products</h1>
                    <p>We partner directly with Amazon to ensure 100% authentic products</p>
                </div>

                <div className="benefits-grid">
                    <div className="benefit-card">
                        <FaCheckCircle />
                        <h3>Guaranteed Authentic</h3>
                        <p>All products are sourced directly from authorized manufacturers through Amazon's verified channels</p>
                    </div>
                    <div className="benefit-card">
                        <FaShieldAlt />
                        <h3>Amazon Protection</h3>
                        <p>Every purchase is protected by Amazon's A-to-Z Guarantee</p>
                    </div>
                    <div className="benefit-card">
                        <FaBoxOpen />
                        <h3>Factory Sealed</h3>
                        <p>Products arrive in original, unopened packaging</p>
                    </div>
                    <div className="benefit-card">
                        <FaAmazon />
                        <h3>Prime Benefits</h3>
                        <p>Enjoy fast, free shipping with Amazon Prime</p>
                    </div>
                </div>

                <section className="info-section">
                    <h2>Our Amazon Partnership</h2>
                    <p>As an official Amazon partner, we maintain strict quality control standards to ensure every product you receive is genuine and meets Amazon's high-quality requirements.</p>
                    
                    <div className="partnership-features">
                        <div className="feature">
                            <h3>Direct Sourcing</h3>
                            <ul>
                                <li>Products sourced directly from Amazon's warehouses</li>
                                <li>No third-party sellers or intermediaries</li>
                                <li>Complete product traceability</li>
                                <li>Original manufacturer warranty</li>
                            </ul>
                        </div>
                        <div className="feature">
                            <h3>Quality Assurance</h3>
                            <ul>
                                <li>Rigorous quality checks</li>
                                <li>Authentic product verification</li>
                                <li>Proper storage and handling</li>
                                <li>Temperature-controlled shipping</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <section className="verification-section">
                    <h2>How to Verify Authenticity</h2>
                    <div className="verification-steps">
                        <div className="step">
                            <div className="step-number">1</div>
                            <h4>Check the Seal</h4>
                            <p>Look for intact factory seals and Amazon's security labels</p>
                        </div>
                        <div className="step">
                            <div className="step-number">2</div>
                            <h4>Scan QR Code</h4>
                            <p>Use Amazon app to scan product's authenticity QR code</p>
                        </div>
                        <div className="step">
                            <div className="step-number">3</div>
                            <h4>Verify Packaging</h4>
                            <p>Check for original brand packaging and security features</p>
                        </div>
                        <div className="step">
                            <div className="step-number">4</div>
                            <h4>Register Product</h4>
                            <p>Register your product with the manufacturer</p>
                        </div>
                    </div>
                </section>

                <section className="guarantee-section">
                    <h2>Our Guarantee</h2>
                    <div className="guarantee-content">
                        <div className="guarantee-text">
                            <p>If you receive a product that you believe is not authentic, we offer:</p>
                            <ul>
                                <li>Immediate full refund</li>
                                <li>Free return shipping</li>
                                <li>Product replacement</li>
                                <li>Additional 10% off your next purchase</li>
                            </ul>
                        </div>
                        <div className="guarantee-badge">
                            <FaShieldAlt />
                            <span>100% Authentic<br />Guaranteed</span>
                        </div>
                    </div>
                </section>

                <div className="contact-support">
                    <h2>Questions About Authenticity?</h2>
                    <p>Our product specialists are here to help verify your product's authenticity</p>
                    <div className="contact-methods">
                        <div className="contact-method">
                            <i className="fas fa-envelope"></i>
                            <p>Email: authenticity@yourbeauty.com</p>
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

export default AuthenticProducts; 