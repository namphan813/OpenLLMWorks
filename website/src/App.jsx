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
import Methodology from "./pages/Methodology";
import Admin from "./pages/Admin";
import AdminSubmission from "./pages/AdminSubmission";


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
        path="/methodology"
        element={<Methodology />}
      />

      <Route
        path="/admin"
        element={<Admin />}
      />

      <Route
        path="/admin/submissions/:submissionId"
        element={<AdminSubmission />}
      />
    </Routes>
  );
}

export default App;