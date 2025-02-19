import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCirclePlay } from "@fortawesome/free-solid-svg-icons";

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

interface BlockProps {
  id: number;
  movie: Movie;
  onClick: () => void;
  className?: string;
  style?: React.CSSProperties;
}

const Block: React.FC<BlockProps> = ({ movie, onClick, className, style }) => {
  const [imageError, setImageError] = useState(false);

  const handleTrailerClick = (event: React.MouseEvent) => {
    event.stopPropagation();
    window.open(movie.trailer_url, "_blank");
  };
  const renderStars = (rating: number) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span
          key={i}
          className={`text-2xl ${i <= rating ? "text-yellow-400" : "text-gray-600"}`}
        >
          ★
        </span>
      );
    }
    return stars;
  };

  return (
    <div
      className={`w-full h-[600px] shadow-2xl rounded-lg flex cursor-pointer overflow-hidden ${className}`}
      style={{ backgroundColor: "#13161E", ...style }}
      onClick={onClick}
    >

      <div className="w-2/5 h-full flex-shrink-0 p-6">
        <div className="w-full h-full rounded-lg overflow-hidden">
          {imageError ? (
            <div className="w-full h-full bg-gray-700 flex items-center justify-center">
              <p className="text-gray-400">Imagen no disponible</p>
            </div>
          ) : (
            <img
              src={movie.poster_url}
              alt={`Póster de ${movie.title}`}
              className="w-full h-full object-cover"
              onError={() => setImageError(true)}
            />
          )}
        </div>
      </div>

      <div className="w-3/5 h-full flex flex-col p-6">
        <div className="flex flex-col h-full justify-between">
          <div className="overflow-y-auto pr-4">
            <h1 className="text-2xl font-bold text-white mb-4">{movie.title}</h1>

            <div className="flex space-x-1 mb-6">
              {renderStars(movie.rating)}
            </div>

            <div className="space-y-2 mb-6">
              <p className="text-gray-400">
                <span className="font-semibold">Género:</span> {movie.genre}
              </p>
              <p className="text-gray-400">
                <span className="font-semibold">Duración:</span> {movie.duration} minutos
              </p>
              <p className="text-gray-400">
                <span className="font-semibold">Estreno:</span> {movie.release_date}
              </p>
            </div>

            <p className="text-gray-400 text-sm leading-relaxed">
              {movie.overview}
            </p>
          </div>

          <div className="border-t border-gray-700 pt-4 pb-0">
            <div className="flex justify-between items-center">
              <span className="text-white text-lg font-semibold">Watch Trailer</span>

              <button
                onClick={handleTrailerClick}
                className="flex items-center px-6 py-3 rounded-full text-white font-semibold"
                style={{
                  background: "linear-gradient(90deg, #963CAF, #C53ECE)",
                }}
              >
                Play Now
                <FontAwesomeIcon
                  icon={faCirclePlay}
                  className="ml-2 text-white text-xl"
                />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Block;