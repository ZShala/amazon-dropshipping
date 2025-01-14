CREATE DATABASE product_recommendations;

USE product_recommendations;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ProductId VARCHAR(255) NOT NULL,
    ProductType VARCHAR(255),
    Rating DECIMAL(3,2),
    Timestamp TIMESTAMP,
    URL TEXT
);
