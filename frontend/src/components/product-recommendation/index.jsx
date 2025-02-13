import React, { useState } from "react";
import "./product-recommendation.styles.scss";

const Loader = () => (
  <div className="loader">
    <div className="spinner"></div>
  </div>
);

function Recommendations() {
  const [productId, setProductId] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = async () => {
    if (!productId) {
      setError("Ju lutem vendosni një Product ID");
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `http://localhost:5001/recommendations?product_id=${productId}`
      );
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Ndodhi një gabim");
      }
      
      const data = await response.json();
      
      if (data.recommendations && data.recommendations.length > 0) {
        setRecommendations(data.recommendations);
      } else {
        setError("Nuk u gjetën rekomandime për këtë produkt");
        setRecommendations([]);
      }
    } catch (error) {
      console.error("Error:", error);
      setError(error.message);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="recommendations-container">
      <h1>Product Recommendations</h1>
      
      <div className="search-container">
        <input
          type="text"
          placeholder="Enter Product ID"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
        />
        <button 
          onClick={fetchRecommendations}
          disabled={loading || !productId}
        >
          {loading ? "Duke kërkuar..." : "Get Recommendations"}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading ? (
        <Loader />
      ) : recommendations.length > 0 ? (
        <ul className="products-container">
          {recommendations.map((rec, index) => (
            <li key={index} className="product-item">
              <img 
                src={rec.ImageURL} 
                alt={rec.ProductType}
                onError={(e) => {
                  e.target.src = "https://via.placeholder.com/150";
                }}
              />
              <div className="product-info">
                <p className="product-type">{rec.ProductType}</p>
                <p className="product-id">ID: {rec.ProductId}</p>
                <p className="rating">Rating: {rec.Rating}</p>
                {rec.ReviewCount && (
                  <p className="review-count">Reviews: {rec.ReviewCount}</p>
                )}
              </div>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

export default Recommendations;
