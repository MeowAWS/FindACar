import Brand from "./Brand"
import Model from "./Model"
import Range from "./Range"
import Condition from "./Condition"
import Search from "./Search"
import {useState, useEffect} from 'react'

function Input({ setSelectedBrand, selectedBrand, setSelectedModel, setSelectedRange, setSelectedCondition, allSelected, onSearchClick }){
   

    return(
        <div id="input">
            <Brand onBrandChange={setSelectedBrand} />
            <Model brand={selectedBrand} onModelChange={setSelectedModel} />
            <Range onRangeChange={setSelectedRange} />
            <Condition onConditionChange={setSelectedCondition} />
            <Search allSelected={allSelected} onSearchClick={onSearchClick}/>
        </div>
    )
}

export default Input;