import React from 'react';
import { Link } from 'react-router-dom';
import Directory from "../../components/directory";
import CounterAnimation from '../../components/counter-animation';
import SEO from '../../components/seo';
import "./landing.styles.scss";
import { 
    FaTruck, 
    FaShieldAlt, 
    FaAward,
    FaUndo, 
} from 'react-icons/fa';

const LandingPage = () => {
    const scrollToDirectory = () => {
        const directorySection = document.getElementById('directory-section');
        if (directorySection) {
            directorySection.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }
    };

    return (
        <>
            <SEO 
                title="Beauty Products | Premium Amazon Beauty Collection"
                description="Discover our curated collection of premium Amazon beauty products. Shop makeup, skincare, haircare and fragrances with Prime shipping."
            />
            
            <div className="landing-page">
                <section className="hero-section">
                    <div className="hero-content">
                        <h1>Premium Beauty Products</h1>
                        <p>Discover Amazon's Best Beauty Products with Prime Shipping</p>
                        <div className="hero-badges">
                            <div className="badge">
                                <span>Amazon Direct</span>
                            </div>
                            <div className="badge">
                                <span>Prime Delivery</span>
                            </div>
                            <div className="badge">
                                <span>Secure Shopping</span>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="features-section">
                    <div className="feature-card">
                        <FaAward />
                        <h3>Amazon's Choice</h3>
                        <p>Handpicked premium products</p>
                    </div>
                    <div className="feature-card">
                        <FaTruck />
                        <h3>Fast Shipping</h3>
                        <p>2-5 day Prime delivery</p>
                    </div>
                    <div className="feature-card">
                        <FaShieldAlt />
                        <h3>Secure Shopping</h3>
                        <p>Protected by Amazon</p>
                    </div>
                    <div className="feature-card">
                        <FaUndo />
                        <h3>Easy Returns</h3>
                        <p>30-day return policy</p>
                    </div>
                </section>
                

                <div id="directory-section">
                    <Directory />
                </div>

                <section className="benefits-section">
                    <h2>Why Choose Us</h2>
                    <div className="benefits-grid">
                        <div className="benefit-item">
                            <h3>Amazon Direct</h3>
                            <p>All products shipped directly from Amazon warehouses</p>
                        </div>
                        <div className="benefit-item">
                            <h3>Authentic Products</h3>
                            <p>100% genuine products with Amazon guarantee</p>
                        </div>
                        <div className="benefit-item">
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
                        <button onClick={scrollToDirectory} className="cta-button">
                            Explore Products
                        </button>
                    </div>
                </section>
            </div>
        </>
    );
};

export default LandingPage;