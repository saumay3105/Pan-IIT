import React, { useState, useEffect } from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import Home from "../pages/Home";
import About from "../pages/About";
import TextToVideo from "../pages/TextToVideo";
import ScriptEditor from "../pages/ScriptEditor";
import Login from "../pages/Login";
import Signup from "../pages/Signup";
import Header from "../components/Commons/Header";
import PrivateRoute from "./PrivateRoutes";
import ProcessingVideo from "../pages/ProcessingVideo";
import VideoPlayer from "../pages/VideoPlayer";
import SocialLoginPage from "../components/SocialLogin";

const AppRoutes = () => {
  const location = useLocation();
  const [showHeader, setShowHeader] = useState(true);

  // Hide Header on classroom page
  useEffect(() => {
    setShowHeader(location.pathname !== "/classroom");
  }, [location.pathname]);

  return (
    <>
      {showHeader && <Header />}
      <Routes>
        <Route index path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route
          path="/create"
          element={<PrivateRoute element={TextToVideo} />}
        />
        <Route
          path="/script-editor"
          element={<PrivateRoute element={ScriptEditor} />}
        />
        <Route
          path="/social-login"
          element={<PrivateRoute element={SocialLoginPage} />}
        />

        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/video/processing"
          element={<PrivateRoute element={ProcessingVideo} />}
        />
        <Route path="/video/:video_id" element={<VideoPlayer/>} />
      </Routes>
    </>
  );
};

export default AppRoutes;
