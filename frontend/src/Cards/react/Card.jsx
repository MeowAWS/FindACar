import '../styles/Card.css'


function Card({ car }) {
    return (
        <div className="card">
            <img src={car.image} alt={`${car.brand} ${car.name}`} className="card-image" />
            <div className="card-info">
                <h3>{car.brand} {car.name}</h3>
                <p>Price: {car.price}</p>
                <p>Condition: {car.condition}</p>
                <a href={car.url} target="_blank" rel="noopener noreferrer">View Ad</a>
            </div>
        </div>
    );
}

export default Card;
