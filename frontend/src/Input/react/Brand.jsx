import "../styles/styles.css"
import {useState, useEffect} from 'react';


function Brand({onBrandChange}){

    const API_URL = import.meta.env.VITE_API_URL;
    const [brandList, setBrandList] = useState([]);
    
    const fetchData = async () => {
        try{
            const response = await fetch(API_URL + 'brands');
            if(!response.ok) throw new Error('Network Response was not ok');
            const result = await response.json();
            setBrandList(result.brands);
        }
        catch(error){
            console.log("Fetch Error: ", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleChange = (e) => {
        onBrandChange(e.target.value);
    };

    // Add this inside your Brand component
useEffect(() => {
    console.log("Updated brandList:", brandList);
}, [brandList]); // This runs every time carList changes

    return(
        <div className="inputSet" id="brandDiv">
            <label htmlFor="brand">Select Brand</label>
    
            <select className="inputBoxes" id="brand" name="brand" onChange={handleChange} defaultValue="">
                {/* Dynamically render options */}
                <option value="" disabled>Select a brand</option>
                {brandList.map((brand, index) => (
                    <option key={index} value={brand.toLowerCase()}>
                        {brand}
                    </option>
                ))}
            </select>
        </div>
    )
}

export default Brand;