import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import Header from "@/components/Commons/Header";
import "./Signup.css";

const Signup = () => {
  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/auth/registration/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );

      const data = await response.json();
      if (response.ok) {
        console.log("Signup successful:", data);
        toast.success("Login Successful!", {
          position: "top-center",
        });
        navigate("/login");
      } else {
        console.error("Signup failed:", data);
        Object.keys(data).forEach((key) => {
          const errorMessages = data[key];

          // Check if the value is an array (as in your example)
          if (Array.isArray(errorMessages)) {
            errorMessages.forEach((message) => {
              toast.error(`Login Failed! ${message}`, {
                position: "top-right",
              });
            });
          } else {
            toast.error(`Login Failed! ${errorMessages}`, {
              position: "top-right",
            });
          }
        });
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <div className="signup-page">
        <div className="signup-container">
          <h2>Signup</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Full Name:</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
              />
            </div>
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
            <div className="form-group">
              <label>Confirm Password:</label>
              <input
                type="password"
                name="confirm_password"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit" className="signup-button">
              Signup
            </button>
          </form>
          <div className="signup-options">
            <p>
              Already have an account?{" "}
              <Link to="/login" style={{ textDecoration: "underline" }}>
                Login
              </Link>
            </p>
          </div>
        </div>
      </div>
      <ToastContainer />
    </>
  );
};

export default Signup;
