import { Link } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../../context/AuthContext";
import "./Header.css";

function Header() {
  const { user } = useContext(AuthContext);
  const [allConnected, setAllConnected] = useState(false);

  // Check social media connection status
  const checkConnectionStatus = () => {
    const storedPlatforms = localStorage.getItem('connectedPlatforms');
    if (storedPlatforms) {
      const platforms = JSON.parse(storedPlatforms);
      // Check if all platforms are connected
      const isAllConnected = platforms.instagram && platforms.youtube && platforms.whatsapp;
      setAllConnected(isAllConnected);
    } else {
      setAllConnected(false);
    }
  };

  // Check status on mount and set up interval
  useEffect(() => {
    checkConnectionStatus();
    const intervalId = setInterval(checkConnectionStatus, 1000);
    
    // Cleanup interval on unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <header className="header">
      <div className="header__container">
        <Link to="/">
          <span className="logo">Adwise.AI</span>
        </Link>
        <nav>
          {!user ? (
            <ul>
              <li>
                <Link to="/create" className="btn-nav-main">
                  Get Started
                </Link>
              </li>
              <li>
                <a href="#features">Features</a>
              </li>
              <li>
                <a href="#about">About</a>
              </li>
              <li>
                <Link to="/login">Log-in</Link>
              </li>
            </ul>
          ) : (
            <ul>
              <li>
                {allConnected ? (
                  <Link className="connected-status" to="/social-login">
                    <span className="green-dot"></span>
                    <span>Connected to Socials</span>
                  </Link>
                ) : (
                  <Link to="/social-login">Connect To Socials</Link>
                )}
              </li>
              <li>
                <Link to="/create">Create</Link>
              </li>
              <li>
                <Link to="/profile">Hi, {user.full_name.split(" ")[0]}</Link>
              </li>
            </ul>
          )}
        </nav>
      </div>
      
      <style jsx>{`
        .connected-status {
          display: flex;
          align-items: center;
          gap: 8px;
        }
        
        .green-dot {
          width: 8px;
          height: 8px;
          background-color: #2ecc71;
          border-radius: 50%;
          display: inline-block;
        }
      `}</style>
    </header>
  );
}

export default Header;