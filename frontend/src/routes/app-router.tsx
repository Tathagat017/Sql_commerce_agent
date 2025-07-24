import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SQLDashboard from "../components/SQLDashboard";

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SQLDashboard />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;
