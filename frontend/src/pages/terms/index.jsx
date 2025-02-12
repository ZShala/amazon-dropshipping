import React from 'react';
import './terms.styles.scss';
import SEO from '../../components/seo';

const TermsOfService = () => {
    return (
        <div className="terms-page">
            <SEO 
                title="Terms of Service | Your Beauty Products"
                description="Read our terms of service and conditions for using our platform."
            />
            
            <div className="terms-container">
                <h1>Terms of Service</h1>
                <div className="last-updated">Last Updated: March 15, 2024</div>

                <section className="terms-section">
                    <h2>1. Acceptance of Terms</h2>
                    <p>By accessing and using this website, you accept and agree to be bound by the terms and provision of this agreement.</p>
                </section>

                <section className="terms-section">
                    <h2>2. Use License</h2>
                    <ul>
                        <li>Permission is granted to temporarily download one copy of the materials for personal, non-commercial transitory viewing only.</li>
                        <li>This is the grant of a license, not a transfer of title.</li>
                        <li>You may not modify or copy the materials.</li>
                        <li>You may not use the materials for any commercial purpose.</li>
                    </ul>
                </section>

                <section className="terms-section">
                    <h2>3. Product Information</h2>
                    <ul>
                        <li>We strive to display accurate product information, including prices and availability.</li>
                        <li>We reserve the right to modify prices without notice.</li>
                        <li>Product images are representative and may vary from actual products.</li>
                        <li>We partner with Amazon for product fulfillment and authenticity guarantee.</li>
                    </ul>
                </section>

                <section className="terms-section">
                    <h2>4. Shipping & Returns</h2>
                    <ul>
                        <li>Orders are typically processed within 1-2 business days.</li>
                        <li>Prime shipping is available for eligible orders.</li>
                        <li>30-day return policy for most items.</li>
                        <li>Items must be unused and in original packaging.</li>
                    </ul>
                </section>

                <section className="terms-section">
                    <h2>5. User Accounts</h2>
                    <ul>
                        <li>You are responsible for maintaining the confidentiality of your account.</li>
                        <li>You must be 18 years or older to create an account.</li>
                        <li>We reserve the right to terminate accounts at our discretion.</li>
                        <li>You agree to provide accurate and complete information.</li>
                    </ul>
                </section>

                <section className="terms-section">
                    <h2>6. Payment Terms</h2>
                    <ul>
                        <li>We accept major credit cards and PayPal.</li>
                        <li>All transactions are processed securely.</li>
                        <li>Prices are in USD unless otherwise noted.</li>
                        <li>Sales tax will be added where applicable.</li>
                    </ul>
                </section>

                <section className="terms-section">
                    <h2>7. Disclaimer</h2>
                    <p>The materials on this website are provided on an 'as is' basis. We make no warranties, expressed or implied, and hereby disclaim and negate all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>
                </section>

                <section className="terms-section">
                    <h2>8. Contact Information</h2>
                    <div className="contact-info">
                        <p>For any questions regarding these terms, please contact us at:</p>
                        <p>Email: legal@glowaura.com</p>
                        <p>Phone: 1-800-BEAUTY</p>
                        <p>Address: 123 Beauty Street, New York, NY 10001</p>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default TermsOfService; 