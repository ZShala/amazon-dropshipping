import React from 'react';
import './category-filter.styles.scss';

const CategoryFilter = ({ productTypes, selectedType, onTypeSelect, categoryType, onGroupProducts }) => {
    const groupedTypes = onGroupProducts(productTypes);

    return (
        <div className="category-filter">
            <div className="filter-options">
                {groupedTypes.map(group => (
                    <button
                        key={group.name}
                        className={`filter-option ${
                            (selectedType === group.name || 
                             (group.name === 'All Products' && selectedType === 'all')
                            ) ? 'active' : ''
                        }`}
                        onClick={() => onTypeSelect(group.name)}
                    >
                        {group.name}
                        <span className="count">({group.count})</span>
                    </button>
                ))}
            </div>
        </div>
    );
};

export default CategoryFilter; 