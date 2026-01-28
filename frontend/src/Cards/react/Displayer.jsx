import { useEffect, useState } from "react";
import Card from "./Card";
import "../styles/Displayer.css";

function Displayer({ brand, model, price, condition, searchPressed, turnSearchOff }) {
    const [cars, setCars] = useState(() => {
        // Load saved cars from localStorage on initial render
        const savedCars = localStorage.getItem('searchResults');
        return savedCars ? JSON.parse(savedCars) : [];
    });
    const [loading, setLoading] = useState(false);
    const [hasSearched, setHasSearched] = useState(() => {
        // Load search state from localStorage
        const savedSearchState = localStorage.getItem('hasSearched');
        return savedSearchState === 'true';
    });

    useEffect(() => {
        if (!searchPressed) return;

        const fetchCars = async () => {
            setLoading(true);
            setHasSearched(true);
            try {
                const response = await fetch(
                    `http://localhost:8000/search?brand=${brand}&name=${model}&price=${price}&condition=${condition}`
                );
                const data = await response.json();
                const results = data.results || [];

                // Save results to state
                setCars(results);

                // Save results to localStorage
                localStorage.setItem('searchResults', JSON.stringify(results));
                localStorage.setItem('hasSearched', 'true');
            } catch (err) {
                console.error("Error fetching cars:", err);
                setCars([]);
                localStorage.setItem('searchResults', JSON.stringify([]));
            } finally {
                setLoading(false);
                turnSearchOff();
            }
        };

        fetchCars();
    }, [searchPressed, brand, model, price, condition, turnSearchOff]);

    // Don't render anything if never searched
    if (!hasSearched && cars.length === 0) return null;

    return (
        <div className="displayer-container">
            {loading && <div className="loading"></div>}

            {!loading && hasSearched && cars.length === 0 && (
                <div className="no-results">
                    <h3>No cars with the following condition in this price range found</h3>
                </div>
            )}

            {!loading && cars.length > 0 && (
                <div className="cards-grid">
                    {cars.map((car, index) => (
                        <Card key={car.id || index} car={car} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default Displayer;