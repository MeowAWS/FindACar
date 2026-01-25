import Card from "./Card";
import "../styles/Displayer.css"

function Displayer({brand, model, price, condition, searchPressed, turnSearchOff}) {

    
    //WHEN YOU ARE DONE, JUST CALL turnSearchOff()

    // If search hasn't been pressed, don't show anything
    if (!searchPressed) {
        return null; 
    }

    return (
        <Card />
    );
}

export default Displayer;