import { Routes, Route } from "react-router-dom";

import Prediction from "./Prediction.jsx";
import Evaluation from "./Evaluation.jsx";

import "./App.css";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={<Prediction />}
      />

      <Route
        path="/evaluation"
        element={<Evaluation />}
      />
    </Routes>
  );
}

export default App;