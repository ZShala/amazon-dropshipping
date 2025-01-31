import React from 'react';
import './toast.styles.scss';

const Toast = ({ message, isVisible, onClose }) => {
    return (
        <div className={`toast ${isVisible ? 'visible' : ''}`}>
            <span>{message}</span>
            <button onClick={onClose}>&times;</button>
        </div>
    );
};

export default Toast; 