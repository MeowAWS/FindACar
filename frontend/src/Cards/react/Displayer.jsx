import { useEffect, useState } from "react";
import Card from "./Card";
import "../styles/Displayer.css";

function Displayer({ brand, model, price, condition, searchPressed, turnSearchOff }) {

    const [cars, setCars] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!searchPressed) return;

        setLoading(true);

        // Correct GET request to FastAPI
        fetch(`http://localhost:8000/search?brand=${brand}&name=${model}&price=${price}&condition=${condition}`)
            .then((res) => res.json())
            .then((data) => {
                setCars(data.results); // Use .results because FastAPI returns { results: [...] }
                setLoading(false);
                turnSearchOff(); // Reset search state
            })
            .catch((err) => {
                console.error(err);
                setLoading(false);
                turnSearchOff();
            });

    }, [searchPressed]);

    if (!searchPressed && cars.length === 0) return null;

    return (
        <div className="displayer">
            {loading && <p>Loading cars...</p>}

            {!loading && cars.length === 0 && (
                <p>No cars found</p>
            )}

            {!loading &&
                cars.map((car, index) => (
                    <Card key={index} car={car} />
                ))
            }
        </div>
    );
}

export default Displayer;
