import React from 'react';
import { Link } from 'react-router-dom';
import visaLogo from '../../assets/visa-logo.webp';
import mastercardLogo from '../../assets/mastercard-logo.png';
import paypalLogo from '../../assets/paypal-logo.png';
import { FaFacebookF, FaInstagram, FaTiktok } from 'react-icons/fa';
import './footer.styles.scss';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-section">
                    <h3>About Us</h3>
                    <p>We partner with Amazon to bring you premium beauty products with fast Prime shipping and authentic product guarantee.</p>
                    <div className="amazon-partnership">
                        <i className="fab fa-amazon"></i>
                        <span>Official Amazon Partner</span>
                    </div>
                </div>

                <div className="footer-section">
                    <h3>Customer Service</h3>
                    <ul>
                        <li>
                            <i className="fas fa-truck"></i>
                            <Link to="/shipping">Shipping Information</Link>
                        </li>
                        <li>
                            <i className="fas fa-undo"></i>
                            <Link to="/returns">Returns & Refunds</Link>
                        </li>
                        <li>
                            <i className="fas fa-question-circle"></i>
                            <Link to="/faq">FAQ</Link>
                        </li>
                        <li>
                            <i className="fas fa-box"></i>
                            Track Your Order
                        </li>
                    </ul>
                </div>

                <div className="footer-section">
                    <h3>Shopping Benefits</h3>
                    <ul>
                        <li>
                            <i className="fas fa-check-circle"></i>
                            Authentic Amazon Products
                        </li>
                        <li>
                            <i className="fas fa-truck-fast"></i>
                            Prime Delivery 2-5 Days
                        </li>
                        <li>
                            <i className="fas fa-shield-alt"></i>
                            Secure Payment
                        </li>
                        <li>
                            <i className="fas fa-headset"></i>
                            24/7 Support
                        </li>
                    </ul>
                </div>

                <div className="footer-section">
                    <h3>Connect With Us</h3>
                    <div className="social-icons">
                        <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="social-icon">
                            <FaFacebookF />
                        </a>
                        <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="social-icon">
                            <FaInstagram />
                        </a>
                        <a href="https://tiktok.com" target="_blank" rel="noopener noreferrer" className="social-icon">
                            <FaTiktok />
                        </a>
                    </div>
                    <div className="payment-methods">
                        <h4>We Accept</h4>
                        <div className="payment-icons">
                            <img src={visaLogo} alt="visa" />
                            <img src={mastercardLogo} alt="mastercard" />
                            <img src={paypalLogo} alt="paypal" />
                        </div>
                    </div>
                </div>
            </div>

            <div className="footer-bottom">
                <div className="trust-badges">
                    <div className="badge">
                        <i className="fab fa-amazon"></i>
                        Amazon Prime Partner
                    </div>
                    <div className="badge">
                        <i className="fas fa-shield-alt"></i>
                        Secure Shopping
                    </div>
                    <div className="badge">
                        <i className="fas fa-undo"></i>
                        30-Day Returns
                    </div>
                </div>
                <div className="copyright">
                    <p>&copy; 2025 GlowAura. All rights reserved. Not affiliated with Amazon.com</p>
                    <div className="legal-links">
                        <Link to="/privacy">Privacy Policy</Link>
                        <Link to="/terms">Terms of Service</Link>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;