import { useState, useEffect } from "react";
import "../styles/CreateUser.css";
import api from "../api";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { ToastContainer, toast, Bounce } from "react-toastify";

function CreateUser() {
  const location = useLocation();
  const navigate = useNavigate();
  const passedRole = location.state?.role;

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [creatingUserRole, setCreatingUserRole] = useState(
    "Project Coordinator"
  );
  const [loading, setLoading] = useState(false);
  const [currentUsername, setCurrentUsername] = useState("");

  useEffect(() => {
    getCurrentUser();
  }, []);

  const getCurrentUser = async () => {
    try {
      const res = await api.get("/user/");
      setCurrentUsername(res.data.username);
    } catch (error) {
      console.log(error);
    }
  };

  if (passedRole === "Employee") {
    return (
      <div className="create-user-container">
        <nav className="navbar">
          <div className="navbar-brand">
            <div className="logo">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="8" fill="#6366f1" />
                <path d="M16 8L22 14L16 20L10 14L16 8Z" fill="white" />
                <path d="M16 12L20 16L16 20L12 16L16 12Z" fill="#c7d2fe" />
              </svg>
            </div>
            <span className="brand-text">Task Manager</span>
          </div>
          <Link to="/" className="back-button">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                clipRule="evenodd"
              />
            </svg>
            <span>Back to Home</span>
          </Link>
        </nav>
        <div className="access-denied">
          <div className="access-denied-card">
            <div className="access-denied-icon">
              <svg
                width="64"
                height="64"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 018.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <h1>Access Denied</h1>
            <p>Employees do not have permission to create users.</p>
            <Link to="/" className="home-link">
              Return to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const url =
    creatingUserRole === "Project Coordinator" ? "/users/" : "/employees/";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await api.post(url, { username, email, creatingUserRole });
      toast.success(res.data?.detail || "User created successfully!", {
        position: "bottom-center",
        autoClose: 5000,
        theme: "light",
        transition: Bounce,
      });
      // Reset form
      setUsername("");
      setEmail("");
      setCreatingUserRole("Project Coordinator");
    } catch (err) {
      toast.error(
        err.response?.data?.detail || err.message || "Something went wrong",
        {
          position: "bottom-center",
          autoClose: 5000,
          theme: "light",
          transition: Bounce,
        }
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-user-container">
      {/* Modern Navbar */}
      <nav className="navbar">
        <div className="navbar-brand">
          <div className="logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <rect width="32" height="32" rx="8" fill="#6366f1" />
              <path d="M16 8L22 14L16 20L10 14L16 8Z" fill="white" />
              <path d="M16 12L20 16L16 20L12 16L16 12Z" fill="#c7d2fe" />
            </svg>
          </div>
          <span className="brand-text">Task Manager</span>
        </div>

        <div className="navbar-actions">
          <span className="current-user">{currentUsername}</span>
          <Link to="/" className="back-button">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                clipRule="evenodd"
              />
            </svg>
            <span>Back to Home</span>
          </Link>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <div className="content-wrapper">
          <div className="page-header">
            <div className="header-icon">
              <svg
                width="32"
                height="32"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z" />
              </svg>
            </div>
            <div>
              <h1 className="page-title">Create New User</h1>
              <p className="page-subtitle">
                Add a new team member to your workspace
              </p>
            </div>
          </div>

          <div className="form-card">
            <form onSubmit={handleSubmit} className="create-user-form">
              <div className="form-group">
                <label htmlFor="username" className="form-label">
                  Username
                  <span className="required">*</span>
                </label>
                <div className="input-wrapper">
                  <div className="input-icon">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <input
                    id="username"
                    className="form-input"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter username"
                    required
                    autoComplete="username"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="email" className="form-label">
                  Email Address
                  <span className="required">*</span>
                </label>
                <div className="input-wrapper">
                  <div className="input-icon">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                    </svg>
                  </div>
                  <input
                    id="email"
                    className="form-input"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter email address"
                    required
                    autoComplete="email"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="role" className="form-label">
                  User Role
                  <span className="required">*</span>
                </label>
                <div className="input-wrapper">
                  <div className="input-icon">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z"
                        clipRule="evenodd"
                      />
                      <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
                    </svg>
                  </div>
                  <select
                    id="role"
                    className="form-select"
                    value={creatingUserRole}
                    onChange={(e) => setCreatingUserRole(e.target.value)}
                    required
                  >
                    <option value="Project Coordinator">
                      Project Coordinator
                    </option>
                    <option value="Employee">Employee</option>
                  </select>
                  <div className="select-arrow">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                </div>
                <p className="field-description">
                  {creatingUserRole === "Project Coordinator"
                    ? "Can manage projects, assign tasks, and create users"
                    : "Can view and complete assigned tasks"}
                </p>
              </div>

              <div className="form-actions">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={() => navigate("/")}
                  disabled={loading}
                >
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <span>Cancel</span>
                </button>

                <button
                  type="submit"
                  className="submit-button"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <svg
                        className="spinner"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                      >
                        <circle
                          className="spinner-circle"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        />
                      </svg>
                      <span>Creating...</span>
                    </>
                  ) : (
                    <>
                      <svg
                        width="20"
                        height="20"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span>Create User</span>
                    </>
                  )}
                </button>
              </div>
            </form>

            <div className="form-info">
              <div className="info-item">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>
                  A temporary password will be sent to the user's email
                </span>
              </div>
            </div>
          </div>
        </div>
      </main>

      <ToastContainer
        position="bottom-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
        transition={Bounce}
      />
    </div>
  );
}

export default CreateUser;
