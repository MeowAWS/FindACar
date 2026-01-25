function Search({ allSelected, onSearchClick }) {
    const handleClick = () => {
        if (allSelected && onSearchClick) {
            onSearchClick();
        }
    };

    return (
        <div className="inputSet">
            <button 
                id="search"
                className="inputBoxes"
                disabled={!allSelected}
                onClick={handleClick} // Calls our local handler
                style={{
                    color: "white",
                    fontWeight: "bold",
                    opacity: allSelected ? 1 : 0.4,
                    cursor: allSelected ? "pointer" : "not-allowed"
                }}
            >
                Search
            </button>
        </div>
    );
}

export default Search