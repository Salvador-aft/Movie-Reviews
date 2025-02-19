import React from "react";
import Header from "../components/Header";
import TiltedCarousel from "../components/Carousel";

const Home: React.FC = () => {
  return (
    <div className="min-h-screen" style={{ backgroundColor: "#01070C" }}>
      <Header />

      <div className="relative w-full flex justify-center items-center min-h-[calc(100vh-80px)]">
        <TiltedCarousel />
      </div>
    </div>
  );
};

export default Home;
