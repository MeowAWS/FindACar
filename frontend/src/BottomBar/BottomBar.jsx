import leftLogo from "../../assets/pakwheels.png";
import "./BottomBar.css"

function BottomBar() {
    return (
        <div id="bottombar">
            <img src={leftLogo} alt="PakWheels" id="pakwheels" />
            <span id="left-text" className="crystal-text">An Extension of PakWheels</span>
        </div>
    )
}

export default BottomBar;