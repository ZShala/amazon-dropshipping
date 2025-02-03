import React from 'react';
import { Link } from 'react-router-dom';
import Directory from "../../components/directory";
import CounterAnimation from '../../components/counter-animation';
import "./landing.styles.scss";

const LandingPage = () => {
    return (
        <div className="landing-page">
            <section className="hero-section">
                <div className="hero-content">
                    <h1>Premium Beauty Products</h1>
                    <p>Discover Amazon's Best Beauty Products with Prime Shipping</p>
                    <div className="hero-badges">
                        <div className="badge">
                            <i className="fab fa-amazon"></i>
                            Amazon Direct
                        </div>
                        <div className="badge">
                            <i className="fas fa-truck-fast"></i>
                            Prime Delivery
                        </div>
                        <div className="badge">
                            <i className="fas fa-shield-alt"></i>
                            Secure Shopping
                        </div>
                    </div>
                </div>
            </section>

            <section className="features-section">
                <div className="feature-card">
                    <i className="fab fa-amazon"></i>
                    <h3>Amazon's Choice</h3>
                    <p>Handpicked premium products</p>
                </div>
                <div className="feature-card">
                    <i className="fas fa-truck"></i>
                    <h3>Fast Shipping</h3>
                    <p>2-5 day Prime delivery</p>
                </div>
                <div className="feature-card">
                    <i className="fas fa-shield-alt"></i>
                    <h3>Secure Shopping</h3>
                    <p>Protected by Amazon</p>
                </div>
                <div className="feature-card">
                    <i className="fas fa-undo"></i>
                    <h3>Easy Returns</h3>
                    <p>30-day return policy</p>
                </div>
            </section>
            
            <Directory />

            <section className="benefits-section">
                <h2>Why Choose Us</h2>
                <div className="benefits-grid">
                    <div className="benefit-item">
                        <div className="icon">
                            <i className="fas fa-box"></i>
                        </div>
                        <h3>Amazon Direct</h3>
                        <p>All products shipped directly from Amazon warehouses</p>
                    </div>
                    <div className="benefit-item">
                        <div className="icon">
                            <i className="fas fa-check-circle"></i>
                        </div>
                        <h3>Authentic Products</h3>
                        <p>100% genuine products with Amazon guarantee</p>
                    </div>
                    <div className="benefit-item">
                        <div className="icon">
                            <i className="fas fa-tag"></i>
                        </div>
                        <h3>Best Prices</h3>
                        <p>Competitive prices with regular Amazon deals</p>
                    </div>
                </div>
            </section>

            <section className="trust-section">
                <div className="trust-content">
                    <div className="trust-item">
                        <div className="number">
                            <CounterAnimation end={50} suffix="K+" />
                        </div>
                        <div className="label">Happy Customers</div>
                    </div>
                    <div className="trust-item">
                        <div className="number">
                            <CounterAnimation end={10} suffix="K+" />
                        </div>
                        <div className="label">Amazon Products</div>
                    </div>
                    <div className="trust-item">
                        <div className="number">
                            <CounterAnimation end={4.8} />
                        </div>
                        <div className="label">Average Rating</div>
                    </div>
                    <div className="trust-item">
                        <div className="number">
                            <CounterAnimation end={99} suffix="%" />
                        </div>
                        <div className="label">On-time Delivery</div>
                    </div>
                </div>
            </section>

            <section className="cta-section">
                <div className="cta-content">
                    <h2>Start Shopping Today</h2>
                    <p>Browse our curated selection of Amazon beauty products</p>
                    <Link to="/products" className="cta-button">
                        Explore Products
                        <i className="fas fa-arrow-right"></i>
                    </Link>
                </div>
            </section>
        </div>
    );
};

export default LandingPage;