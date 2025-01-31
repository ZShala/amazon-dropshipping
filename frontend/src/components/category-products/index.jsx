import React, { useState, useEffect } from 'react';
import ProductCard from '../product-card';
import ProductSkeleton from '../product-skeleton';
import CategoryFilter from '../category-filter';
import './category-products.styles.scss';

const CategoryProducts = ({ categoryType }) => {
    const [allProducts, setAllProducts] = useState([]);
    const [displayedProducts, setDisplayedProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedType, setSelectedType] = useState('all');
    const [productTypes, setProductTypes] = useState([]);
    const [page, setPage] = useState(1);
    const productsPerPage = 20;
    const [selectedFilter, setSelectedFilter] = useState('all');

    // Funksion për të marrë produktet nga cache
    const getFromCache = (category) => {
        try {
            const cached = localStorage.getItem(`products_${category}`);
            if (cached) {
                const { data, timestamp } = JSON.parse(cached);
                // Kontrollojmë nëse cache është më i vjetër se 1 orë
                if (Date.now() - timestamp < 3600000) {
                    return data;
                }
                // Fshijmë cache-in e vjetër
                localStorage.removeItem(`products_${category}`);
            }
        } catch (error) {
            console.error('Cache error:', error);
        }
        return null;
    };

    // Funksion për të ruajtur produktet në cache
    const saveToCache = (category, products) => {
        try {
            const cacheData = {
                data: products,
                timestamp: Date.now()
            };
            localStorage.setItem(`products_${category}`, JSON.stringify(cacheData));
        } catch (error) {
            console.error('Cache save error:', error);
        }
    };

    const fetchProducts = async () => {
        try {
            setLoading(true);
            setError(null);

            // Kontrollojmë fillimisht cache-in
            const cachedProducts = getFromCache(categoryType.toLowerCase());
            if (cachedProducts) {
                console.log('Loading from cache');
                setAllProducts(cachedProducts);
                setDisplayedProducts(cachedProducts.slice(0, productsPerPage));
                const types = [...new Set(cachedProducts.map(p => p.ProductType))];
                setProductTypes(types);
                setLoading(false);
                return;
            }

            // Nëse nuk ka cache, bëjmë fetch nga API
            const url = `http://localhost:5001/api/${categoryType.toLowerCase()}`;
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            
            const data = await response.json();

            if (data && data.products) {
                const products = data.products;
                // Ruajmë në cache
                saveToCache(categoryType.toLowerCase(), products);
                
                setAllProducts(products);
                setDisplayedProducts(products.slice(0, productsPerPage));
                const types = [...new Set(products.map(p => p.ProductType))];
                setProductTypes(types);
            } else {
                throw new Error('Invalid response format from server');
            }
            
        } catch (err) {
            console.error('Error details:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const getSubcategoryKeywords = (subcategory) => {
        const subcategoryMap = {
            // Makeup
            'Eye Makeup': [
                'eye', 'mascara', 'eyeliner', 'kajal', 'shadow', 
                'eyeshadow', 'eye liner', 'eye shadow', 'eye makeup'
            ],
            'Lip Products': [
                'lip', 'lipstick', 'gloss', 'lip gloss', 'lip stick',
                'lipgloss', 'lip color', 'lip colour', 'lip stain',
                'lip liner', 'lipliner', 'lip balm', 'lipbalm'
            ],
            'Face Makeup': [
                'foundation', 'concealer', 'powder', 'blush', 'compact',
                'face powder', 'bb cream', 'cc cream', 'primer',
                'bronzer', 'highlighter', 'contour', 'face makeup'
            ],
            'Nail Products': [
                'nail', 'polish', 'lacquer', 'nail polish',
                'nail color', 'nail colour', 'nail care', 'nail art'
            ],

            // Skincare
            'Cleansers': [
                'cleanser', 'face wash', 'facial wash', 'cleaning',
                'cleansing', 'face cleanser', 'facial cleanser'
            ],
            'Moisturizers': [
                'moisturizer', 'cream', 'lotion', 'hydrating',
                'moisturizing', 'face cream', 'facial cream',
                'day cream', 'night cream', 'hydration'
            ],
            'Treatments': [
                'serum', 'treatment', 'essence', 'ampoule',
                'face serum', 'facial serum', 'skin treatment'
            ],
            'Masks': [
                'mask', 'pack', 'peel', 'face mask',
                'facial mask', 'sheet mask', 'clay mask'
            ],
            'Toners': [
                'toner', 'mist', 'essence', 'facial toner',
                'face toner', 'skin toner'
            ],

            // Haircare
            'Shampoos': [
                'shampoo', 'hair wash', 'hair cleaner',
                'hair cleanser', 'hair cleaning'
            ],
            'Conditioners': [
                'conditioner', 'conditioning', 'hair conditioner',
                'deep conditioner', 'leave-in conditioner'
            ],
            'Hair Treatments': [
                'hair treatment', 'hair mask', 'hair oil', 'hair serum',
                'hair care', 'scalp treatment', 'hair therapy'
            ],

            // Fragrance
            'Perfumes': [
                'perfume', 'parfum', 'eau de', 'fragrance',
                'eau de parfum', 'eau de toilette', 'edt', 'edp'
            ],
            'Body Sprays': [
                'body spray', 'body mist', 'body fragrance',
                'deodorant spray', 'fragrance mist'
            ],
            'Deodorants': [
                'deodorant', 'antiperspirant', 'anti-perspirant',
                'deo', 'roll-on'
            ]
        };
        
        return subcategoryMap[subcategory] || [];
    };

    const filterProductByType = (product, type) => {
        if (type === 'All Products' || type === 'all') {
            return true;
        }

        const productType = product.ProductType.toLowerCase();
        const keywords = getSubcategoryKeywords(type);
        
        return keywords.some(keyword => {
            const normalizedKeyword = keyword.toLowerCase().trim();
            return productType.includes(normalizedKeyword) ||
                   normalizedKeyword.split(' ').every(word => 
                       productType.includes(word.toLowerCase())
                   );
        });
    };

    // Përditësojmë filtrimin kur ndryshon tipi i zgjedhur
    useEffect(() => {
        if (allProducts.length > 0) {
            const filtered = allProducts.filter(p => filterProductByType(p, selectedType));
            setDisplayedProducts(filtered.slice(0, page * productsPerPage));
        }
    }, [selectedType, allProducts, page]);

    // Përditësojmë loadMore për të përdorur produktet e filtruara
    const loadMore = () => {
        const nextPage = page + 1;
        const filteredProducts = allProducts.filter(p => filterProductByType(p, selectedType));
        const start = 0;
        const end = nextPage * productsPerPage;
        
        setDisplayedProducts(filteredProducts.slice(start, end));
        setPage(nextPage);
    };

    // Përditësojmë hasMore për të përdorur produktet e filtruara
    const hasMore = displayedProducts.length < 
        allProducts.filter(p => filterProductByType(p, selectedType)).length;

    // Përditësojmë filteredProducts
    const filteredProducts = displayedProducts;

    // Shtojmë një efekt për të pastruar cache-in e vjetër
    useEffect(() => {
        const cleanOldCache = () => {
            try {
                const now = Date.now();
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    if (key.startsWith('products_')) {
                        const cached = JSON.parse(localStorage.getItem(key));
                        if (now - cached.timestamp > 3600000) { // 1 orë
                            localStorage.removeItem(key);
                        }
                    }
                }
            } catch (error) {
                console.error('Cache cleanup error:', error);
            }
        };

        cleanOldCache();
    }, []);

    const groupProductTypes = (types) => {
        const grouped = new Map();
        
        // Definojmë nënkategoritë për secilën kategori kryesore
        const categorySubgroups = {
            'makeup': [
                { name: 'All Products', keywords: [] },
                { name: 'Eye Makeup', keywords: ['eye', 'mascara', 'eyeliner', 'kajal', 'shadow'] },
                { name: 'Lip Products', keywords: ['lip', 'lipstick', 'gloss'] },
                { name: 'Face Makeup', keywords: ['foundation', 'concealer', 'powder', 'blush'] },
                { name: 'Nail Products', keywords: ['nail', 'polish'] }
            ],
            'skincare': [
                { name: 'All Products', keywords: [] },
                { name: 'Cleansers', keywords: ['cleanser', 'wash'] },
                { name: 'Moisturizers', keywords: ['moisturizer', 'cream', 'lotion'] },
                { name: 'Treatments', keywords: ['serum', 'treatment'] },
                { name: 'Masks', keywords: ['mask', 'pack'] },
                { name: 'Toners', keywords: ['toner', 'mist', 'essence'] }
            ],
            'haircare': [
                { name: 'All Products', keywords: [] },
                { name: 'Shampoos', keywords: ['shampoo', 'wash'] },
                { name: 'Conditioners', keywords: ['conditioner', 'conditioning'] },
                { name: 'Hair Treatments', keywords: ['treatment', 'mask', 'oil', 'serum'] }
            ],
            'fragrance': [
                { name: 'All Products', keywords: [] },
                { name: 'Perfumes', keywords: ['perfume', 'parfum', 'eau de'] },
                { name: 'Body Sprays', keywords: ['body spray', 'mist'] },
                { name: 'Deodorants', keywords: ['deodorant', 'antiperspirant'] }
            ],
            'miscellaneous': [
                { name: 'All Products', keywords: [] },
                { name: 'Tools', keywords: ['tool', 'brush', 'applicator'] },
                { name: 'Accessories', keywords: ['accessory', 'accessories'] },
                { name: 'Sets & Kits', keywords: ['kit', 'set', 'collection'] }
            ]
        };

        const currentCategory = categoryType ? categoryType.toLowerCase() : 'all';
        const subgroups = categorySubgroups[currentCategory] || [{ name: 'All Products', keywords: [] }];

        // Shtojmë secilën nënkategori
        subgroups.forEach(subgroup => {
            const matchingProducts = subgroup.name === 'All Products' 
                ? types 
                : types.filter(type => {
                    const productType = type.toLowerCase();
                    return subgroup.keywords.some(keyword => 
                        productType.includes(keyword.toLowerCase())
                    );
                });

            if (matchingProducts.length > 0 || subgroup.name === 'All Products') {
                grouped.set(subgroup.name, {
                    name: subgroup.name,
                    count: matchingProducts.length,
                    types: matchingProducts
                });
            }
        });

        // Kthejmë array të sortuar, me "All Products" në fillim
        const groupedArray = Array.from(grouped.values());
        const allProducts = groupedArray.find(g => g.name === 'All Products');
        const otherGroups = groupedArray.filter(g => g.name !== 'All Products')
            .sort((a, b) => b.count - a.count);

        return allProducts ? [allProducts, ...otherGroups] : otherGroups;
    };

    useEffect(() => {
        const testConnection = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/test');
                const data = await response.json();
                console.log('Backend connection:', data.message);
            } catch (err) {
                console.error('Backend connection failed:', err);
            }
        };
        
        testConnection();
    }, []);

    const renderSkeletons = () => {
        return Array(12).fill(0).map((_, index) => (
            <ProductSkeleton key={index} />
        ));
    };

    // Shtojmë efektin për të thirrur fetchProducts kur ndryshon kategoria
    useEffect(() => {
        setPage(1);
        setAllProducts([]);
        setDisplayedProducts([]);
        setProductTypes([]);
        setSelectedType('all');
        fetchProducts();
    }, [categoryType]);

    if (loading && displayedProducts.length === 0) {
        return (
            <div className="category-products">
                <h2>{categoryType} Products</h2>
                <div className="products-grid">
                    {renderSkeletons()}
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="category-products">
                <div className="error">
                    <h2>Error Loading Products</h2>
                    <p>{error}</p>
                    <button onClick={() => fetchProducts()}>
                        Try Again
                    </button>
                </div>
            </div>
        );
    }

    if (displayedProducts.length > 0) {
        return (
            <div className="category-products">
                <div className="subheader">
                    <div className="filters">
                        <button 
                            className={`filter-button ${selectedFilter === 'rating' ? 'selected' : ''}`}
                            onClick={() => setSelectedFilter('rating')}
                        >
                            Top Rated
                        </button>
                        <button 
                            className={`filter-button ${selectedFilter === 'reviews' ? 'selected' : ''}`}
                            onClick={() => setSelectedFilter('reviews')}
                        >
                            Most Reviewed
                        </button>
                    </div>
                </div>

                <h2>{categoryType} Products</h2>
                
                <CategoryFilter 
                    productTypes={productTypes}
                    selectedType={selectedType}
                    onTypeSelect={setSelectedType}
                    categoryType={categoryType.toLowerCase()}
                    onGroupProducts={groupProductTypes}
                />

                <div className="products-grid">
                    {filteredProducts.map(product => (
                        <ProductCard 
                            key={product.ProductId}
                            product={product}
                        />
                    ))}
                </div>

                {hasMore && !loading && (
                    <div className="load-more-container">
                        <button 
                            className="load-more-button"
                            onClick={loadMore}
                        >
                            <span>Load More Products</span>
                            <span className="products-count">
                                {allProducts.length - displayedProducts.length} more
                            </span>
                        </button>
                        
                        <div className="products-progress">
                            <div className="progress-bar">
                                <div 
                                    className="progress" 
                                    style={{ 
                                        width: `${(displayedProducts.length / allProducts.length) * 100}%` 
                                    }}
                                />
                            </div>
                            <span>
                                Showing {displayedProducts.length} of {allProducts.length} products
                            </span>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    return (
        <div className="category-products">
            <h2>{categoryType} Products</h2>
            <div className="no-products">
                <p>No products found in this category.</p>
            </div>
        </div>
    );
};

export default CategoryProducts; 