import { useEffect, useState } from "react";

function Condition({ onConditionChange }) {
    const [conditions, setConditions] = useState([]);
    const [selected, setSelected] = useState("");

    const API_URL = import.meta.env.VITE_API_URL;

    useEffect(() => {
        fetch(`${API_URL}conditions`)
            .then((res) => res.json())
            .then((data) => setConditions(data.conditions))
            .catch((err) => console.error(err));
    }, []);

    const handleChange = (e) => {
        setSelected(e.target.value);
        onConditionChange(e.target.value);
    };

    return (
        <div className="inputSet" id="conditionDiv">
            <label htmlFor="condition">Select Condition</label>
            <select
                className="inputBoxes"
                id="condition"
                value={selected}
                onChange={handleChange}
            >
                <option value="" disabled>Select condition</option>
                {conditions.map((cond, idx) => (
                    <option key={idx} value={cond}>{cond}</option>
                ))}
            </select>
        </div>
    );
}

export default Condition;
