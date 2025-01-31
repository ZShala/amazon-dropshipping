import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import CartIcon from '../cart-icon';

import "./header.styles.scss";

const Header = () => {
    return (
        <header className="header">
            <div className="header-content">
                <Link to="/" className="logo">
                    <h1>Your Logo</h1>
                </Link>

                <nav className="navigation">
                    <CartIcon />
                </nav>
            </div>
        </header>
    );
};

export default Header;