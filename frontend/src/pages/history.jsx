import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function History() {
  const navigate = useNavigate();

  const [queries, setQueries] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);

  const [queryError, setQueryError] = useState("");
  const [chatError, setChatError] = useState("");

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setLoading(true);

    setQueryError("");
    setChatError("");

    // AI Queries
    try {
      const response = await api.get("/ai-queries");

      console.log(
        "AI QUERIES:",
        response.data
      );

      const data = response.data;

      if (Array.isArray(data)) {
        setQueries(data);
      } else if (
        Array.isArray(data.ai_queries)
      ) {
        setQueries(data.ai_queries);
      } else if (
        Array.isArray(data.queries)
      ) {
        setQueries(data.queries);
      } else {
        setQueries([]);
      }

    } catch (error) {
      console.error(
        "AI QUERY HISTORY ERROR:",
        error
      );

      setQueryError(
        error.response?.data?.message ||
        error.response?.data?.error ||
        "Unable to load AI queries."
      );
    }


    // Chat History
    try {
      const response = await api.get(
        "/chat-history"
      );

      console.log(
        "CHAT HISTORY:",
        response.data
      );

      const data = response.data;

      if (Array.isArray(data)) {
        setChatHistory(data);
      } else if (
        Array.isArray(data.chat_history)
      ) {
        setChatHistory(data.chat_history);
      } else if (
        Array.isArray(data.history)
      ) {
        setChatHistory(data.history);
      } else {
        setChatHistory([]);
      }

    } catch (error) {
      console.error(
        "CHAT HISTORY ERROR:",
        error
      );

      setChatError(
        error.response?.data?.message ||
        error.response?.data?.error ||
        "Unable to load chat history."
      );
    }

    setLoading(false);
  };


  const logout = () => {
    localStorage.removeItem("jwt_token");
    navigate("/login");
  };


  return (
    <div className="app-layout">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="brand">

          <h1>
            Second Brain
          </h1>

          <p>
            Personal Knowledge Assistant
          </p>

        </div>


        <nav className="sidebar-nav">

          <button
            className="nav-item"
            onClick={() =>
              navigate("/dashboard")
            }
          >
            <span>🏠</span>
            <span>Dashboard</span>
          </button>


          <button
            className="nav-item"
            onClick={() =>
              navigate("/notes")
            }
          >
            <span>📝</span>
            <span>Notes</span>
          </button>


          <button
            className="nav-item"
            onClick={() =>
              navigate("/upload")
            }
          >
            <span>📁</span>
            <span>Upload</span>
          </button>


          <button
            className="nav-item"
            onClick={() =>
              navigate("/search")
            }
          >
            <span>🔍</span>
            <span>Search</span>
          </button>


          <button
            className="nav-item"
            onClick={() =>
              navigate("/ask")
            }
          >
            <span>✨</span>
            <span>Ask AI</span>
          </button>


          <button
            className="nav-item active"
            onClick={() =>
              navigate("/history")
            }
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


      {/* MAIN */}

      <main className="main-content">

        <div className="page-header">

          <div>

            <h1>
              AI History
            </h1>

            <p>
              View your previous AI questions
              and responses.
            </p>

          </div>

        </div>


        {loading ? (

          <div className="history-loading">

            <div className="loading-spinner">
              ⟳
            </div>

            <p>
              Loading your history...
            </p>

          </div>

        ) : (

          <div className="history-grid">

            {/* AI QUERIES */}

            <section className="history-panel">

              <div className="history-panel-header">

                <div>

                  <h2>
                    AI Queries
                  </h2>

                  <p>
                    Your previous questions
                  </p>

                </div>

                <span>
                  {queries.length}
                </span>

              </div>


              {queryError ? (

                <div className="history-error">
                  {queryError}
                </div>

              ) : queries.length === 0 ? (

                <div className="history-empty">

                  <div>
                    💬
                  </div>

                  <h3>
                    No AI queries yet
                  </h3>

                  <p>
                    Your questions will appear
                    here after using Ask AI.
                  </p>

                </div>

              ) : (

                <div className="history-list">

                  {queries.map(
                    (item, index) => (

                      <div
                        className="history-item"
                        key={
                          item.id ||
                          item.query_id ||
                          index
                        }
                      >

                        <div className="history-number">
                          {index + 1}
                        </div>

                        <div className="history-content">

                          <h3>
                            {item.question ||
                              item.query ||
                              "Question"}
                          </h3>

                          {item.created_at && (

                            <small>
                              {new Date(
                                item.created_at
                              ).toLocaleString()}
                            </small>

                          )}

                        </div>

                      </div>

                    )
                  )}

                </div>

              )}

            </section>


            {/* CHAT HISTORY */}

            <section className="history-panel">

              <div className="history-panel-header">

                <div>

                  <h2>
                    Chat History
                  </h2>

                  <p>
                    Previous AI responses
                  </p>

                </div>

                <span>
                  {chatHistory.length}
                </span>

              </div>


              {chatError ? (

                <div className="history-error">
                  {chatError}
                </div>

              ) : chatHistory.length === 0 ? (

                <div className="history-empty">

                  <div>
                    💭
                  </div>

                  <h3>
                    No chat history yet
                  </h3>

                  <p>
                    AI responses will appear
                    here after asking questions.
                  </p>

                </div>

              ) : (

                <div className="history-list">

                  {chatHistory.map(
                    (item, index) => (

                      <div
                        className="chat-item"
                        key={
                          item.id ||
                          item.query_id ||
                          index
                        }
                      >

                        <div className="chat-question">

                          <span>
                            Q
                          </span>

                          <div>

                            <strong>
                              {item.question ||
                                item.query ||
                                "Question"}
                            </strong>

                          </div>

                        </div>


                        <div className="chat-answer">

                          <span>
                            AI
                          </span>

                          <p>
                            {item.ai_response ||
                              item.response ||
                              item.answer ||
                              "No response available."}
                          </p>

                        </div>


                        {item.created_at && (

                          <small>
                            {new Date(
                              item.created_at
                            ).toLocaleString()}
                          </small>

                        )}

                      </div>

                    )
                  )}

                </div>

              )}

            </section>

          </div>

        )}

      </main>

    </div>
  );
}

export default History;