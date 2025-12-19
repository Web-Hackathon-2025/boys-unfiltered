import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authAPI, getCurrentUser } from "../../services/api";

export default function Login() {
<<<<<<< HEAD
=======
  const { login, demoLogin } = useAuth();
>>>>>>> c229480abe1d16e291e9eb5d70fc6b39e8fd2577
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
      await authAPI.login(formData);
      const user = getCurrentUser();
      if (user?.role) {
        // Redirect based on user role
        if (user.role === 'admin') {
          navigate('/admin/dashboard');
        } else if (user.role === 'provider') {
          navigate('/provider/dashboard');
        } else {
          navigate('/customer/dashboard');
        }
      } else {
        navigate('/');
      }
    } catch (err) {
      console.error("Login error:", err);
      setError(err.response?.data?.detail || "Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (role) => {
    demoLogin(role);
    navigate(`/${role}`);
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
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 rounded text-sm">
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
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />

            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-500">
            Don't have an account?{" "}
            <Link to="/register/customer" className="text-blue-600 hover:underline font-medium">
              Register as Customer
            </Link>{" "}
            or{" "}
            <Link to="/register/provider" className="text-green-600 hover:underline font-medium">
              Register as Provider
            </Link>
          </div>

          <div className="mt-4">
            <p className="text-center text-xs text-gray-400 mb-2">Demo Logins</p>
            <div className="space-y-2">
              <button
                onClick={() => handleDemoLogin("customer")}
                className="w-full bg-blue-100 hover:bg-blue-200 text-blue-700 py-2 rounded text-sm font-medium"
              >
                Demo Customer Login
              </button>
              <button
                onClick={() => handleDemoLogin("provider")}
                className="w-full bg-green-100 hover:bg-green-200 text-green-700 py-2 rounded text-sm font-medium"
              >
                Demo Provider Login
              </button>
              <button
                onClick={() => handleDemoLogin("admin")}
                className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 rounded text-sm font-medium"
              >
                Demo Admin Login
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* RIGHT: BRAND IMAGE */}
      <div className="hidden md:flex items-center justify-center bg-gradient-to-br from-blue-900 to-slate-900 text-white">
        <div className="max-w-md px-6">
          <h2 className="text-3xl font-bold mb-4">
            Hire trusted local professionals
          </h2>
          <p className="text-blue-100 mb-6">
            From electricians to plumbers, Karigar helps you
            find reliable services near you — quickly and safely.
          </p>

          <ul className="space-y-3 text-blue-100">
            <li className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Verified service providers
            </li>
            <li className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Transparent pricing
            </li>
            <li className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Simple booking process
            </li>
            <li className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              24/7 customer support
            </li>
          </ul>
        </div>
      </div>

    </div>
  );
}