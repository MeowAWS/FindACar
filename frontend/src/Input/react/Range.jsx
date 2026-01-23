function Range(){
    return(
        <div className="inputSet" id="rangeDiv">
            <label for="range">Price Range</label>
            <input className="inputBoxes" type="number" placeholder="$$-$$" id="range"/>
        </div>
    )
}

export default Range;