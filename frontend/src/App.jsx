import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";
import AppRoutes from "./routes/AppRoutes";
import Preloader from "./pages/Preloader";
import { BrowserRouter as Router } from "react-router-dom";

function App() {
  const { loading } = useContext(AuthContext);

  // if (loading) {
  //   return <Preloader />;
  // }
  return (
    <div className="App">
      <Router>
        <AppRoutes />
      </Router>
    </div>
  );
}

export default App;
