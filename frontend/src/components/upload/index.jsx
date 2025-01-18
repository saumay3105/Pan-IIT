import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./upload.css";
import VideoPreferenceSelector from "../VideoPreferenceSelector";
import LanguageSelector from "../LanguageSelector";
import { AiOutlineUpload } from "react-icons/ai";
import { BsStars } from "react-icons/bs";
import axios from "axios";

const FileUpload = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [textInput, setTextInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [videoPreference, setVideoPreference] = useState("simplify");
  const [selectedLanguage, setSelectedLanguage] = useState("English");
  const [activeTab, setActiveTab] = useState("upload");
  const navigate = useNavigate();
  const { state } = useLocation();
  const [title, setTitle] = useState();

  // Handle file selection through the file input
  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(files);
  };

  // Handle the upload process for both files and text input
  const handleUpload = async () => {
    if (selectedFiles.length === 0 && textInput.trim() === "") {
      toast.error("Please select a file or input text before uploading.", {
        position: "top-right",
      });
      return;
    }

    const formData = new FormData();

    // Add the file or text to formData
    if (selectedFiles.length > 0) {
      formData.append("file", selectedFiles[0]);
    } else {
      formData.append("text", textInput);
    }

    // Add preferences
    formData.append("video_preference", videoPreference);
    formData.append("language", selectedLanguage);

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/generate-video/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      if (response.status === 202) {
        localStorage.setItem("currentJobId", response.data.job_id);
        navigate("/video/processing");
      }
    } catch (error) {
      console.error("Upload error:", error);
      setLoading(false);
      toast.error("Failed to Process. Please try again.", {
        position: "top-right",
      });
    }
  };

  // Render preview for uploaded files
  const renderPreview = (file) => {
    const fileType = file.type;
    const fileExtension = file.name.split(".").pop().toUpperCase();

    if (fileType.startsWith("image/")) {
      const imageUrl = URL.createObjectURL(file);
      return (
        <img src={imageUrl} alt={file.name} className="file-preview-image" />
      );
    } else
      return (
        <div className="file-preview-icon">
          {"📄" + fileExtension || "📎 File"}
        </div>
      );
  };

  if (loading) {
    return (
      <div className="loading-container">
        <h2 className="upload-heading">Processing your document...</h2>
        <img src="./public/load-35.gif" alt="Loading..." className="img-load" />
      </div>
    );
  }

  return (
    <div className="upload-container">
      <h1 className="upload__title">{title}</h1>
      <div className="tab-navigation">
        <button
          onClick={() => setActiveTab("upload")}
          className={activeTab === "upload" ? "active-tab" : ""}
        >
          Upload File
        </button>
        <button
          onClick={() => setActiveTab("text")}
          className={activeTab === "text" ? "active-tab" : ""}
        >
          Enter Text
        </button>
      </div>

      {activeTab === "upload" && (
        <div className="tab-content">
          <input
            type="file"
            accept=".pdf, .doc, .docx, .pptx, image/*"
            className="upload-file-input"
            onChange={handleFileChange}
            id="file-upload"
          />
          <p className="upload-description">
            Supported file formats: PDF, DOC, DOCX, PPTX, and images (JPEG, PNG,
            etc.)
          </p>
          <label htmlFor="file-upload" className="button-outlined">
            <AiOutlineUpload style={{ marginRight: "8px" }} />
            Choose a file
          </label>
          <div className="file-preview">
            {selectedFiles.length > 0 && (
              <ul>
                {selectedFiles.map((file, index) => (
                  <li key={index} className="file-preview-item">
                    {renderPreview(file)}
                    <p>{file.name}</p>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      {activeTab === "text" && (
        <div className="tab-content">
          <textarea
            className="upload-text-input"
            placeholder="Enter your text here..."
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            rows={7}
          />
        </div>
      )}

      <LanguageSelector setSelectedLanguage={setSelectedLanguage} />
      <VideoPreferenceSelector setVideoLength={setVideoPreference} />
      <ToastContainer />
      <button className="upload-button" onClick={handleUpload}>
        <BsStars style={{ marginRight: "8px" }} />
        Start Generating
      </button>
    </div>
  );
};

export default FileUpload;
