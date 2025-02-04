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

function App() {
  return (
    <CartProvider>
      <Router>
        <ScrollToTop />
        <div>
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
          </Routes>
          {/* <Recommendations /> */}
          <Footer />
        </div>
      </Router>
    </CartProvider>
  );
}

export default App;
