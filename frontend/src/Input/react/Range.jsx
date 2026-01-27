import { useState } from "react";

function Range({ onRangeChange }) {
    const [value, setValue] = useState("");

    const handleChange = (e) => {
        const val = e.target.value;
        // Optional: Only allow numbers
        if (/^\d*$/.test(val)) {
            setValue(val);
            onRangeChange(val); // Send value to parent
        }
    };

    return (
        <div className="inputSet" id="rangeDiv">
            <label htmlFor="range">Max Price (in Lakh):</label>
            <input
                id="range"
                type="text"
                className="inputBoxes"
                placeholder="Enter max price"
                value={value}
                onChange={handleChange}
            />
        </div>
    );
}

export default Range;
