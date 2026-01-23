import { useState } from 'react'
import './App.css'
import Displayer from './Cards/react/Displayer'
import Input from "./Input/react/Input"

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
          <Input />
          <Displayer />
      </div>
    </>
  )
}

export default App
