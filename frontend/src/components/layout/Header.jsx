import { Link } from "react-router-dom";
import { FaTools, FaUserCircle, FaSignOutAlt } from "react-icons/fa";
import { useAuth } from "../../context/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="bg-slate-900 text-white sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* LOGO / WORDMARK */}
        <Link to="/" className="flex items-center gap-2">
          <FaTools className="text-green-500 text-xl" />
          <span className="text-lg font-bold tracking-wide">
            Karigar
          </span>
        </Link>

        {/* NAV LINKS */}
        <nav className="hidden md:flex items-center gap-8 text-sm">
          <Link
            to="/"
            className="hover:text-green-400 transition"
          >
            Home
          </Link>
          {user && (
            <Link
              to={`/${user.role}`}
              className="hover:text-green-400 transition"
            >
              Dashboard
            </Link>
          )}
        </nav>

        {/* AUTH / CTA */}
        <div className="flex items-center gap-4">
          {user ? (
            <>
              <span className="text-sm">Welcome, {user.name}</span>
              <button
                onClick={logout}
                className="flex items-center gap-2 text-sm hover:text-green-400 transition"
              >
                <FaSignOutAlt />
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="flex items-center gap-2 text-sm hover:text-green-400 transition"
              >
                <FaUserCircle />
                Login
              </Link>

              <Link
                to="/register/customer"
                className="hidden sm:inline-block bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition"
              >
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
