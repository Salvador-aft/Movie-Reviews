import React, { useState, useEffect } from "react";
import Block from "../components/Block";

interface Movie {
  title: string;
  genre: string;
  duration: number;
  release_date: string;
  is_upcoming: boolean;
  rating: number;
  poster_url: string;
  trailer_url: string;
  overview: string;
}

const TiltedCarousel: React.FC = () => {
  const [activeIndex, setActiveIndex] = useState(1);
  const [animating, setAnimating] = useState(false);
  const [delayedRotate, setDelayedRotate] = useState(false);
  const [movies, setMovies] = useState<Movie[]>([]);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/top-rated-movies/");
        if (!response.ok) {
          throw new Error("Error al obtener los datos");
        }
        const data = await response.json();
        setMovies(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchMovies();
  }, []);

  const nextIndex = (activeIndex + 1) % movies.length;
  const prevIndex = (activeIndex - 1 + movies.length) % movies.length;
  const prevPrevIndex = (activeIndex - 2 + movies.length) % movies.length;
  const nextNextIndex = (activeIndex + 2) % movies.length;

  const handleSelect = (index: number) => {
    if (animating) return;
    setAnimating(true);
    setDelayedRotate(false);
    setTimeout(() => {
      setActiveIndex(index);
      setTimeout(() => {
        setAnimating(false);
        setDelayedRotate(true);
      }, 500);
    }, 500);
  };

  if (movies.length === 0) {
    return <div>Cargando películas...</div>;
  }

  return (
    <div className="relative w-screen h-[calc(100vh-80px)] flex justify-center items-center overflow-hidden z-10">
      <div className="relative w-full h-full flex justify-center items-center overflow-hidden">
        {[prevPrevIndex, prevIndex, activeIndex, nextIndex, nextNextIndex].map((index) => {
          const movie = movies[index];
          let width = "45vw";
          let translateX: string = "0";
          let scale = 0.75;
          let rotateY = 0;
          let opacity = 0;
          let transition = "transform 0.5s ease-in-out, opacity 0.5s ease-in-out";

          if (index === activeIndex) {
            width = "45vw";
            scale = 1;
            opacity = 1;
          } else if (index === prevIndex) {
            translateX = "-50vw";
            opacity = 1;
          } else if (index === nextIndex) {
            translateX = "50vw";
            opacity = 1;
          }

          if (index !== activeIndex && delayedRotate) {
            rotateY = index === prevIndex ? 25 : index === nextIndex ? -25 : 0;
            transition += ", rotateY 0.3s ease-in-out";
          }

          return (
            <Block
              key={movie.title}
              id={index + 1}
              movie={movie}
              onClick={() => handleSelect(index)}
              className="absolute shadow-2xl rounded-lg flex justify-center items-center cursor-pointer"
              style={{
                width,
                transform: `translateX(${translateX}) scale(${scale}) perspective(1500px) rotateY(${rotateY}deg)`,
                opacity,
                transition,
                left: "50%",
                top: "50%",
                marginLeft: `calc(-${width} / 2)`,
                marginTop: "-25vh",
                height: "50vh",
              }}
            />
          );
        })}
      </div>
    </div>
  );
};

export default TiltedCarousel;