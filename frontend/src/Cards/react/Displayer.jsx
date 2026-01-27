import { useEffect, useState } from "react";
import Card from "./Card";
import "../styles/Displayer.css";

function Displayer({ brand, model, price, condition, searchPressed, turnSearchOff }) {
    const [cars, setCars] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!searchPressed) return;

        const fetchCars = async () => {
            setLoading(true);
            try {
                const response = await fetch(
                    `http://localhost:8000/search?brand=${brand}&name=${model}&price=${price}&condition=${condition}`
                );
                const data = await response.json();
                setCars(data.results || []);
            } catch (err) {
                console.error("Error fetching cars:", err);
                setCars([]);
            } finally {
                setLoading(false);
                turnSearchOff();
            }
        };

        fetchCars();
    }, [searchPressed, brand, model, price, condition, turnSearchOff]);

    if (!searchPressed && cars.length === 0) return null;

    return (
        <div className="displayer">
            {loading && <p>Loading cars...</p>}
            {!loading && searchPressed && cars.length === 0 && <p>No cars found.</p>}

            {!loading &&
                cars.map((car, index) => (
                    <Card key={car.id || index} car={car} />
                ))}
        </div>
    );
}

export default Displayer;
