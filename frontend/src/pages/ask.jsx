import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Ask() {
  const navigate = useNavigate();

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleAsk = async (e) => {
    e.preventDefault();

    if (!question.trim()) {
      setMessage("Please enter your question.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setAnswer("");
      setSources([]);
      setConfidence(null);

      const response = await api.post("/ask", {
        query: question.trim(),
        top_k: 5,
      });

      console.log("ASK RESPONSE:", response.data);

      setAnswer(response.data.answer || "");

      setSources(
        Array.isArray(response.data.sources)
          ? response.data.sources
          : []
      );

      if (
        response.data.confidence_score !== undefined &&
        response.data.confidence_score !== null
      ) {
        setConfidence(
          Number(response.data.confidence_score)
        );
      }

    } catch (error) {
      console.error("ASK ERROR:", error);

      setMessage(
        error.response?.data?.message ||
        error.response?.data?.error ||
        "Failed to generate AI answer."
      );

    } finally {
      setLoading(false);
    }
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
          <h1>Second Brain</h1>
          <p>Personal Knowledge Assistant</p>
        </div>

        <nav className="sidebar-nav">

          <button
            className="nav-item"
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
            className="nav-item active"
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


      {/* MAIN */}

      <main className="main-content">

        <div className="page-header">

          <div>
            <h1>Ask AI</h1>

            <p>
              Ask questions about your stored
              knowledge using RAG.
            </p>
          </div>

        </div>


        {/* ASK CARD */}

        <section className="ask-main-card">

          <div className="ask-card-header">

            <div className="ask-icon-box">
              ✨
            </div>

            <div>
              <h2>
                Ask Your Second Brain
              </h2>

              <p>
                Your question will be answered using
                relevant information from your knowledge base.
              </p>
            </div>

          </div>


          <form
            className="ask-form"
            onSubmit={handleAsk}
          >

            <label>
              Your Question
            </label>

            <textarea
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              placeholder="Example: What did I write about Python?"
              rows="5"
            />

            <button
              type="submit"
              className="ask-btn"
              disabled={loading}
            >
              {loading
                ? "Generating Answer..."
                : "✨ Ask AI"}
            </button>

          </form>


          {message && (
            <div className="ask-error">
              {message}
            </div>
          )}

        </section>


        {/* ANSWER */}

        {answer && (

          <section className="answer-section">

            <div className="answer-card">

              <div className="answer-heading">

                <span className="answer-icon">
                  ✨
                </span>

                <div>
                  <h2>AI Answer</h2>

                  <p>
                    Generated using retrieved
                    information from your knowledge.
                  </p>
                </div>

              </div>


              <div className="answer-text">
                {answer}
              </div>


              {confidence !== null && (

                <div className="context-score">

                  <span>
                    Context Relevance
                  </span>

                  <strong>
                    {confidence.toFixed(2)}%
                  </strong>

                </div>

              )}

            </div>


            {/* SOURCES */}

            {sources.length > 0 && (

              <div className="sources-card">

                <div className="sources-header">

                  <h2>
                    Retrieved Sources
                  </h2>

                  <span>
                    {sources.length}
                  </span>

                </div>


                <div className="sources-list">

                  {sources.map(
                    (source, index) => (

                      <div
                        className="source-item"
                        key={index}
                      >

                        <div className="source-title">

                          <span>
                            📄
                          </span>

                          <strong>
                            {source.file_name ||
                              `Source ${index + 1}`}
                          </strong>

                        </div>


                        <p>
                          {source.text}
                        </p>


                        {source.chunk_id && (
                          <small>
                            Chunk {source.chunk_id}
                          </small>
                        )}

                      </div>

                    )
                  )}

                </div>

              </div>

            )}

          </section>

        )}


        {/* EMPTY STATE */}

        {!answer &&
          !loading &&
          !message && (

          <div className="ask-empty">

            <div>
              ✨
            </div>

            <h3>
              Ask your Second Brain
            </h3>

            <p>
              Ask a question about your stored
              notes or documents.
            </p>

          </div>

        )}

      </main>

    </div>
  );
}

export default Ask;