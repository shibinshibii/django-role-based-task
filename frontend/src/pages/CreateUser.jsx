import { useState } from "react";
import "../styles/Login.css";
import api from "../api";
import { useLocation } from "react-router-dom";
import { ToastContainer, toast, Bounce } from "react-toastify";

function CreateUser() {
  const location = useLocation();
  const passedRole = location.state?.role;

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const creatingUserRole = passedRole === "Admin" ? "Project Coordinator" : "Employee";
  const [loading, setLoading] = useState(false);

  const url = passedRole === "Admin" ? "/users/" : "/employees/";

  if (passedRole === "Employee") {
    return (
      <div>
        <h1>Employees cannot create users.</h1>
      </div>
    );
  }

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post(url, { username, email, creatingUserRole });
      toast.success(res.data?.detail || "User created successfully!", {
        position: "bottom-center",
        autoClose: 5000,
        theme: "light",
        transition: Bounce,
      });
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
    <div>
      <form onSubmit={handleSubmit} className="form-container">
        <h1>Create User</h1>
        <input
          className="form-input"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          className="form-input"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          className="form-input"
          type="text"
          value={creatingUserRole}
          placeholder="Role"
          disabled={true}
        />
        {/* <label htmlFor="difficulty">Select Role</label>
        <select
          id="role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <option value="project coordinator">Project Coordinator</option>
          <option value="employee">Employee</option>
        </select> */}
        <button type="submit" className="form-button" disabled={loading}>
          {loading ? "Creating..." : "Create User"}
        </button>
      </form>

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
