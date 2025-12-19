import React, { createContext, useContext, useState, useEffect } from "react";
import { api } from "../services/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load user from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  // Save user to localStorage whenever it changes
  useEffect(() => {
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);

  const login = async (email, password) => {
    try {
      const response = await api.login({ email, password });
      const userData = {
        id: response.user.id,
        email: response.user.email,
        role: response.role,
        name: `${response.user.first_name} ${response.user.last_name}`,
      };
      setUser(userData);
      return userData;
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    // Optionally call logout API
  };

  const demoLogin = (role) => {
    if (role === "provider") {
      setUser({
        id: 1,
        email: "provider@example.com",
        role: "provider",
        name: "Muhammad Ali",
      });
    } else if (role === "customer") {
      setUser({
        id: 101,
        email: "customer@example.com",
        role: "customer",
        name: "Rohan Singh",
      });
    } else if (role === "admin") {
      setUser({
        id: 999,
        email: "admin@example.com",
        role: "admin",
        name: "Admin User",
      });
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, demoLogin, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
