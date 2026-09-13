import "./App.css";

import {
  Routes,
  Route,
} from "react-router-dom";

import Home from "./pages/Home";
import Hardware from "./pages/Hardware";
import HardwareProfile from "./pages/HardwareProfile";
import HardwareCompare from "./pages/HardwareCompare";
import HardwareCompareSelect from "./pages/HardwareCompareSelect";
import Admin from "./pages/Admin";


function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={<Home />}
      />

      <Route
        path="/hardware"
        element={<Hardware />}
      />

      <Route
        path="/hardware/:variantId"
        element={<HardwareProfile />}
      />

      <Route
        path="/compare"
        element={<HardwareCompareSelect />}
      />

      <Route
        path="/compare/:leftVariantId/:rightVariantId"
        element={<HardwareCompare />}
      />

      <Route
        path="/admin"
        element={<Admin />}
      />
    </Routes>
  );
}

export default App;