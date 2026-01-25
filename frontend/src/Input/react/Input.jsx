import Brand from "./Brand"
import Model from "./Model"
import Range from "./Range"
import Condition from "./Condition"
import Search from "./Search"
import {useState} from 'react'

function Input(){
    const [selectedBrand, setSelectedBrand] = useState("");
    return(
        <div id="input">
            <Brand onBrandChange={setSelectedBrand} />
            <Model brand={selectedBrand}/>
            <Range />
            <Condition />
            <Search />
        </div>
    )
}

export default Input;