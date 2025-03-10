import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/landing'
import { Cursor } from './components/cursor';
import Footer from './components/footer';
import Header from './components/header';
import Fragrance from './pages/fragrance';
import Miscellaneous from './pages/miscellaneous';
import Makeup from './pages/makeup';
import Skincare from './pages/skincare';
import Haircare from './pages/haircare';
import ProductDetail from './pages/product-detail';
import CartPage from './pages/cart-page';
import { CartProvider } from './contexts/cart.context';
import ScrollToTop from './components/scroll-to-top';
import { FaTruck, FaBolt, FaGift } from 'react-icons/fa';
import FAQ from './pages/faq';
import PrivacyPolicy from './pages/privacy-policy';
import TermsOfService from './pages/terms';
import Returns from './pages/returns';
import Shipping from './pages/shipping';
import TrackOrder from './pages/track-order';
import AuthenticProducts from './pages/authentic';
import PrimeDelivery from './pages/prime-delivery';
import SecurePayment from './pages/secure-payment';
import Support from './pages/support';

const PromoBanner = () => {
  const promoItems = [
    { icon: <FaTruck />, text: "FREE Prime Shipping on Orders $25+" },
    { icon: <FaGift />, text: "New Customers: Get 10% OFF" }
  ];

  return (
    <div className="promo-banner">
      <div className="promo-scroll">
        {[...Array(3)].map((_, i) => (
          promoItems.map((item, index) => (
            <div key={`${i}-${index}`} className="promo-item">
              {item.icon}
              <span>{item.text}</span>
            </div>
          ))
        ))}
      </div>
    </div>
  );
};

function App() {
  return (
    <CartProvider>
      <Router>
        <ScrollToTop />
        <PromoBanner />
        <>
          <Header />
          <Cursor />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/fragrance" element={<Fragrance />} />
            <Route path="/miscellaneous" element={<Miscellaneous />} />
            <Route path="/makeup" element={<Makeup />} />
            <Route path="/skincare" element={<Skincare />} />
            <Route path="/haircare" element={<Haircare />} />
            <Route path="/product/:productId" element={<ProductDetail />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/faq" element={<FAQ />} />
            <Route path="/privacy" element={<PrivacyPolicy />} />
            <Route path="/terms" element={<TermsOfService />} />
            <Route path="/returns" element={<Returns />} />
            <Route path="/shipping" element={<Shipping />} />
            <Route path="/track-order" element={<TrackOrder />} />
            <Route path="/authentic" element={<AuthenticProducts />} />
            <Route path="/prime-delivery" element={<PrimeDelivery />} />
            <Route path="/secure-payment" element={<SecurePayment />} />
            <Route path="/support" element={<Support />} />
          </Routes>
          <Footer />
        </>
      </Router>
    </CartProvider>
  );
}

export default App;
