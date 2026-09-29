import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/axios";

function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
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
      const response = await api.post(
        "/auth/login",
        formData
      );

      const token = response.data.access_token;

      localStorage.setItem("jwt_token", token);

      setMessage("Login successful!");

      setTimeout(() => {
        navigate("/dashboard");
      }, 500);

    } catch (error) {
      console.error("Login error:", error);

      setMessage(
        error.response?.data?.message ||
        error.response?.data?.error ||
        "Invalid email or password."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">

      <div className="auth-wrapper">

        {/* LEFT BRAND SECTION */}

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
            Store your knowledge.
            <br />
            Search it intelligently.
            <br />
            Ask your AI.
          </span>

        </div>


        {/* LOGIN CARD */}

        <div className="auth-form-section">

          <div className="auth-form-card">

            <div className="auth-heading">

              <h2>
                Welcome Back
              </h2>

              <p>
                Sign in to continue to your
                personal knowledge assistant.
              </p>

            </div>


            <form
              onSubmit={handleSubmit}
              className="auth-form"
            >

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
                  placeholder="Enter your password"
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
                  ? "Signing in..."
                  : "Sign In"}
              </button>

            </form>


            {message && (
              <div
                className={
                  message === "Login successful!"
                    ? "auth-success"
                    : "auth-error"
                }
              >
                {message}
              </div>
            )}


            <div className="auth-footer">

              <span>
                Don't have an account?
              </span>

              <Link to="/register">
                Create an account
              </Link>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Login;