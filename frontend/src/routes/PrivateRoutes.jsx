import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const PrivateRoute = ({ element: Component }) => {
  const { user } = useContext(AuthContext);

  if (!user) {
    // If the user is not logged in, redirect to the login page
    return <Navigate to="/login" />;
  }

  // If the user is logged in, render the desired component
  return <Component />;
};

export default PrivateRoute;
