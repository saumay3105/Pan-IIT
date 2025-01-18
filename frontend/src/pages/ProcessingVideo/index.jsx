import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./ProcessingVideo.css";

const ProcessingVideo = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [status, setStatus] = useState("processing");

  useEffect(() => {
    const storedJobId = localStorage.getItem("currentJobId");
    if (storedJobId) {
      pollVideoStatus(storedJobId);
    } else {
      setError("Job ID not found in local storage.");
      setStatus("failed");
    }
  }, []);

  const pollVideoStatus = (jobId) => {
    const pollInterval = setInterval(async () => {
      try {
        const statusResponse = await axios.get(
          `http://localhost:8000/video-status/${jobId}/`
        );

        const videoStatus = statusResponse.data.status;

        if (videoStatus === "completed") {
          const videoId = statusResponse.data.videoId;
          clearInterval(pollInterval);
          navigate(`/video/${videoId}`);
        } else if (videoStatus === "failed") {
          setError("Video generation failed.");
          setStatus("failed");
          clearInterval(pollInterval);
        } else {
          setStatus("processing");
        }
      } catch (err) {
        console.error(err);
        setError("Error fetching video status.");
        setStatus("failed");
        clearInterval(pollInterval);
      }
    }, 5000);
  };

  return (
    <div className="processing-container">
      {status === "processing" && (
        <div className="processing">
          <div className="loader"></div>
          <p>Your video is being processed. Please wait...</p>
        </div>
      )}
      {status === "failed" && (
        <div className="failed">
          <div className="error-icon">❌</div>
          <p>{error || "Something went wrong while processing your video."}</p>
        </div>
      )}
    </div>
  );
};

export default ProcessingVideo;
