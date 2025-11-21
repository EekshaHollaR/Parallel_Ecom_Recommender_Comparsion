import React, { createContext, useState, useEffect, useContext } from 'react';
import jwt_decode from 'jwt-decode';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      try {
        const decoded = jwt_decode(token);
        // Check expiry
        if (decoded.exp * 1000 < Date.now()) {
          logout();
        } else {
          setUser({ username: decoded.sub });
          localStorage.setItem('token', token);
        }
      } catch (e) {
        logout();
      }
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const login = (newToken) => {
    setToken(newToken);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
