function Search({ allSelected, onSearchClick }) {
    return (
        <div className="inputSet" id="searchDiv">
            <button
                className="searchButton"
                disabled={!allSelected}  // only clickable if all inputs are selected
                onClick={onSearchClick}
            >
                Search
            </button>
        </div>
    );
}

export default Search;
