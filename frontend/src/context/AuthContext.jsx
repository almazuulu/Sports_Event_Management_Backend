import { createContext, useContext, useState, useEffect } from "react";
import { toast } from "react-toastify";

const AuthContext = createContext(null);

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem("user"));
    if (storedUser) setUser(storedUser);
  }, []);

  const login = async (credentials) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          login: credentials.username,
          email: credentials.email,
          password: credentials.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        toast.error("Login failed!");
      }

      if (response.ok) {
        localStorage.setItem("user", JSON.stringify(data));

        const getProfileUser = await fetch(
          "http://127.0.0.1:8000/api/users/profile/",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${data.access}`,
            },
          }
        );

        const profileData = await getProfileUser.json();

        if (getProfileUser.ok) {
          const existingUser = JSON.parselocalStorage.getItem("user");
          const updatedUser = { ...existingUser, ...profileData };
          localStorage.setItem("user", JSON.stringify(updatedUser));
        }
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
