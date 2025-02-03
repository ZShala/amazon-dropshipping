import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import CartIcon from '../cart-icon';
import logo from '../../assets/logo-black.png';

import "./header.styles.scss";

const Header = () => {
    return (
        <header className="header">
            <div className="header-content">
                <Link to="/" className="logo">
                    <img src={logo} alt="logo" width={150} height="auto" />
                </Link>

                <nav className="navigation">
                    <CartIcon />
                </nav>
            </div>
        </header>
    );
};

export default Header;