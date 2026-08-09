import "./App.css";

import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Hardware from "./pages/Hardware";
import HardwareProfile from "./pages/HardwareProfile";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/hardware" element={<Hardware />} />
      <Route
        path="/hardware/:variantId"
        element={<HardwareProfile />}
      />
    </Routes>
  );
}

export default App;