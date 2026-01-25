function Condition({onConditionChange}){

    const handleChange = (e) => {
        onConditionChange(e.target.value);
    };

    return(
        <div className="inputSet" id="conditionDiv">
            <label htmlFor="condition">Select Condition</label>
    
            <select className="inputBoxes" id="condition" name="condition" onChange={handleChange}>
                <option value="" disabled selected>Condition</option>
                <option value="new">New</option>
                <option value="used">Used</option>
            </select>
        </div>
    )
}

export default Condition;