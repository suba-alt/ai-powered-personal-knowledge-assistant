import { NavLink, useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("jwt_token");
    navigate("/login");
  };

  return (
    <aside className="sidebar">
      <div className="logo">
        🧠 <span>Second Brain</span>
      </div>

      <nav>
        <NavLink to="/dashboard">🏠 Dashboard</NavLink>
        <NavLink to="/notes">📝 Notes</NavLink>
        <NavLink to="/upload">📁 Upload</NavLink>
        <NavLink to="/search">🔍 Search</NavLink>
        <NavLink to="/ask">🤖 Ask AI</NavLink>
        <NavLink to="/history">🕘 History</NavLink>
        <NavLink to="/profile">👤 Profile</NavLink>
      </nav>

      <button className="logout-btn" onClick={logout}>
        🚪 Logout
      </button>
    </aside>
  );
}

export default Sidebar;