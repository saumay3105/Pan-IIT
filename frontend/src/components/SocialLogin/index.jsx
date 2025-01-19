import React, { useState, useEffect } from "react";
import { Instagram, Youtube, MessageCircle } from "lucide-react";

const Modal = ({ isOpen, onClose, title, children, footer }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="close-button" onClick={onClose}>
            &times;
          </button>
        </div>
        <div
          className="modal-body"
          style={{ color: "#000", textAlign: "left" }}
        >
          {children}
        </div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
};

const SocialLoginPage = () => {
  const [connectedPlatforms, setConnectedPlatforms] = useState({
    instagram: false,
    youtube: false,
    whatsapp: false,
  });

  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [showCredentialsDialog, setShowCredentialsDialog] = useState(false);
  const [showInitialDialog, setShowInitialDialog] = useState(false);
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
    phoneNumber: "",
  });

  // Load connected platforms from localStorage on component mount
  useEffect(() => {
    const savedPlatforms = localStorage.getItem("connectedPlatforms");
    if (savedPlatforms) {
      setConnectedPlatforms(JSON.parse(savedPlatforms));
    }
  }, []);

  // Save connected platforms to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(
      "connectedPlatforms",
      JSON.stringify(connectedPlatforms)
    );
  }, [connectedPlatforms]);

  const platforms = {
    instagram: {
      name: "Instagram",
      icon: Instagram,
      color: "pink",
    },
    youtube: {
      name: "YouTube",
      icon: Youtube,
      color: "red",
    },
    whatsapp: {
      name: "WhatsApp",
      icon: MessageCircle,
      color: "green",
    },
  };

  const handleConnect = (platform) => {
    setSelectedPlatform(platform);
    setShowInitialDialog(false);
    setShowCredentialsDialog(true);
  };

  const handleLogin = () => {
    const isWhatsApp = selectedPlatform === "whatsapp";
    const isValidInput = isWhatsApp
      ? credentials.phoneNumber
      : credentials.username && credentials.password;

    if (isValidInput) {
      setConnectedPlatforms((prev) => ({
        ...prev,
        [selectedPlatform]: true,
      }));
      setShowCredentialsDialog(false);
      setCredentials({ username: "", password: "", phoneNumber: "" });
    }
  };

  const renderCredentialsForm = () => {
    if (selectedPlatform === "whatsapp") {
      return (
        <div className="credentials-form">
          <input
            type="tel"
            placeholder="Phone Number"
            value={credentials.phoneNumber}
            onChange={(e) =>
              setCredentials((prev) => ({
                ...prev,
                phoneNumber: e.target.value,
              }))
            }
          />
        </div>
      );
    }

    return (
      <div className="credentials-form">
        <input
          type="text"
          placeholder="Username"
          value={credentials.username}
          onChange={(e) =>
            setCredentials((prev) => ({
              ...prev,
              username: e.target.value,
            }))
          }
        />
        <input
          type="password"
          placeholder="Password"
          value={credentials.password}
          onChange={(e) =>
            setCredentials((prev) => ({
              ...prev,
              password: e.target.value,
            }))
          }
        />
      </div>
    );
  };

  return (
    <div className="hero">
      <div className="background-video" />
      <div className="hero-content homepage">
        <h1 className="hero-heading">
          <span className="hero__boring-text">Connect Your</span>
          <span className="hero__gradient-text">Social Media Accounts</span>
        </h1>

        <div className="features-container">
          <div className="features-grid">
            {Object.entries(platforms).map(([key, platform]) => (
              <div key={key} className="platform-card">
                <div className="platform-info">
                  <platform.icon
                    className="platform-icon"
                    style={{ color: platform.color }}
                  />
                  <span className="platform-name">{platform.name}</span>
                </div>

                <button
                  className={`connect-button ${
                    connectedPlatforms[key] ? "connected" : ""
                  }`}
                  disabled={connectedPlatforms[key]}
                  onClick={() => {
                    setSelectedPlatform(key);
                    setShowInitialDialog(true);
                  }}
                >
                  {connectedPlatforms[key] ? "Connected" : "Connect"}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Initial Dialog */}
        <Modal
          isOpen={showInitialDialog}
          onClose={() => setShowInitialDialog(false)}
          title={`Connect to ${
            selectedPlatform ? platforms[selectedPlatform].name : ""
          }`}
          footer={
            <div className="modal-buttons">
              <button
                className="btn-secondary"
                onClick={() => setShowInitialDialog(false)}
              >
                Cancel
              </button>
              <button
                className="btn-primary"
                onClick={() => handleConnect(selectedPlatform)}
              >
                Continue
              </button>
            </div>
          }
        >
          <p>
            Would you like to connect your{" "}
            {selectedPlatform ? platforms[selectedPlatform].name : ""} account?
          </p>
        </Modal>

        {/* Credentials Dialog */}
        <Modal
          isOpen={showCredentialsDialog}
          onClose={() => setShowCredentialsDialog(false)}
          title={`Enter your ${
            selectedPlatform ? platforms[selectedPlatform].name : ""
          } ${
            selectedPlatform === "whatsapp" ? "phone number" : "credentials"
          }`}
          footer={
            <div className="modal-buttons">
              <button
                className="btn-secondary"
                onClick={() => {
                  setShowCredentialsDialog(false);
                  setCredentials({
                    username: "",
                    password: "",
                    phoneNumber: "",
                  });
                }}
              >
                Cancel
              </button>
              <button className="btn-primary" onClick={handleLogin}>
                Connect
              </button>
            </div>
          }
        >
          {renderCredentialsForm()}
        </Modal>
      </div>

      <style jsx>{`
        .hero {
          position: relative;
          height: calc(100vh - 66px);
          text-align: center;
          display: flex;
          flex-direction: column;
          justify-content: center;
          overflow: hidden;
        }

        .background-video {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
          z-index: -1;
        }

        .hero-content {
          position: relative;
          z-index: 1;
          padding: 0;
        }

        .hero-heading {
          font-size: 3rem;
          text-align: center;
          display: flex;
          flex-direction: column;
          font-weight: 100;
          color: #4a566f;
        }

        .hero__boring-text {
          font-weight: 800;
          background: rgb(211, 211, 211);
          background: linear-gradient(
            150deg,
            rgba(211, 211, 211, 1) 0%,
            rgba(111, 111, 111, 1) 100%
          );
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .hero__gradient-text {
          font-weight: 800;
          background: rgb(251, 185, 108);
          background: linear-gradient(
            290deg,
            rgb(44, 173, 238) 0%,
            rgba(0, 106, 209, 1) 100%
          );
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .homepage {
          position: relative;
          color: white;
          z-index: 1;
          margin: 0;
          background-color: rgba(255, 255, 255, 0.5);
        }

        .features-container {
          display: flex;
          justify-content: center;
          align-items: center;
          margin: 40px auto;
          max-width: 1200px;
        }

        .features-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 24px;
          padding: 0 20px;
        }

        .platform-card {
          background: white;
          border-radius: 8px;
          padding: 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .platform-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        .platform-info {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .platform-icon {
          width: 24px;
          height: 24px;
          padding: 4px;
          border-radius: 50%;
          transition: transform 0.3s ease;
        }

        .platform-card:hover .platform-icon {
          transform: scale(1.1);
        }

        .platform-name {
          color: rgb(35, 87, 140);
          font-weight: 500;
        }

        .connect-button {
          padding: 10px 20px;
          border-radius: 5px;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.3s ease;
          border: none;
          background: #006ad1;
          color: white;
        }

        .connect-button:hover:not(:disabled) {
          background: #0256aa;
          transform: translateY(-1px);
        }

        .connect-button.connected {
          background: transparent;
          border: 2px solid #006ad1;
          color: rgb(35, 87, 140);
          cursor: default;
        }

        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
          animation: fadeIn 0.3s ease;
        }

        .modal-content {
          background: white;
          border-radius: 8px;
          width: 90%;
          max-width: 500px;
          padding: 20px;
          animation: slideIn 0.3s ease;
        }

        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }

        .modal-header h2 {
          margin: 0;
          color: #333;
        }

        .close-button {
          background: none;
          border: none;
          font-size: 24px;
          cursor: pointer;
          color: #666;
          transition: color 0.3s ease;
        }

        .close-button:hover {
          color: #333;
        }

        .modal-body {
          margin-bottom: 20px;
        }

        .modal-buttons {
          display: flex;
          justify-content: flex-end;
          gap: 12px;
        }

        .credentials-form {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .credentials-form input {
          padding: 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 16px;
          transition: border-color 0.3s ease;
        }

        .credentials-form input:focus {
          outline: none;
          border-color: #006ad1;
        }

        .btn-primary {
          background: #006ad1;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 5px;
          cursor: pointer;
          transition: background-color 0.3s ease;
        }

        .btn-primary:hover {
          background: #0256aa;
        }

        .btn-secondary {
          background: transparent;
          color: rgb(35, 87, 140);
          border: 2px solid #006ad1;
          padding: 10px 20px;
          border-radius: 5px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .btn-secondary:hover {
          background: #c1c1c141;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default SocialLoginPage;
