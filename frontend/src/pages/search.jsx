import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Search() {
  const navigate = useNavigate();

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) {
      setMessage("Please enter something to search.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setResults([]);

      const response = await api.post("/search", {
        query: query.trim(),
      });

      console.log("SEARCH RESPONSE:", response.data);

      const data = response.data;

      if (Array.isArray(data)) {
        setResults(data);
      } else if (Array.isArray(data.results)) {
        setResults(data.results);
      } else {
        setResults([]);
      }

    } catch (error) {
      console.error("SEARCH ERROR:", error);

      setMessage(
        error.response?.data?.message ||
        error.response?.data?.error ||
        "Search failed."
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
            className="nav-item active"
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

        <div className="page-header">

          <div>

            <h1>
              Semantic Search
            </h1>

            <p>
              Find relevant information from
              your personal knowledge.
            </p>

          </div>

        </div>


        {/* =========================
            SEARCH CARD
        ========================= */}

        <section className="search-main-card">

          <div className="search-card-heading">

            <div className="search-icon-box">
              🔍
            </div>

            <div>

              <h2>
                Search Your Knowledge
              </h2>

              <p>
                Ask naturally instead of searching
                with exact keywords.
              </p>

            </div>

          </div>


          <form
            onSubmit={handleSearch}
            className="search-form"
          >

            <input
              type="text"
              value={query}
              onChange={(e) =>
                setQuery(e.target.value)
              }
              placeholder="Example: What is Python?"
            />


            <button
              type="submit"
              className="search-btn"
              disabled={loading}
            >
              {loading
                ? "Searching..."
                : "Search"}
            </button>

          </form>


          {message && (

            <div className="search-message">
              {message}
            </div>

          )}

        </section>


        {/* =========================
            SEARCH RESULTS
        ========================= */}

        {results.length > 0 && (

          <section className="search-results-section">

            <div className="results-header">

              <div>

                <h2>
                  Relevant Results
                </h2>

                <p>
                  Information retrieved from
                  your knowledge base.
                </p>

              </div>

              <span className="result-count">
                {results.length}
              </span>

            </div>


            <div className="results-list">

              {results.map(
                (result, index) => (

                  <article
                    className="search-result-card"
                    key={index}
                  >

                    <div className="result-top">

                      <div>

                        <h3>
                          {result.file_name ||
                            `Result ${index + 1}`}
                        </h3>

                        {result.chunk_id && (

                          <span className="chunk-label">
                            Chunk {result.chunk_id}
                          </span>

                        )}

                      </div>


                      {result.distance !==
                        undefined && (

                        <div className="distance-box">

                          <span>
                            Distance
                          </span>

                          <strong>
                            {Number(
                              result.distance
                            ).toFixed(4)}
                          </strong>

                        </div>

                      )}

                    </div>


                    <p className="result-text">
                      {result.text}
                    </p>


                    {result.relevance_percentage !==
                      undefined && (

                      <div className="relevance">

                        <span>
                          Relevance
                        </span>

                        <strong>
                          {Number(
                            result.relevance_percentage
                          ).toFixed(2)}
                          %
                        </strong>

                      </div>

                    )}

                  </article>

                )
              )}

            </div>

          </section>

        )}


        {/* EMPTY STATE */}

        {!loading &&
          !message &&
          results.length === 0 && (

          <div className="search-empty">

            <div className="empty-search-icon">
              🔍
            </div>

            <h3>
              Search your knowledge
            </h3>

            <p>
              Enter a natural-language question
              above to find relevant information.
            </p>

          </div>

        )}

      </main>

    </div>
  );
}

export default Search;