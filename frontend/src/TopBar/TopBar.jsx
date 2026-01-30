import "./TopBar.css"
import logo from "../../assets/logo1.jpeg"

function TopBar () {
    return (
        <div id="topbar">
            <div id="logo-container">
                <img src={logo} alt="Logo" id="logo" />
                <p id="findacar">Find a Car</p>
            </div>

            <a href="mailto:msubhannoor24.07@gmail.com">Contact Us</a>
        </div>
    )
}

export default TopBar;