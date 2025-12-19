import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const user = await login(formData.email, formData.password);
      navigate(`/${user.role}`);
    } catch (err) {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-2">
      
      {/* LEFT: LOGIN CARD */}
      <div className="flex items-center justify-center bg-slate-50">
        <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-md">
          
          <h1 className="text-2xl font-bold mb-2">
            Welcome to <span className="text-blue-600">Karigar</span>
          </h1>
          <p className="text-gray-500 mb-6">
            Login to continue
          </p>

          {error && (
            <div className="mb-4 text-red-600 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
              className="w-full border rounded px-4 py-2"
              required
            />

            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className="w-full border rounded px-4 py-2"
              required
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded font-medium disabled:opacity-50"
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-500">
            Don't have an account?{" "}
            <Link to="/register/customer" className="text-blue-600 hover:underline">
              Register as Customer
            </Link>{" "}
            or{" "}
            <Link to="/register/provider" className="text-green-600 hover:underline">
              Register as Provider
            </Link>
          </div>
        </div>
      </div>

      {/* RIGHT: BRAND IMAGE */}
      <div className="hidden md:flex items-center justify-center bg-slate-900 text-white">
        <div className="max-w-md px-6">
          <h2 className="text-3xl font-bold mb-4">
            Hire trusted local professionals
          </h2>
          <p className="text-slate-300 mb-6">
            From electricians to plumbers, Karigar helps you
            find reliable services near you — quickly and safely.
          </p>

          <ul className="space-y-3 text-slate-200">
            <li>✔ Verified service providers</li>
            <li>✔ Transparent pricing</li>
            <li>✔ Simple booking process</li>
          </ul>
        </div>
      </div>

    </div>
  );
}
