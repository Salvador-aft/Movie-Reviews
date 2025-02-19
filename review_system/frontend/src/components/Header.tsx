import { Link } from "react-router-dom";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
import cinemaCameraIcon from "../assets/cinema-camera-icon.png";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="bg-black text-white w-full p-4 font-maven-pro" style={{ width: "100vw" }}>
      <div className="flex justify-between items-center max-w-7xl mx-auto">
        <div className="flex items-center">
          <img src={cinemaCameraIcon} alt="Cinema Camera Icon" className="w-8 h-8 mr-2" />
          <Link to="/" className="text-2xl font-bold">
            <span style={{ color: "#F06471" }}>Movie</span>
            <span> Hut</span>
          </Link>
        </div>

        <div className="flex items-center space-x-6">
          <nav className="hidden md:flex space-x-6">
            <Link to="/" className="hover:text-red-500 py-2 px-3">Home</Link>
            <Link to="/movies" className="hover:text-red-500 py-2 px-3">Movies</Link>
            <Link to="/books" className="hover:text-red-500 py-2 px-3">Books</Link>
          </nav>

          <div className="relative hidden md:flex items-center border border-gray-500 rounded-full px-3 py-1 w-64">
            <select className="bg-transparent text-white outline-none">
              <option>Movies</option>
              <option>Books</option>
            </select>
            <input
              type="text"
              placeholder="Search..."
              className="bg-transparent outline-none ml-2 flex-grow pr-8"
            />
            <button className="absolute right-1 bg-transparent border-none outline-none text-xs text-white hover:text-red-500 transition-colors p-2">
              <FontAwesomeIcon icon={faMagnifyingGlass} />
            </button>
          </div>

          <div className="flex items-center">
            <span className="mr-2 hidden sm:inline">Welcome Guest!</span>
            <Link to="/login" className="hover:text-red-500 py-2 px-3">Login</Link>
          </div>

          <button
            className="md:hidden ml-4 p-2"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            ☰
          </button>
        </div>
      </div>

      <nav className={`w-full md:hidden ${menuOpen ? "block" : "hidden"} mt-3`}>
        <Link to="/" className="hover:text-red-500 block py-2 px-4">Home</Link>
        <Link to="/movies" className="hover:text-red-500 block py-2 px-4">Movies</Link>
        <Link to="/books" className="hover:text-red-500 block py-2 px-4">Books</Link>
      </nav>
    </header>
  );
};

export default Header;