function Range({ onRangeChange }){
     const handleChange = (e) => {
        onRangeChange(e.target.value);
    };
    return(
        <div className="inputSet" id="rangeDiv" onChange={handleChange}>
            <label htmlFor="range">Price Range</label>
            <input className="inputBoxes" type="number" placeholder="$$-$$" id="range"/>
        </div>
    )
}

export default Range;