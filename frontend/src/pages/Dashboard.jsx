import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const response = await api.get("/auth/profile");

        setUser(response.data);
      } catch (error) {
        console.error("Profile error:", error);

        localStorage.removeItem("jwt_token");

        navigate("/login");
      }
    };

    loadProfile();
  }, [navigate]);

  const logout = () => {
    localStorage.removeItem("jwt_token");

    navigate("/login");
  };

  return (
    <div className="app-layout">

      {/* =========================
          SIDEBAR
      ========================= */}

      <aside className="sidebar">

        <div className="brand">
          <h1>Second Brain</h1>

          <p>
            Personal Knowledge Assistant
          </p>
        </div>


        <nav className="sidebar-nav">

          <button
            className="nav-item active"
            onClick={() => navigate("/dashboard")}
          >
            <span>🏠</span>
            <span>Dashboard</span>
          </button>


          <button
            className="nav-item"
            onClick={() => navigate("/notes")}
          >
            <span>📝</span>
            <span>Notes</span>
          </button>


          <button
            className="nav-item"
            onClick={() => navigate("/upload")}
          >
            <span>📁</span>
            <span>Upload</span>
          </button>


          <button
            className="nav-item"
            onClick={() => navigate("/search")}
          >
            <span>🔍</span>
            <span>Search</span>
          </button>


          <button
            className="nav-item"
            onClick={() => navigate("/ask")}
          >
            <span>✨</span>
            <span>Ask AI</span>
          </button>


          <button
            className="nav-item"
            onClick={() => navigate("/history")}
          >
            <span>🕘</span>
            <span>History</span>
          </button>

        </nav>


        <button
          className="logout-btn"
          onClick={logout}
        >
          ↪ Logout
        </button>

      </aside>


      {/* =========================
          MAIN CONTENT
      ========================= */}

      <main className="main-content">

        {/* HEADER */}

        <header className="dashboard-header">

          <div>

            <h1>
              Welcome back,{" "}
              {user?.name || "User"}
            </h1>

            <p>
              Manage and explore your personal
              knowledge.
            </p>

          </div>


          <div className="user-email">
            {user?.email || ""}
          </div>

        </header>


        {/* =========================
            STAT CARDS
        ========================= */}

        <section className="stats-grid">

          <div className="stat-card">

            <span>
              My Notes
            </span>

            <strong>
              —
            </strong>

          </div>


          <div className="stat-card">

            <span>
              Documents
            </span>

            <strong>
              —
            </strong>

          </div>


          <div className="stat-card">

            <span>
              AI Queries
            </span>

            <strong>
              —
            </strong>

          </div>

        </section>


        {/* =========================
            QUICK ACTIONS
        ========================= */}

        <section className="quick-section">

          <div className="section-heading">

            <h2>
              Quick Actions
            </h2>

            <p>
              Access your knowledge tools quickly.
            </p>

          </div>


          <div className="quick-grid">

            {/* CREATE NOTE */}

            <button
              className="quick-card"
              onClick={() => navigate("/notes")}
            >

              <span className="quick-icon">
                📝
              </span>

              <div>

                <h3>
                  Create a Note
                </h3>

                <p>
                  Add and manage your personal
                  notes.
                </p>

              </div>

            </button>


            {/* UPLOAD */}

            <button
              className="quick-card"
              onClick={() => navigate("/upload")}
            >

              <span className="quick-icon">
                📁
              </span>

              <div>

                <h3>
                  Upload Knowledge
                </h3>

                <p>
                  Upload PDF, DOCX or image files.
                </p>

              </div>

            </button>


            {/* SEARCH */}

            <button
              className="quick-card"
              onClick={() => navigate("/search")}
            >

              <span className="quick-icon">
                🔍
              </span>

              <div>

                <h3>
                  Search Knowledge
                </h3>

                <p>
                  Find relevant information using
                  semantic search.
                </p>

              </div>

            </button>


            {/* ASK AI */}

            <button
              className="quick-card"
              onClick={() => navigate("/ask")}
            >

              <span className="quick-icon">
                ✨
              </span>

              <div>

                <h3>
                  Ask AI
                </h3>

                <p>
                  Ask questions and get
                  context-aware answers.
                </p>

              </div>

            </button>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;
