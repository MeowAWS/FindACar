import { useState, useEffect } from "react";
import Card from "./Card"; // assuming you have a Card component
import "../styles/Displayer.css"

function Displayer({ brand, model, price, condition, searchPressed, turnSearchOff }) {
    // Load saved cars from sessionStorage on initial render
    const [cars, setCars] = useState(() => {
        const savedCars = sessionStorage.getItem('searchResults');
        return savedCars ? JSON.parse(savedCars) : [];
    });

    const [loading, setLoading] = useState(false);

    // Load search state from sessionStorage
    const [hasSearched, setHasSearched] = useState(() => {
        const savedSearchState = sessionStorage.getItem('hasSearched');
        return savedSearchState === 'true';
    });

    const API_URL = import.meta.env.VITE_API_URL;

    useEffect(() => {
        if (!searchPressed) return;

        const fetchCars = async () => {
            setLoading(true);
            setHasSearched(true);
            try {
                const response = await fetch(
                    `${API_URL}search?brand=${brand}&name=${model}&price=${price}&condition=${condition}`
                );
                const data = await response.json();
                const results = data.results || [];

                // Save results to state
                setCars(results);

                // Save results to sessionStorage (only persists across refresh)
                sessionStorage.setItem('searchResults', JSON.stringify(results));
                sessionStorage.setItem('hasSearched', 'true');
            } catch (err) {
                console.error("Error fetching cars:", err);
                setCars([]);
                sessionStorage.setItem('searchResults', JSON.stringify([]));
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
