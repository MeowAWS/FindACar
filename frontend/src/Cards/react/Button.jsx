import "../styles/Button.css"

function Button({url}){

    return(
        <div className="mybutton">
            <a id="pakwheelButton" href={url}>View on PakWheels</a>
        </div>
    )
}

export default Button;