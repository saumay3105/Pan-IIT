import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../../../context/AuthContext";
import "./Header.css";

function Header() {
  const { user, loading } = useContext(AuthContext);

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
                <Link to="/social-login">Connect To Socials</Link>
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
    </header>
  );
}

export default Header;
