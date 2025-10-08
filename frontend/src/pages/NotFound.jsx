import { Link } from "react-router-dom";
import "../styles/AuthPages.css";

function NotFound() {
  return (
    <div className="auth-container">
      <div className="auth-wrapper">
        <div className="not-found-card">
          <div className="not-found-animation">
            <div className="not-found-circle">
              <svg width="200" height="200" viewBox="0 0 200 200" fill="none">
                <circle
                  cx="100"
                  cy="100"
                  r="80"
                  stroke="url(#gradient404)"
                  strokeWidth="4"
                  strokeDasharray="10 5"
                  className="rotating-circle"
                />
                <text
                  x="100"
                  y="115"
                  textAnchor="middle"
                  fontSize="72"
                  fontWeight="700"
                  fill="url(#gradient404)"
                >
                  404
                </text>
                <defs>
                  <linearGradient
                    id="gradient404"
                    x1="0"
                    y1="0"
                    x2="200"
                    y2="200"
                  >
                    <stop offset="0%" stopColor="#667eea" />
                    <stop offset="100%" stopColor="#764ba2" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>

          <div className="not-found-content">
            <h1 className="not-found-title">Page Not Found</h1>
            <p className="not-found-text">
              Oops! The page you're looking for doesn't exist.
              <br />
              It might have been moved or deleted.
            </p>

            <div className="not-found-actions">
              <Link to="/" className="home-button">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                </svg>
                <span>Go to Home</span>
              </Link>

              <Link to="/login" className="login-button">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M3 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1zm7.707 3.293a1 1 0 010 1.414L9.414 9H17a1 1 0 110 2H9.414l1.293 1.293a1 1 0 01-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>Sign In</span>
              </Link>
            </div>
          </div>

          <div className="not-found-suggestions">
            <p className="suggestions-title">Quick Links:</p>
            <div className="suggestions-list">
              <Link to="/" className="suggestion-link">
                Dashboard
              </Link>
              <Link to="/createuser" className="suggestion-link">
                Create User
              </Link>
              <Link to="/changepassword" className="suggestion-link">
                Change Password
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NotFound;
