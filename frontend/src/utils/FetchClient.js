import { getAccessToken, getRefreshToken } from "./Authentication";

const API_URL = "http://127.0.0.1:8000";

const saveTokens = (accessToken, refreshToken) => {
  localStorage.setItem("accessToken", accessToken);
  if (refreshToken) localStorage.setItem("refreshToken", refreshToken);
};

const verifyAccessToken = async (accessToken) => {
  try {
    const response = await fetch(`${API_URL}/api/token/verify/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token: accessToken }),
    });

    return response.ok;
  } catch (error) {
    console.error("Error verifying token:", error);
    return false;
  }
};

const refreshAccessToken = async () => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return null;

  try {
    const response = await fetch(`${API_URL}/api/token/refresh/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) return null;

    const data = await response.json();
    saveTokens(data.access, data?.refresh);
    return data.access;
  } catch (error) {
    console.error("Error refreshing token:", error);
    return null;
  }
};

const fetchWithAuth = async (url, options = {}) => {
  let accessToken = getAccessToken();

  if (accessToken && !(await verifyAccessToken(accessToken))) {
    console.warn("Access token invalid, refreshing...");
    accessToken = await refreshAccessToken();
  }

  if (!accessToken) {
    console.error("Failed to refresh token. Please log in again.");
    return { error: "Unauthorized" };
  }

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${accessToken}`,
  };

  if (options.method !== "DELETE") {
    headers["Content-Type"] = "application/json";
  }

  return fetch(`${API_URL}${url}`, { ...options, headers });
};

const fetchWithoutAuth = async (url, options = {}) => {
  const headers = {
    ...options.headers,
  };

  if (options.method !== "DELETE") {
    headers["Content-Type"] = "application/json";
  }

  return fetch(`${API_URL}${url}`, { ...options, headers });
};

export { fetchWithAuth, fetchWithoutAuth, saveTokens };
