import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Facebook,
  Instagram,
  Twitter,
  Copy,
  Share2,
  MessageCircle,
} from "lucide-react";

import "./VideoPlayer.css";

function VideoPlayer() {
  const { video_id } = useParams(); // Get video_id from URL
  const [videoData, setVideoData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const videoRef = useRef(null);
  const navigate = useNavigate();
  const currentUrl = window.location.href; // Get the current page URL
  const setIsVideoPlaying = false;
  const [visemes, setVisemes] = useState();

  useEffect(() => {
    // Fetch video details based on video_id
    const fetchVideo = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/video/${video_id}/`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch video");
        }
        const data = await response.json();
        setVideoData(data.video);
        setVisemes(data.video.visemes);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchVideo();
  }, [video_id]);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return; // Ensure the video element exists

    const handlePlay = () => {
      setIsVideoPlaying(true);
    };
    const handlePause = () => {
      setIsVideoPlaying(false);
    };

    video.addEventListener("play", handlePlay);
    video.addEventListener("pause", handlePause);

    // Cleanup event listeners
    return () => {
      video.removeEventListener("play", handlePlay);
      video.removeEventListener("pause", handlePause);
    };
  }, [setIsVideoPlaying, videoRef.current]);

  const handleQuizRedirect = () => {
    navigate("/quiz");
  };

  const handleCopyUrl = () => {
    navigator.clipboard.writeText(currentUrl);
    alert("URL copied to clipboard!");
  };

  const handleSendEmail = async () => {
    const storedJobId = localStorage.getItem("currentJobId");

    if (!storedJobId) {
      console.error("No Job ID found in localStorage.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/send-emails/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ job_id: storedJobId }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Email sent successfully:", result);
      } else {
        console.error("Failed to send email:", response.statusText);
      }
    } catch (error) {
      console.error("Error sending email:", error);
    }
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div className="video-player-container">
      <h2>{videoData.title}</h2>
      <div className="video-container">
        <video
          ref={videoRef}
          src={"http://127.0.0.1:8000" + videoData.video_file}
          controls
        />
        <div className="avatar-container">
          {/* <Canvas
            camera={{
              zoom: 5,
            }}
          >
            <OrbitControls
              target={[0, 1.2, 0]}
              enableRotate={false}
              enablePan={false}
              enableZoom={true}
            />
            <Environment preset="sunset" />
            <ambientLight intensity={0.8} color="pink" />
            <TalkingAvatar
              avatar="Ananya"
              visemes={visemes}
              videoRef={videoRef}
            />
          </Canvas> */}
        </div>
      </div>
      <p>{videoData.description}</p>

      {/* Share buttons with icons */}
      <div className="share-buttons">
        <button className="share-btn" onClick={handleCopyUrl}>
          <Copy size={16} style={{ marginRight: "5px" }} /> Copy URL
        </button>
        <button className="share-btn" onClick={handleSendEmail}>
          <Copy size={16} style={{ marginRight: "5px" }} /> Send Email
        </button>

        <a
          href={`https://www.facebook.com/sharer/sharer.php?u=${currentUrl}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          <button className="share-btn">
            <Facebook size={16} style={{ marginRight: "5px" }} /> Facebook
          </button>
        </a>
        <a
          href={`https://www.instagram.com/?url=${currentUrl}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          <button className="share-btn">
            <Instagram size={16} style={{ marginRight: "5px" }} /> Instagram
          </button>
        </a>
        <a
          href={`https://twitter.com/intent/tweet?url=${currentUrl}&text=${videoData.title}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          <button className="share-btn">
            <Twitter size={16} style={{ marginRight: "5px" }} /> Twitter
          </button>
        </a>
        <a
          href={`https://api.whatsapp.com/send?text=${currentUrl}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          <button className="share-btn">
            <MessageCircle size={16} style={{ marginRight: "5px" }} /> WhatsApp
          </button>
        </a>
      </div>
    </div>
  );
}

export default VideoPlayer;
