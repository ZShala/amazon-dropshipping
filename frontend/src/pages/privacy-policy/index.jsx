import React from 'react';
import './privacy-policy.styles.scss';
import SEO from '../../components/seo';

const PrivacyPolicy = () => {
    return (
        <div className="privacy-policy-page">
            <SEO 
                title="Privacy Policy | Your Beauty Products"
                description="Learn about how we collect, use, and protect your personal information."
            />
            
            <div className="privacy-policy-container">
                <h1>Privacy Policy</h1>
                <div className="last-updated">Last Updated: March 15, 2024</div>

                <section className="policy-section">
                    <h2>1. Information We Collect</h2>
                    <p>We collect information that you provide directly to us, including:</p>
                    <ul>
                        <li>Name and contact information</li>
                        <li>Billing and shipping addresses</li>
                        <li>Payment information</li>
                        <li>Order history and preferences</li>
                        <li>Communication history with our customer service</li>
                    </ul>
                </section>

                <section className="policy-section">
                    <h2>2. How We Use Your Information</h2>
                    <p>We use the information we collect to:</p>
                    <ul>
                        <li>Process your orders and payments</li>
                        <li>Deliver products to you</li>
                        <li>Send order confirmations and updates</li>
                        <li>Provide customer support</li>
                        <li>Improve our services and products</li>
                        <li>Send marketing communications (with your consent)</li>
                    </ul>
                </section>

                <section className="policy-section">
                    <h2>3. Information Sharing</h2>
                    <p>We share your information with:</p>
                    <ul>
                        <li>Amazon for order fulfillment</li>
                        <li>Payment processors for secure transactions</li>
                        <li>Shipping partners for delivery</li>
                        <li>Service providers who assist our operations</li>
                    </ul>
                </section>

                <section className="policy-section">
                    <h2>4. Data Security</h2>
                    <p>We implement appropriate security measures to protect your personal information, including:</p>
                    <ul>
                        <li>Encryption of sensitive data</li>
                        <li>Secure payment processing</li>
                        <li>Regular security assessments</li>
                        <li>Limited access to personal information</li>
                    </ul>
                </section>

                <section className="policy-section">
                    <h2>5. Your Rights</h2>
                    <p>You have the right to:</p>
                    <ul>
                        <li>Access your personal information</li>
                        <li>Correct inaccurate data</li>
                        <li>Request deletion of your data</li>
                        <li>Opt-out of marketing communications</li>
                        <li>Request data portability</li>
                    </ul>
                </section>

                <section className="policy-section">
                    <h2>6. Contact Us</h2>
                    <p>If you have any questions about this Privacy Policy, please contact us at:</p>
                    <div className="contact-info">
                        <p>Email: privacy@glowaura.com</p>
                        <p>Phone: 1-800-BEAUTY</p>
                        <p>Address: 123 Beauty Street, New York, NY 10001</p>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default PrivacyPolicy; 