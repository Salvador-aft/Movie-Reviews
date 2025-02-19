import { BrowserRouter } from "react-router-dom";
import Home from "./pages/Home";
import React from "react";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Home />
    </BrowserRouter>
  );
};

export default App;