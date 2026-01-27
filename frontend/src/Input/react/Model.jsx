import { useState, useEffect } from 'react';

function Model({ brand, onModelChange }) {
    const [modelList, setModelList] = useState([]);
    const [filteredModels, setFilteredModels] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [showDropdown, setShowDropdown] = useState(false);
    const [focusedIndex, setFocusedIndex] = useState(-1); // Track arrow key position

    const API_URL = import.meta.env.VITE_API_URL;

    useEffect(() => {
        const fetchData = async () => {
            if (!brand) return;
            try {
                const response = await fetch(`${API_URL}names?brand=${brand}`);
                const result = await response.json();
                setModelList(result.Car_name || []);
            } catch (error) {
                console.log("Fetch Error: ", error);
            }
        };
        fetchData();
        setInputValue("");
    }, [brand, API_URL]);

    const handleInputChange = (e) => {
        const val = e.target.value;
        setInputValue(val);
        onModelChange(val); //sends value to parent
        if (val.length > 0) {
            const filtered = modelList.filter(model =>
                model.toLowerCase().includes(val.toLowerCase())
            );
            setFilteredModels(filtered);
            setShowDropdown(true);
            setFocusedIndex(-1); // Reset focus when typing
        } else {
            setShowDropdown(false);
        }
    };

    const handleKeyDown = (e) => {
        if (!showDropdown) return;

        if (e.key === "ArrowDown") {
            setFocusedIndex(prev => (prev < filteredModels.length - 1 ? prev + 1 : prev));
        } else if (e.key === "ArrowUp") {
            setFocusedIndex(prev => (prev > 0 ? prev - 1 : prev));
        } else if (e.key === "Enter" && focusedIndex !== -1) {
            e.preventDefault();
            selectModel(filteredModels[focusedIndex]);
        } else if (e.key === "Escape") {
            setShowDropdown(false);
        }
    };

    const selectModel = (model) => {
        setInputValue(model);
        setShowDropdown(false);
        setFocusedIndex(-1);
        onModelChange(model); // send selected model to parent
    };


    return (
        <div className="inputSet" id="modelDiv" onKeyDown={handleKeyDown}>
            <label htmlFor="model">Select Model</label>
            <input
                className="inputBoxes"
                type="text"
                placeholder="Type to search..."
                value={inputValue}
                onChange={handleInputChange}
                autoComplete="off"
            />

            {showDropdown && filteredModels.length > 0 && (
                <ul className="customDropdown">
                    {filteredModels.map((model, index) => (
                        <li
                            key={index}
                            onClick={() => selectModel(model)}
                            className={index === focusedIndex ? "activeOption" : ""}
                        >
                            {model}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default Model;