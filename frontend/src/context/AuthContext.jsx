import React, { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  // user = { role, id, name }

  const login = (role) => {
    if (role === "provider") {
      setUser({
        role: "provider",
        id: 1, // 🔑 must match provider id in mockData.js
        name: "Muhammad Ali",
      });
    } else if (role === "customer") {
      setUser({
        role: "customer",
        id: 101,
        name: "Rohan",
      });
    } else {
      setUser({
        role: "admin",
        id: 999,
        name: "Admin",
      });
    }
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
