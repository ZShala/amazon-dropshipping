import React from 'react';
import './secure-payment.styles.scss';
import SEO from '../../components/seo';
import { FaLock, FaCreditCard, FaShieldAlt, FaAmazon, FaPaypal, FaApplePay, FaGooglePay } from 'react-icons/fa';
import { SiVisa, SiMastercard, SiAmericanexpress } from 'react-icons/si';

const SecurePayment = () => {
    return (
        <div className="secure-payment-page">
            <SEO 
                title="Secure Payment | Your Beauty Products"
                description="Learn about our secure payment methods and transaction protection."
            />
            
            <div className="secure-payment-container">
                <div className="hero-section">
                    <FaLock className="security-icon" />
                    <h1>Secure Payment</h1>
                    <p>Your security is our top priority</p>
                </div>

                <div className="payment-methods">
                    <h2>Accepted Payment Methods</h2>
                    <div className="methods-grid">
                        <div className="method-card">
                            <SiVisa />
                            <span>Visa</span>
                        </div>
                        <div className="method-card">
                            <SiMastercard />
                            <span>Mastercard</span>
                        </div>
                        <div className="method-card">
                            <SiAmericanexpress />
                            <span>American Express</span>
                        </div>
                        <div className="method-card">
                            <FaPaypal />
                            <span>PayPal</span>
                        </div>
                        <div className="method-card">
                            <FaApplePay />
                            <span>Apple Pay</span>
                        </div>
                        <div className="method-card">
                            <FaGooglePay />
                            <span>Google Pay</span>
                        </div>
                        <div className="method-card">
                            <FaAmazon />
                            <span>Amazon Pay</span>
                        </div>
                    </div>
                </div>

                <div className="security-features">
                    <h2>Security Features</h2>
                    <div className="features-grid">
                        <div className="feature-card">
                            <FaLock />
                            <h3>SSL Encryption</h3>
                            <p>256-bit SSL encryption for all transactions</p>
                        </div>
                        <div className="feature-card">
                            <FaShieldAlt />
                            <h3>Fraud Protection</h3>
                            <p>Advanced fraud detection system</p>
                        </div>
                        <div className="feature-card">
                            <FaCreditCard />
                            <h3>Secure Processing</h3>
                            <p>PCI DSS compliant payment processing</p>
                        </div>
                        <div className="feature-card">
                            <FaAmazon />
                            <h3>Amazon Security</h3>
                            <p>Protected by Amazon's secure infrastructure</p>
                        </div>
                    </div>
                </div>

                <section className="security-info">
                    <h2>Our Security Measures</h2>
                    <div className="security-grid">
                        <div className="security-item">
                            <h3>Data Protection</h3>
                            <ul>
                                <li>End-to-end encryption</li>
                                <li>Secure data storage</li>
                                <li>Regular security audits</li>
                                <li>No card data storage</li>
                            </ul>
                        </div>
                        <div className="security-item">
                            <h3>Transaction Security</h3>
                            <ul>
                                <li>Real-time fraud monitoring</li>
                                <li>Secure payment gateway</li>
                                <li>3D Secure verification</li>
                                <li>Two-factor authentication</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <section className="payment-process">
                    <h2>Safe Payment Process</h2>
                    <div className="process-steps">
                        <div className="step">
                            <div className="step-number">1</div>
                            <h4>Choose Payment</h4>
                            <p>Select your preferred payment method</p>
                        </div>
                        <div className="step">
                            <div className="step-number">2</div>
                            <h4>Enter Details</h4>
                            <p>Provide payment information securely</p>
                        </div>
                        <div className="step">
                            <div className="step-number">3</div>
                            <h4>Verify</h4>
                            <p>Complete security verification if required</p>
                        </div>
                        <div className="step">
                            <div className="step-number">4</div>
                            <h4>Confirm</h4>
                            <p>Review and confirm your payment</p>
                        </div>
                    </div>
                </section>

                <section className="guarantees">
                    <h2>Our Guarantees</h2>
                    <div className="guarantees-content">
                        <div className="guarantee-text">
                            <p>We provide the following security guarantees:</p>
                            <ul>
                                <li>100% secure transactions</li>
                                <li>Fraud protection guarantee</li>
                                <li>Purchase protection</li>
                                <li>Secure refund process</li>
                            </ul>
                        </div>
                        <div className="guarantee-badge">
                            <FaShieldAlt />
                            <span>100% Secure<br />Payments</span>
                        </div>
                    </div>
                </section>

                <div className="payment-support">
                    <h2>Payment Support</h2>
                    <p>Having issues with payment? Our team is here to help</p>
                    <div className="contact-methods">
                        <div className="contact-method">
                            <i className="fas fa-envelope"></i>
                            <p>Email: payments@glowaura.com</p>
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

export default SecurePayment; 