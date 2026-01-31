import "./TopBar.css"
import logo from "../../assets/logoTopBar.png"
import leftLogo from "../../assets/pakwheels.png"

function TopBar() {
    return (
        <div id="topbar">


            <div id="left-container">
                <img src={leftLogo} alt="PakWheel" id="pakwheels" />
                <span id="left-text">An Extension of PakWheels</span>
            </div>

            <div id="logo-container">
                <img src={logo} alt="Logo" id="logo" />
                <p id="findacar">Find a Car</p>
            </div>

            <a href="mailto:msubhannoor24.07@gmail.com" id="contactUs">Contact Us</a>
        </div>
    )
}

export default TopBar;