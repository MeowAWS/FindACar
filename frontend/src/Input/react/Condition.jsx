function Condition({onConditionChange}){

    const handleChange = (e) => {
        onConditionChange(e.target.value);
    };

    return(
        <div className="inputSet" id="conditionDiv">
            <label htmlFor="condition">Select Condition</label>
    
            <select className="inputBoxes" id="condition" name="condition" onChange={handleChange}>
                <option value="" disabled selected>Condition</option>
                <option value="A+">A+</option>
                <option value="A">A</option>
                <option value="B+">B+</option>
                <option value="B">B</option>
                <option value="C+">C+</option>
                <option value="C">C</option>
            </select>
        </div>
    )
}

export default Condition;