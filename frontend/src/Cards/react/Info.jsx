import "../styles/Info.css"

function Info({carName, price, condition}) {
    return(
        <div id="info">
            <p id="carName">{carName}</p>
            <p id="price">{price}</p>
            <p id="condition">{condition}</p>
        </div>
    )
}

export default Info;