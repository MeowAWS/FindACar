function Brand({ brands, onBrandChange, selectedBrand }) {
    return (
        <div className="brand-dropdown">
            <label htmlFor="brand-select">Brand:</label>
            <select
                id="brand-select"
                value={selectedBrand}
                onChange={(e) => onBrandChange(e.target.value)}
            >
                <option value="">Select Brand</option>
                {brands.map((brand, idx) => (
                    <option key={idx} value={brand}>
                        {brand}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default Brand;
