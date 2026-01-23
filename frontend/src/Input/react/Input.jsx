import Brand from "./Brand"
import Model from "./Model"
import Range from "./Range"
import Condition from "./Condition"
import Search from "./Search"

function Input(){
    return(
        <div id="input">
            <Brand />
            <Model />
            <Range />
            <Condition />
            <Search />
        </div>
    )
}

export default Input;