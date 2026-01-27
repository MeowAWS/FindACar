import { useEffect, useState } from "react";

function Brand({ brands, selectedBrand, onBrandChange }) {
    const handleChange = (e) => {
        onBrandChange(e.target.value);
    };

    return (
        <div className="inputSet" id="brandDiv">
            <label htmlFor="brand">Select Brand</label>
            <select
                className="inputBoxes"
                id="brand"
                value={selectedBrand}
                onChange={handleChange}
            >
                <option value="">Select a brand</option>
                {brands.map((brand, index) => (
                    <option key={index} value={brand}>
                        {brand}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default Brand;
