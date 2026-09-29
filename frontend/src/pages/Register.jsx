import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/axios";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");
    setLoading(true);

    try {
      await api.post(
        "/auth/register",
        formData
      );

      setMessage(
        "Registration successful! Redirecting to login..."
      );

      setTimeout(() => {
        navigate("/login");
      }, 1000);

    } catch (error) {
      console.error(
        "Registration error:",
        error
      );

      setMessage(
        error.response?.data?.message ||
        error.response?.data?.error ||
        "Registration failed."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">

      <div className="auth-wrapper">

        {/* LEFT BRAND */}

        <div className="auth-brand">

          <div className="brand-icon">
            🧠
          </div>

          <h1>
            Second Brain
          </h1>

          <p>
            Personal Knowledge Assistant
          </p>

          <div className="brand-line"></div>

          <span>
            Build your personal knowledge base.
            <br />
            Store notes and documents.
            <br />
            Ask questions using AI.
          </span>

        </div>


        {/* REGISTER */}

        <div className="auth-form-section">

          <div className="auth-form-card">

            <div className="auth-heading">

              <h2>
                Create Account
              </h2>

              <p>
                Start building your personal
                knowledge base.
              </p>

            </div>


            <form
              onSubmit={handleSubmit}
              className="auth-form"
            >

              <div className="form-group">

                <label>
                  Full Name
                </label>

                <input
                  type="text"
                  name="name"
                  placeholder="Enter your name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />

              </div>


              <div className="form-group">

                <label>
                  Email Address
                </label>

                <input
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />

              </div>


              <div className="form-group">

                <label>
                  Password
                </label>

                <input
                  type="password"
                  name="password"
                  placeholder="Create a password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />

              </div>


              <button
                type="submit"
                className="auth-submit-btn"
                disabled={loading}
              >
                {loading
                  ? "Creating Account..."
                  : "Create Account"}
              </button>

            </form>


            {message && (
              <div
                className={
                  message.startsWith(
                    "Registration successful"
                  )
                    ? "auth-success"
                    : "auth-error"
                }
              >
                {message}
              </div>
            )}


            <div className="auth-footer">

              <span>
                Already have an account?
              </span>

              <Link to="/login">
                Sign in
              </Link>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Register;