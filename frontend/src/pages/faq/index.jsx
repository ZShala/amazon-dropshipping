import React from 'react';
import './faq.styles.scss';
import SEO from '../../components/seo';

const FAQ = () => {
    const faqItems = [
        {
            question: "How do I place an order?",
            answer: "You can place an order by browsing our products, adding items to your cart, and proceeding to checkout. Follow the simple steps to enter your shipping and payment information."
        },
        {
            question: "What payment methods do you accept?",
            answer: "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and Amazon Pay for secure transactions."
        },
        {
            question: "How long does shipping take?",
            answer: "With Amazon Prime, most orders are delivered within 2-5 business days. International shipping times may vary by location."
        },
        {
            question: "What is your return policy?",
            answer: "We offer a 30-day return policy for most items. Products must be unused and in their original packaging. Contact our customer service for return authorization."
        },
        {
            question: "Are your products authentic?",
            answer: "Yes, all our products are 100% authentic and sourced directly from authorized manufacturers or through Amazon's verified channels."
        },
        {
            question: "Do you ship internationally?",
            answer: "Yes, we ship to most countries worldwide. Shipping costs and delivery times vary by location."
        },
        {
            question: "How can I track my order?",
            answer: "Once your order ships, you'll receive a tracking number via email. You can use this to track your package on our website or through Amazon's tracking system."
        },
        {
            question: "Are the products cruelty-free?",
            answer: "Many of our products are cruelty-free. You can check the product details page for specific information about each item's certifications."
        }
    ];

    return (
        <div className="faq-page">
            <SEO 
                title="FAQ | Your Beauty Products"
                description="Find answers to frequently asked questions about our beauty products, shipping, returns, and more."
            />
            
            <div className="faq-container">
                <h1>Frequently Asked Questions</h1>
                <div className="faq-grid">
                    {faqItems.map((item, index) => (
                        <div key={index} className="faq-item">
                            <h3>{item.question}</h3>
                            <p>{item.answer}</p>
                        </div>
                    ))}
                </div>

                <div className="contact-section">
                    <h2>Still have questions?</h2>
                    <p>Our customer service team is here to help!</p>
                    <div className="contact-methods">
                        <div className="contact-method">
                            <i className="fas fa-envelope"></i>
                            <p>Email us at: support@glowaura.com</p>
                        </div>
                        <div className="contact-method">
                            <i className="fas fa-phone"></i>
                            <p>Call us: 1-800-BEAUTY</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FAQ; 