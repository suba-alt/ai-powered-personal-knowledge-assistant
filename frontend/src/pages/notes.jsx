import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Notes() {
  const navigate = useNavigate();

  const [notes, setNotes] = useState([]);

  const [form, setForm] = useState({
    title: "",
    content: "",
  });

  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // ==========================================
  // GET NOTES
  // ==========================================

  const getNotes = async () => {
    try {
      const response = await api.get("/notes");

      console.log("NOTES RESPONSE:", response.data);

      const data = response.data;

      if (Array.isArray(data)) {
        setNotes(data);
      } else if (Array.isArray(data.notes)) {
        setNotes(data.notes);
      } else {
        setNotes([]);
      }
    } catch (error) {
      console.error("GET NOTES ERROR:", error);

      setMessage(
        error.response?.data?.message ||
          "Failed to load notes."
      );
    }
  };

  // ==========================================
  // PAGE LOAD
  // ==========================================

  useEffect(() => {
    getNotes();
  }, []);

  // ==========================================
  // INPUT CHANGE
  // ==========================================

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  // ==========================================
  // CREATE / UPDATE
  // ==========================================

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.title.trim() || !form.content.trim()) {
      setMessage("Please enter title and content.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      if (editingId) {
        await api.put(
          `/notes/${editingId}`,
          {
            title: form.title,
            content: form.content,
          }
        );

        setMessage("Note updated successfully.");
      } else {
        await api.post(
          "/notes",
          {
            title: form.title,
            content: form.content,
          }
        );

        setMessage("Note created successfully.");
      }

      setForm({
        title: "",
        content: "",
      });

      setEditingId(null);

      await getNotes();

    } catch (error) {
      console.error("SAVE NOTE ERROR:", error);

      setMessage(
        error.response?.data?.message ||
          "Unable to save note."
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // EDIT
  // ==========================================

  const editNote = (note) => {
    setEditingId(note.id);

    setForm({
      title: note.title || "",
      content: note.content || "",
    });

    setMessage("");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // ==========================================
  // CANCEL EDIT
  // ==========================================

  const cancelEdit = () => {
    setEditingId(null);

    setForm({
      title: "",
      content: "",
    });

    setMessage("");
  };

  // ==========================================
  // DELETE
  // ==========================================

  const deleteNote = async (id) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this note?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setMessage("");

      await api.delete(
        `/notes/${id}`
      );

      setMessage("Note deleted successfully.");

      await getNotes();

    } catch (error) {
      console.error("DELETE NOTE ERROR:", error);

      setMessage(
        error.response?.data?.message ||
          "Unable to delete note."
      );
    }
  };

  // ==========================================
  // LOGOUT
  // ==========================================

  const logout = () => {
    localStorage.removeItem("jwt_token");

    navigate("/login");
  };

  // ==========================================
  // DATE FORMAT
  // ==========================================

  const formatDate = (date) => {
    if (!date) {
      return "";
    }

    try {
      return new Date(date).toLocaleString();
    } catch {
      return "";
    }
  };

  return (
    <div className="app-layout">

      {/* =====================================
          SIDEBAR
      ===================================== */}

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
            className="nav-item active"
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
            className="nav-item"
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


      {/* =====================================
          MAIN CONTENT
      ===================================== */}

      <main className="main-content">

        {/* HEADER */}

        <div className="page-header">

          <div>

            <h1>
              My Notes
            </h1>

            <p>
              Create and manage your personal
              knowledge.
            </p>

          </div>

          <div className="notes-count">

            <strong>
              {notes.length}
            </strong>

            <span>
              {notes.length === 1
                ? "Note"
                : "Notes"}
            </span>

          </div>

        </div>


        {/* =====================================
            CONTENT GRID
        ===================================== */}

        <div className="notes-layout">

          {/* ===================================
              CREATE NOTE
          =================================== */}

          <section className="note-form-card">

            <div className="card-heading">

              <div className="heading-icon">
                📝
              </div>

              <div>

                <h2>
                  {editingId
                    ? "Edit Note"
                    : "Create a Note"}
                </h2>

                <p>
                  {editingId
                    ? "Update your existing knowledge."
                    : "Add information to your personal knowledge base."}
                </p>

              </div>

            </div>


            <form
              onSubmit={handleSubmit}
              className="note-form"
            >

              <label>
                Note Title
              </label>

              <input
                type="text"
                name="title"
                value={form.title}
                onChange={handleChange}
                placeholder="Example: Python Basics"
                required
              />


              <label>
                Note Content
              </label>

              <textarea
                name="content"
                value={form.content}
                onChange={handleChange}
                placeholder="Write your knowledge here..."
                rows="10"
                required
              />


              <div className="form-actions">

                <button
                  type="submit"
                  className="primary-btn"
                  disabled={loading}
                >
                  {loading
                    ? "Saving..."
                    : editingId
                    ? "Update Note"
                    : "Save Note"}
                </button>


                {editingId && (
                  <button
                    type="button"
                    className="secondary-btn"
                    onClick={cancelEdit}
                  >
                    Cancel
                  </button>
                )}

              </div>

            </form>


            {message && (
              <div className="note-message">
                {message}
              </div>
            )}

          </section>


          {/* ===================================
              SAVED NOTES
          =================================== */}

          <section className="saved-notes-section">

            <div className="saved-notes-header">

              <div>

                <h2>
                  Saved Notes
                </h2>

                <p>
                  Your personal knowledge
                </p>

              </div>

              <span className="notes-badge">
                {notes.length}
              </span>

            </div>


            {notes.length === 0 ? (

              <div className="empty-notes">

                <div className="empty-icon">
                  📝
                </div>

                <h3>
                  No notes yet
                </h3>

                <p>
                  Create your first note
                  using the form.
                </p>

              </div>

            ) : (

              <div className="notes-list">

                {notes.map((note) => (

                  <article
                    className="saved-note-card"
                    key={note.id}
                  >

                    <div className="saved-note-top">

                      <div>

                        <h3>
                          {note.title}
                        </h3>

                        <span className="note-date">
                          {formatDate(
                            note.created_at
                          )}
                        </span>

                      </div>

                    </div>


                    <p className="saved-note-content">
                      {note.content}
                    </p>


                    <div className="note-actions">

                      <button
                        className="edit-btn"
                        onClick={() =>
                          editNote(note)
                        }
                      >
                        Edit
                      </button>


                      <button
                        className="delete-btn"
                        onClick={() =>
                          deleteNote(note.id)
                        }
                      >
                        Delete
                      </button>

                    </div>

                  </article>

                ))}

              </div>

            )}

          </section>

        </div>

      </main>

    </div>
  );
}

export default Notes;