import { useState, useEffect } from "react";

function Model({ models, selectedModel, onModelChange }) {
    const [inputValue, setInputValue] = useState("");
    const [filteredModels, setFilteredModels] = useState([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const [focusedIndex, setFocusedIndex] = useState(-1);

    useEffect(() => {
        setInputValue(selectedModel || ""); // reset when brand changes
        setShowDropdown(false);
    }, [selectedModel]);

    const handleInputChange = (e) => {
        const val = e.target.value;
        setInputValue(val);
        onModelChange(val);

        if (val.length > 0) {
            const filtered = models.filter(m => m.toLowerCase().includes(val.toLowerCase()));
            setFilteredModels(filtered);
            setShowDropdown(true);
            setFocusedIndex(-1);
        } else {
            setShowDropdown(false);
        }
    };

    const handleKeyDown = (e) => {
        if (!showDropdown) return;

        if (e.key === "ArrowDown") {
            setFocusedIndex(prev => Math.min(prev + 1, filteredModels.length - 1));
        } else if (e.key === "ArrowUp") {
            setFocusedIndex(prev => Math.max(prev - 1, 0));
        } else if (e.key === "Enter" && focusedIndex !== -1) {
            e.preventDefault();
            selectModel(filteredModels[focusedIndex]);
        } else if (e.key === "Escape") {
            setShowDropdown(false);
        }
    };

    // Make sure onModelChange is called on typing AND selecting
    const selectModel = (model) => {
        setInputValue(model);
        setShowDropdown(false);
        setFocusedIndex(-1);
        onModelChange(model); // important: send selected value to parent
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
