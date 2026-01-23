function Condition(){
    return(
        <div className="inputSet" id="conditionDiv">
            <label for="condition">Select Condition</label>
    
            <select className="inputBoxes" id="condition" name="condition">
                <option value="" disabled selected>Condition</option>
                <option value="new">New</option>
                <option value="used">Used</option>
            </select>
        </div>
    )
}

export default Condition;