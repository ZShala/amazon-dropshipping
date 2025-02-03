import React, { useState, useEffect, useRef } from 'react';
import './counter-animation.styles.scss';

const CounterAnimation = ({ end, duration = 2000, suffix = '' }) => {
    const [count, setCount] = useState(0);
    const countRef = useRef(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                if (entries[0].isIntersecting) {
                    startCounting();
                }
            },
            { threshold: 0.5 }
        );

        if (countRef.current) {
            observer.observe(countRef.current);
        }

        return () => {
            if (countRef.current) {
                observer.unobserve(countRef.current);
            }
        };
    }, []);

    const startCounting = () => {
        let startTime;
        const startValue = 0;
        const endValue = parseFloat(end);

        const animate = (currentTime) => {
            if (!startTime) startTime = currentTime;
            const progress = (currentTime - startTime) / duration;

            if (progress < 1) {
                const currentCount = startValue + (endValue - startValue) * progress;
                setCount(currentCount);
                requestAnimationFrame(animate);
            } else {
                setCount(endValue);
            }
        };

        requestAnimationFrame(animate);
    };

    return (
        <span ref={countRef} className="counter">
            {typeof count === 'number' && count % 1 !== 0 
                ? count.toFixed(1) 
                : Math.floor(count)}
            {suffix}
        </span>
    );
};

export default CounterAnimation; 