import Image from "./Image"
import Info from "./Info"
import Button from "./Button"
import "../styles/Card.css"

function Card(){
    return (
        <div id="card">
            <Image url="https://cache2.pakwheels.com/ad_pictures/1190/honda-vezel-hybrid-z-honda-sensing-2019-119065443.webp"/> 
            <Info carName="Bonda Vezel" price="2300000" condition="A+"/> 
            <Button url="https://www.pakwheels.com/used-cars/honda-vezel-2019-for-sale-in-lahore-9918177"/>
        </div>
    )
}

export default Card