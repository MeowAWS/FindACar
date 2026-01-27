import { useState, useEffect } from "react";

// These are your individual components
import Brand from "./Brand";
import Model from "./Model";
import Range from "./Range";
import Condition from "./Condition";
import Search from "./Search";

function Input({
    setSelectedBrand,
    selectedBrand,
    selectedModel,
    setSelectedModel,
    setSelectedRange,
    setSelectedCondition,
    allSelected,
    onSearchClick,
}) {

    const [brands, setBrands] = useState([]);
    const [models, setModels] = useState([]);

    // Fetch all brands from backend on mount
    useEffect(() => {
        fetch("http://localhost:8000/brands")
            .then(res => res.json())
            .then(data => setBrands(data.brands))
            .catch(err => console.error(err));
    }, []);

    // Fetch models whenever brand changes
    useEffect(() => {
        if (!selectedBrand) {
            setModels([]); // reset models if no brand
            setSelectedModel(""); // reset selected model
            return;
        }

        fetch(`http://localhost:8000/names?brand=${selectedBrand}`)
            .then(res => res.json())
            .then(data => setModels(data.Car_name))
            .catch(err => console.error(err));
    }, [selectedBrand, setSelectedModel]);

    return (
        <div id="input">

            {/* Brand dropdown */}
            <Brand
                brands={brands}
                onBrandChange={setSelectedBrand}
                selectedBrand={selectedBrand}
            />
            <Model
                models={models}
                selectedModel={selectedModel}  // current value
                onModelChange={setSelectedModel} // setter function
            />
            <Condition
                onConditionChange={setSelectedCondition}
            />


            {/* Range slider or input */}
            <Range onRangeChange={setSelectedRange} />

            {/* Condition dropdown */}
            <Condition onConditionChange={setSelectedCondition} />

            {/* Search button */}
            <Search allSelected={allSelected} onSearchClick={onSearchClick} />

        </div>
    );
}

export default Input;
