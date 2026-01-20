import "../styles/Image.css"

function Image({url}){
    return (
        <div>
            <img src={url} alt="Image not available"></img>
        </div>
    )
}

export default Image;