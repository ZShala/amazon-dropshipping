import React, { useState } from "react";
import styles from "./ProductRecommendation.module.css";

const Loader = () => (
  <div className={styles.loader}>
    <div className={styles.spinner}></div>
  </div>
);

function Recommendations() {
  const [productId, setProductId] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = async () => {
    if (!productId) return;
    
    setLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/recommendations?product_id=${productId}`
      );
      const data = await response.json();
      if (data.recommendations) {
        setRecommendations(data.recommendations);
      } else {
        setRecommendations([]);
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    } finally {
      setLoading(false);  
    }
  };

  return (
    <div>
      <h1>Product Recommendations</h1>
      <input
        type="text"
        placeholder="Enter Product ID"
        value={productId}
        onChange={(e) => setProductId(e.target.value)}
      />
      <button onClick={fetchRecommendations}>Get Recommendations</button>

      {loading ? (
        <Loader /> 
      ) : recommendations.length > 0 ? (
        <ul className={styles.productsContainer}>
          {recommendations.map((rec, index) => (
            <li key={index} className={styles.productItem}>
              <img src={rec.ImageURL} alt={rec.ProductId} />
              <p>{rec.ProductType}</p>
              <p>Rating: {rec.Rating}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No recommendations available.</p>
      )}
    </div>
  );
}

export default Recommendations;
