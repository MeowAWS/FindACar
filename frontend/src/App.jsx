import { useState, useEffect } from 'react'
import './App.css'
import Displayer from './Cards/react/Displayer'
import Input from "./Input/react/Input"

function App() {
  const [count, setCount] = useState(0)

  const [selectedBrand, setSelectedBrand] = useState("");
  const [selectedModel, setSelectedModel] = useState("");
  const [selectedRange, setSelectedRange] = useState("");
  const [selectedCondition, setSelectedCondition] = useState("");

  const [allSelected, setAllSelected] = useState(false);
  const [searchPressed, setSearchPressed] = useState(false);

  useEffect(() => {
    // Check if all variables have a value (are not "")
    if (selectedBrand && selectedModel && selectedRange && selectedCondition) {
        setAllSelected(true);
    } else {
        setAllSelected(false);
    }
  }, [selectedBrand, selectedModel, selectedRange, selectedCondition]);

  const handleSearchTrigger = () => {
    setSearchPressed(true);
  };

  const turnSearchOff = () => {
    setSearchPressed(false);
  };

  return (
    <>
      <div>

          <Input 
            setSelectedBrand={setSelectedBrand} 
            setSelectedModel={setSelectedModel} 
            setSelectedRange={setSelectedRange} 
            setSelectedCondition={setSelectedCondition} 
            allSelected={allSelected} 
            selectedBrand={selectedBrand}
            onSearchClick={handleSearchTrigger}
          />


          <Displayer 
            brand={selectedBrand} 
            model={selectedModel} 
            price={selectedRange} 
            condition={selectedCondition} 
            searchPressed={searchPressed}
            turnSearchOff={turnSearchOff}
          />
      </div>
    </>
  )
}

export default App
