import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import "./Login.css";

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const { setUser } = useContext(AuthContext);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleNormalLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("my-app-auth", data.access);
        toast.success("Login Successful!", {
          position: "top-center",
        });
        setUser(data.user);
        navigate("/");
      } else {
        const error_messages = data["non_field_errors"];
        error_messages.forEach((e) => {
          toast.error(`Login Failed! ${e}`, {
            position: "top-right",
          });
        });
      }
    } catch (error) {
      console.log("An Error occured while logging in:", error);
    }
  };

  const handleGoogleLogin = () => {
    const clientId =
      "124612198450-m656umkla59i5d7nisl122q914fqnrck.apps.googleusercontent.com";
    const redirectUri = "http://localhost:3000/";
    const scope = "openid email profile";
    const nonce = "abcdef";

    const googleAuthUrl = `https://accounts.google.com/o/oauth2/auth?client_id=${clientId}&response_type=token+id_token&redirect_uri=${encodeURIComponent(
      redirectUri
    )}&scope=${encodeURIComponent(scope)}&nonce=${nonce}`;

    window.location.href = googleAuthUrl;
  };

  return (
    <>
      <div className="login-page">
        <div className="login-container">
          <h3 className="login-heading">Welcome Back</h3>
          <form onSubmit={handleNormalLogin}>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit" className="login-button">
              Login
            </button>
          </form>

          <div className="login-options">
            <button
              className="google-signin-button"
              onClick={handleGoogleLogin}
            >
              <img
                src="/google.png"
                alt="Google Logo"
                style={{ width: "20px", marginRight: "10px" }}
              />
              Sign in with Google
            </button>
            <p>
              New User?{" "}
              <Link to="/signup" style={{ textDecoration: "underline" }}>
                Register
              </Link>
            </p>
          </div>
        </div>
      </div>
      <ToastContainer />
    </>
  );
};

export default Login;
