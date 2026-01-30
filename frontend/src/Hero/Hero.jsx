import { useState, useEffect } from "react";
import "./Hero.css";

function Hero({ searchButtonOn }) {
  const [showContent, setShowContent] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  useEffect(() => {
    setShowContent(true);
  }, []);

  useEffect(() => {
    if (searchButtonOn && !hasSearched) {
      setHasSearched(true);
    }
  }, [searchButtonOn]);

  return (
    <div className={`hero-wrapper ${hasSearched ? "hidden" : ""}`}>
      <div id="herodiv" className={`fade-in ${showContent ? "visible" : ""}`}>
        <h1 id="description">AI Based Car Rater</h1>
        <h2 id="textBelow">Condition Analysis using a machine learning model</h2>
      </div>
    </div>
  );
}


export default Hero;
