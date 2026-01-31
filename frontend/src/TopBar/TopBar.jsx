import "./TopBar.css";
import logo from "../../assets/logoTopBar.png";
import leftLogo from "../../assets/pakwheels.png";

function TopBar() {
    return (
        <div id="topbar">

            {/* LEFT LOGO + PHRASE */}
            <div id="left-container">
                <img src={leftLogo} alt="PakWheels" id="pakwheels" />
                <span id="left-text" className="crystal-text">An Extension of PakWheels</span>
            </div>

            {/* CENTER LOGO + FIND A CAR */}
            <div id="logo-container">
                <img src={logo} alt="Logo" id="logo" />
                <p id="findacar" className="crystal-text">
                    <a href="/" style={{ color: "inherit", textDecoration: "none" }}>
                        Find a Car
                    </a>
                </p>

            </div>

            {/* RIGHT CONTACT LINK */}
            <a href="mailto:msubhannoor24.07@gmail.com" id="contactUs" className="crystal-text">Contact Us</a>
        </div>
    );
}

export default TopBar;
