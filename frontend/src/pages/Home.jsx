import { useEffect, useState } from "react";
import api from "../api";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Home.css";
function Home() {
  const [role, setRole] = useState("");
  const [username, setUsername] = useState("");
  const navigate = useNavigate();
  useEffect(() => {
    getUser();
  }, []);

  const getUser = async () => {
    const res = await api.get("/user/");
    const userRole = res.data.role_name;
    setUsername(res.data.username);
    setRole(userRole);
  };
  return (
    <div>
      <div className="navbar">
        <div>
          Logged in as <b>{role}</b>
        </div>
        <div className="username">{username}</div>
        <Link to="/changepassword" className="change-password">
          Change Password
        </Link>
        <Link to="/logout" className="logout-button">
          Logout
        </Link>
      </div>

      <Link to="/createuser" state={{ role }}>
        <button className="create-user-button">Create User +</button>
      </Link>
    </div>
  );
}
export default Home;
