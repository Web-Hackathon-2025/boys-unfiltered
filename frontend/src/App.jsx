import { Routes, Route } from "react-router-dom";
import Layout from "./components/layout/Layout";
import ProtectedRoute from "./routes/ProtectedRoute";

import Home from "./pages/Home";
import Login from "./pages/auth/Login";
import BrowseProviders from "./pages/customer/BrowseProviders";
import ProviderProfile from "./pages/customer/ProviderProfile";
import ProviderDashboard from "./pages/provider/Dashboard";
import AdminDashboard from "./pages/admin/AdminDashboard";

export default function App() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />

      {/* Customer Dashboard */}
      <Route
        path="/customer"
        element={
          <ProtectedRoute role="customer">
            <Layout>
              <BrowseProviders />
            </Layout>
          </ProtectedRoute>
        }
      />

      {/* ✅ PROVIDER PROFILE — MUST BE TOP LEVEL */}
      <Route
        path="/providers/:id"
        element={
          <ProtectedRoute role="customer">
            <Layout>
              <ProviderProfile />
            </Layout>
          </ProtectedRoute>
        }
      />

      {/* Provider */}
      <Route
        path="/provider"
        element={
          <ProtectedRoute role="provider">
            <Layout>
              <ProviderDashboard />
            </Layout>
          </ProtectedRoute>
        }
      />

      {/* Admin */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute role="admin">
            <Layout>
              <AdminDashboard />
            </Layout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
