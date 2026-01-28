import "../styles/Card.css";

function Card({ car }) {
    // Extract first letter of condition for badge
    const conditionLetter = car.condition ? car.condition.charAt(0).toUpperCase() : 'U';
    const conditionClass = car.condition && car.condition.toLowerCase() === 'used' ? 'used' : 'new';

    // Format price with commas
    const formatPrice = (price) => {
        if (!price) return 'N/A';
        // Remove any existing commas and convert to number
        const numPrice = typeof price === 'string' ? price.replace(/,/g, '') : price;
        // Add commas
        return numPrice.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    };

    return (
        <div className="card">
            <img src={car.image} alt={`${car.brand} ${car.name}`} className="card-image" />
            <div className="card-info">
                <div className={`condition-badge ${conditionClass}`}>
                    {conditionLetter}
                </div>
                <h3>{car.brand} {car.name}</h3>
                <p>PKR {formatPrice(car.price)}</p>
                <p>Condition: {car.condition}</p>
                <a href={car.url} target="_blank" rel="noopener noreferrer">View Ad</a>
            </div>
        </div>
    );
}

export default Card;