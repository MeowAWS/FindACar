import { useState } from 'react'
import './App.css'
import Card from "./Cards/react/Card"

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
          <Card />
      </div>
    </>
  )
}

export default App
