import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Upload() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);

  // ==========================================
  // FILE SELECT
  // ==========================================

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    setMessage("");
    setResult(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "image/jpeg",
      "image/png",
      "image/jpg",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setFile(null);

      setMessage(
        "Only PDF, DOCX, JPG and PNG files are allowed."
      );

      e.target.value = "";

      return;
    }

    setFile(selectedFile);
  };

  // ==========================================
  // UPLOAD + EMBEDDING
  // ==========================================

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      setUploading(true);
      setMessage("");
      setResult(null);

      // ==========================================
      // STEP 1 — UPLOAD FILE
      // ==========================================

      setMessage("Uploading file...");

      const uploadResponse = await api.post(
        "/files/upload",
        formData
      );

      console.log(
        "UPLOAD RESPONSE:",
        uploadResponse.data
      );

      // Get document ID
      const documentId =
        uploadResponse.data.document_id;

      if (!documentId) {
        throw new Error(
          "Upload succeeded, but document_id was not returned."
        );
      }

      console.log(
        "DOCUMENT ID:",
        documentId
      );

      // ==========================================
      // STEP 2 — GENERATE EMBEDDINGS
      // ==========================================

      setMessage(
        "File uploaded. Generating embeddings..."
      );

      const embedResponse = await api.post(
        `/files/${documentId}/embed`
      );

      console.log(
        "EMBED RESPONSE:",
        embedResponse.data
      );

      // ==========================================
      // STEP 3 — SUCCESS
      // ==========================================

      setResult({
        ...uploadResponse.data,
        embedding: embedResponse.data,
      });

      setMessage(
        "File uploaded and added to your knowledge base successfully."
      );

      setFile(null);

      e.target.reset();

    } catch (error) {
      console.error(
        "UPLOAD / EMBEDDING ERROR:",
        error
      );

      console.error(
        "ERROR RESPONSE:",
        error.response?.data
      );

      setMessage(
        error.response?.data?.message ||
        error.response?.data?.error ||
        error.message ||
        "File processing failed."
      );

    } finally {
      setUploading(false);
    }
  };

  // ==========================================
  // LOGOUT
  // ==========================================

  const logout = () => {
    localStorage.removeItem("jwt_token");

    navigate("/login");
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
            className="nav-item"
            onClick={() =>
              navigate("/notes")
            }
          >
            <span>📝</span>
            <span>Notes</span>
          </button>

          <button
            className="nav-item active"
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

        {/* PAGE HEADER */}

        <div className="page-header">

          <div>

            <h1>
              Upload Knowledge
            </h1>

            <p>
              Add documents and images to your
              personal knowledge base.
            </p>

          </div>

        </div>

        {/* =====================================
            UPLOAD AREA
        ===================================== */}

        <div className="upload-layout">

          {/* LEFT — UPLOAD CARD */}

          <section className="upload-card">

            <div className="upload-card-header">

              <div className="upload-icon">
                📁
              </div>

              <div>

                <h2>
                  Upload a Document
                </h2>

                <p>
                  Your file will be processed and
                  added to your knowledge base.
                </p>

              </div>

            </div>

            <form
              onSubmit={handleUpload}
              className="upload-form"
            >

              <div className="file-select-area">

                <div className="file-icon">
                  📄
                </div>

                <h3>
                  Select your file
                </h3>

                <p>
                  PDF, DOCX, JPG, JPEG or PNG
                </p>

                <label className="file-input-label">

                  Choose File

                  <input
                    type="file"
                    accept=".pdf,.docx,.jpg,.jpeg,.png"
                    onChange={handleFileChange}
                  />

                </label>

                {file && (

                  <div className="selected-file">

                    <strong>
                      Selected file
                    </strong>

                    <p>
                      {file.name}
                    </p>

                    <span>
                      {(file.size / 1024).toFixed(2)}
                      {" "}KB
                    </span>

                  </div>

                )}

              </div>

              <button
                type="submit"
                className="upload-btn"
                disabled={
                  uploading || !file
                }
              >

                {uploading
                  ? "Processing..."
                  : "Upload File"}

              </button>

            </form>

            {/* MESSAGE */}

            {message && (

              <div
                className={
                  message.includes("successfully")
                    ? "upload-message success"
                    : "upload-message error"
                }
              >
                {message}
              </div>

            )}

            {/* RESULT */}

            {result && (

              <div className="upload-result">

                <h3>
                  ✓ Knowledge Added
                </h3>

                {result.document_id && (

                  <p>
                    <strong>
                      Document ID:
                    </strong>{" "}
                    {result.document_id}
                  </p>

                )}

                {result.file_name && (

                  <p>
                    <strong>
                      File:
                    </strong>{" "}
                    {result.file_name}
                  </p>

                )}

                {result.embedding && (

                  <p>
                    <strong>
                      Status:
                    </strong>{" "}
                    Embeddings stored in ChromaDB
                  </p>

                )}

              </div>

            )}

          </section>

          {/* RIGHT — HOW IT WORKS */}

          <section className="process-card">

            <div className="process-header">

              <h2>
                How it works
              </h2>

              <p>
                Your uploaded knowledge goes
                through the AI pipeline.
              </p>

            </div>

            <div className="process-step">

              <div className="step-number">
                01
              </div>

              <div>

                <h3>
                  Upload
                </h3>

                <p>
                  Select your PDF, DOCX or
                  supported image file.
                </p>

              </div>

            </div>

            <div className="process-line" />

            <div className="process-step">

              <div className="step-number">
                02
              </div>

              <div>

                <h3>
                  Extract
                </h3>

                <p>
                  Text is extracted from
                  the uploaded file.
                </p>

              </div>

            </div>

            <div className="process-line" />

            <div className="process-step">

              <div className="step-number">
                03
              </div>

              <div>

                <h3>
                  Process
                </h3>

                <p>
                  Content is divided into
                  smaller chunks.
                </p>

              </div>

            </div>

            <div className="process-line" />

            <div className="process-step">

              <div className="step-number">
                04
              </div>

              <div>

                <h3>
                  Embed
                </h3>

                <p>
                  MiniLM converts the chunks
                  into embeddings.
                </p>

              </div>

            </div>

            <div className="process-line" />

            <div className="process-step">

              <div className="step-number">
                05
              </div>

              <div>

                <h3>
                  Store
                </h3>

                <p>
                  Chunks and embeddings are
                  stored in ChromaDB.
                </p>

              </div>

            </div>

          </section>

        </div>

      </main>

    </div>
  );
}

export default Upload;