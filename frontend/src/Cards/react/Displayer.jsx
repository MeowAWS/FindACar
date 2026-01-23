import Card from "./Card";
import "../styles/Displayer.css"

function Displayer({brand, name, price, condition}) {

    return(
        <div id="displayer">
            <Card />
        </div>
    )

}

export default Displayer;