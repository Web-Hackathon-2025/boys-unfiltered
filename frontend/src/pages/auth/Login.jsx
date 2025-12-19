import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = (role) => {
    login(role);
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

          {/* Mock role login buttons */}
          <div className="space-y-3">
            <button
              onClick={() => handleLogin("customer")}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded font-medium"
            >
              Continue as Customer
            </button>

            <button
              onClick={() => handleLogin("provider")}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded font-medium"
            >
              Continue as Service Provider
            </button>

            <button
              onClick={() => handleLogin("admin")}
              className="w-full bg-gray-800 hover:bg-gray-900 text-white py-3 rounded font-medium"
            >
              Continue as Admin
            </button>
          </div>

          <div className="mt-6 text-center text-sm text-gray-500">
            This is a demo login UI.  
            <br />
            Backend auth will be added later.
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
