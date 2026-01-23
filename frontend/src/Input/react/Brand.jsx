import "../styles/styles.css"

function Brand(){
    return(
        <div className="inputSet" id="brandDiv">
            <label for="brand">Select Brand</label>
    
            <select className="inputBoxes" id="brand" name="brand">
                <option value="" disabled selected>Brand name</option>
                <option value="suzuki">Suzuki</option>
                <option value="honda">Honda</option>
                <option value="toyota">Toyota</option>
            </select>
        </div>
    )
}

export default Brand;